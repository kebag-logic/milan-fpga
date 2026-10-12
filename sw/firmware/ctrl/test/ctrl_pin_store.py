# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_pin_store.py - the pin proof's controls of Git's object store and of the repositories' own configuration (#697).

The pin proof reads the pinned commit and each tree under it raw from the
stack's object store, and hashes each here against its id
(ctrl_build.stored); it reads no blob, hashing each file of the checkout from
its own bytes instead. Git checks the hash of no object cat-file prints, nor
of a tree below the one ls-tree is given, so without that check an object
forged in the store would be read as the pinned one. Each of these controls
takes a clone of the stack whose objects are all loose in its own store (none
packed, none in another store), edits a source, and replaces the loose file of
one object of the pin with one holding the bytes of another that would hide the
edit (a new file, so no file a hard link shares is written):
- the pinned src/ tree, with a tree holding the edit (R585-12's F1): refused
  as a forged object, by the tree's place;
- the pinned commit, with a commit whose tree holds the edit: refused as a
  forged object, the pinned commit;
- the pinned blob of the edited source, with the edit's: refused by the edited
  source's name, since the proof reads no blob.
The helper gives Git core.fsmonitor=false, so no repository's own
configuration starts a program when Git reads an index. Two controls name a
recorder (ctrl_pin_env.RECORDER) as core.fsmonitor in a repository's own
configuration: a superproject's, whose index's gitlink is the pin, read as the
proof reads the checkout's (ctrl_build.stack_gitlink); and the stack clone's,
beside an edit. Each ends in the verdict its repository earns, and the
recorder never runs.
"""

from __future__ import annotations

import shutil
from collections.abc import Callable
from pathlib import Path

from ctrl_build import Refusal, stack_gitlink, stack_pin
from ctrl_pin_env import EDITED, GITLINK, Scene, answer

#: More objects than a fetch of the pin's history brings, so that the fetch unpacks each into a loose object
#: rather than keep the pack it is sent.
UNPACK_LIMIT = 1_000_000
#: The pin check's words for an object of the store that does not hash to its id.
FORGED = "holds a forged or corrupt object: "


def loose(scene: Scene) -> None:
    """The clone made again with every object of the pin's history loose in its own store, none packed and none
    in another store: fetched from the clone into a new repository, then checked out at the pin."""
    packed = scene.own / "packed"
    scene.stack.rename(packed)
    answer(scene.own, "init", "--quiet", str(scene.stack))
    answer(scene.stack, "-c", f"fetch.unpackLimit={UNPACK_LIMIT}", "fetch", "--quiet", "--no-tags", str(packed),
           "HEAD")
    answer(scene.stack, "-c", "advice.detachedHead=false", "checkout", "--quiet", scene.pin)
    shutil.rmtree(packed)
    store = scene.stack / ".git/objects"
    if any((store / "pack").iterdir()) or (store / "info/alternates").exists():
        raise Refusal("an object-store control's clone keeps a pack or another store, so it cannot forge an object")


def forge(scene: Scene, victim: str, source: str) -> None:
    """Reading the object `victim` gives the object `source`'s bytes: its loose file replaced by a new one holding
    theirs, so that no file another store may share through a hard link is written."""
    if victim == source:
        raise Refusal(f"an object-store control would forge {victim[:8]} with itself")
    taken, given = (scene.stack / ".git/objects" / oid[:2] / oid[2:] for oid in (victim, source))
    forged = taken.with_name(taken.name + ".forged")
    forged.write_bytes(given.read_bytes())
    forged.replace(taken)


def forged_tree(scene: Scene) -> None:
    """The edit on disk, and the pinned src/ tree's object overwritten by a tree holding it (R585-12's F1)."""
    loose(scene)
    scene.edit()
    forge(scene, *scene.edited_src())


def forged_commit(scene: Scene) -> None:
    """The edit on disk, and the pinned commit's object overwritten by a copy of it whose tree holds the edit."""
    loose(scene)
    scene.edit()
    _, src = scene.edited_src()
    root = answer(scene.stack, "rev-parse", f"{scene.pin}^{{tree}}").strip()
    commit = answer(scene.stack, "cat-file", "commit", scene.pin)
    copy = commit.replace(f"tree {root}\n", f"tree {scene.remade(root, 'src', src)}\n", 1)
    forge(scene, scene.pin, answer(scene.stack, "hash-object", "-t", "commit", "-w", "--stdin", stdin=copy).strip())


def forged_blob(scene: Scene) -> None:
    """The edit on disk, and the object of the edited source's pinned blob overwritten by the edit's."""
    loose(scene)
    scene.edit()
    blob = answer(scene.stack, "hash-object", "-w", "--stdin", stdin=scene.edited()).strip()
    forge(scene, answer(scene.stack, "rev-parse", f"{scene.pin}:{EDITED}").strip(), blob)


def monitored_superproject(scene: Scene) -> None:
    """A superproject whose index's gitlink is the pin, and whose own configuration names the recorder as
    core.fsmonitor."""
    top = scene.own / "superproject"
    answer(scene.own, "init", "--quiet", str(top))
    answer(top, "update-index", "--add", "--cacheinfo", f"160000,{scene.pin},{GITLINK}")
    answer(top, "config", "core.fsmonitor", scene.recorder())


def monitored_stack(scene: Scene) -> None:
    """The clone's own configuration naming the recorder as core.fsmonitor, and the edit on disk."""
    answer(scene.stack, "config", "core.fsmonitor", scene.recorder())
    scene.edit()


def store_arms(stack: Path, pin: str, work: Path, edited: str) -> list[tuple]:
    """The pin controls of the object store and of the repositories' own configuration, as ctrl_pin.pin_controls
    runs them (each after a fresh clone of the stack at `stack`, pinned at `pin`): each must end in its verdict,
    and no program a configuration names may run. `edited` begins the refusal of a checkout that differs."""
    own = work / "store"
    scene = Scene(stack, pin, own)

    def spoiled(spoil: Callable[[Scene], None]) -> Callable[[], None]:
        """`spoil`, in a control directory of its own made afresh."""
        def prepared() -> None:
            """The control's directory afresh, then `spoil`."""
            if own.exists():
                shutil.rmtree(own)
            own.mkdir(parents=True)
            spoil(scene)
        return prepared

    def gitlink() -> str:
        """The superproject's gitlink, read as the pin proof reads the checkout's: the pin, or a Refusal."""
        said = stack_gitlink(own / "superproject")
        if said != pin:
            raise Refusal(f"the superproject's gitlink was read as {said}, not as the pin {pin}")
        return said

    def judged(read: Callable[[], str], needle: str) -> tuple[bool, str]:
        """`read`'s verdict: accepted, and what it said. A program a configuration names that Git ran fails the
        control, whatever the verdict."""
        try:
            accepted, said = True, f"accepted {read()}"
        except Refusal as exc:
            accepted, said = False, str(exc)
        ran = sorted(own.rglob("ran"))
        if ran:
            return bool(needle), f"Git ran a program a repository's own configuration names: " \
                                 f"{ran[0].read_text(encoding='utf-8').splitlines()[0]}"
        return accepted, said

    def checked() -> str:
        """The pin check on the clone."""
        return stack_pin(stack, pin)

    controls = (
        ("the object store, a source edited, the pinned src/ tree's object overwritten by a tree holding the edit",
         forged_tree, checked, FORGED + "the pinned src/ tree"),
        ("the object store, a source edited, the pinned commit's object overwritten by a commit whose tree holds "
         "the edit", forged_commit, checked, FORGED + "the pinned commit"),
        ("the object store, a source edited, its pinned blob's object overwritten by the edit's", forged_blob,
         checked, edited + EDITED),
        ("the superproject's own configuration, a program named as core.fsmonitor, its gitlink read",
         monitored_superproject, gitlink, ""),
        ("the stack's own configuration, a program named as core.fsmonitor, a source edited", monitored_stack,
         checked, edited + EDITED),
    )
    return [(what, spoiled(spoil), lambda r=read, n=needle: judged(r, n), needle)
            for what, spoil, read, needle in controls]
