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
Nor is a file hashed through Git: a source whose line endings the clone's
attributes have Git convert back into the pinned blob (text) is refused by
its name.
The stack's own configuration may hold only Git's own bookkeeping of a
clone and a submodule (ctrl_build.STACK_CONFIG, its allowlist), and the pin
check refuses every other key by its name before it reads an object
(ctrl_build.configured). One control holds each family of keys it refuses,
each key naming a recorder (ctrl_pin_env.RECORDER) where it names a program:
- a promisor remote whose transport is a program, beside a missing object of
  the pin, as R584-12 and R585-13 probed it: its upload-pack
  (remote.<name>.uploadpack), and ssh through core.sshCommand;
- each of those four keys alone: extensions.partialClone and
  remote.<name>.promisor beside the missing object, remote.<name>.uploadpack
  and core.sshCommand on the pinned clone;
- core.fsmonitor beside an edit, core.hooksPath, credential.helper, and the
  other programs Git may start (an askpass, a pager, an editor, a textconv, a
  signing program, an alternate refs command, a pack-objects hook);
- an include of a file that names a program, and a work tree's own
  configuration that does;
- a key no Git defines, as a later Git might add.
Each ends in the refusal naming exactly the keys it planted, and the recorder
never runs. A clone holding a key of every family of the allowlist is
accepted. A clean filter in the clone's own configuration is held by
ctrl_pin.py's control. The helper also gives Git core.fsmonitor=false, which
holds the superproject's own configuration: a superproject whose index's
gitlink is the pin, its configuration naming the recorder as core.fsmonitor,
is read as the proof reads the checkout's (ctrl_build.stack_gitlink), and
the recorder never runs.
"""

from __future__ import annotations

import shutil
from collections.abc import Callable
from pathlib import Path

from ctrl_build import STACK_CONFIG, UNLISTED, Refusal, stack_gitlink, stack_pin
from ctrl_pin_env import EDITED, GITLINK, RECORDER, Scene, answer

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


def converted(scene: Scene) -> None:
    """A source's line endings made CRLF, and the clone's attributes giving it the text attribute, which has Git
    convert them back when it hashes the file, so that a hash through Git is the pinned blob (checked here, or the
    control would prove nothing): a conversion no configuration names."""
    source = scene.stack / EDITED
    data = source.read_bytes()
    if b"\r" in data:
        raise Refusal("the line-ending control needs a source that holds no carriage return")
    source.write_bytes(data.replace(b"\n", b"\r\n"))
    (scene.stack / ".git/info/attributes").write_text(f"{EDITED} text\n", encoding="utf-8")
    if answer(scene.stack, "hash-object", EDITED) != answer(scene.stack, "rev-parse", f"{scene.pin}:{EDITED}"):
        raise Refusal("the line-ending control's conversion does not turn its edit back into the pinned blob")


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


def keyed(scene: Scene, keys: tuple[tuple[str, str | None], ...], missing: bool = False) -> None:
    """`keys` set in the clone's own configuration, a value None naming the recorder; first (`missing`) the clone
    made again with every object loose (loose) and the pinned src/ tree's object removed, so that Git reading the
    pin would fetch it from a promisor remote the keys name."""
    if missing:
        loose(scene)
        src = answer(scene.stack, "rev-parse", f"{scene.pin}:src").strip()
        (scene.stack / ".git/objects" / src[:2] / src[2:]).unlink()
    for key, value in keys:
        answer(scene.stack, "config", key, scene.recorder() if value is None else value)


def hooked(scene: Scene) -> None:
    """The clone's own configuration naming as core.hooksPath a directory whose hooks are the recorder."""
    hooks = scene.own / "hooks"
    hooks.mkdir()
    for hook in ("post-checkout", "post-index-change", "reference-transaction"):
        (hooks / hook).write_text(RECORDER, encoding="utf-8")
        (hooks / hook).chmod(0o755)
    answer(scene.stack, "config", "core.hooksPath", str(hooks))


def included(scene: Scene) -> None:
    """The clone's own configuration including (include.path) a file that names the recorder as core.fsmonitor."""
    (scene.own / "included").write_text(f"[core]\n\tfsmonitor = {scene.recorder()}\n", encoding="utf-8")
    answer(scene.stack, "config", "include.path", str(scene.own / "included"))


def worktree_configured(scene: Scene) -> None:
    """The clone's work tree given its own configuration (extensions.worktreeConfig), which names the recorder as
    core.fsmonitor."""
    answer(scene.stack, "config", "extensions.worktreeConfig", "true")
    answer(scene.stack, "config", "--worktree", "core.fsmonitor", scene.recorder())


def allowlisted(scene: Scene) -> None:
    """A key of each family of the allowlist (ctrl_build.STACK_CONFIG) in the clone's own configuration, beside the
    keys its clone holds, each naming what Git itself would: the clone's own work tree, a branch's remote, its
    submodules' bookkeeping. A family the clone then holds no key of refuses the control's setup."""
    keyed(scene, (("core.worktree", str(scene.stack)), ("branch.main.remote", "origin"),
                  ("branch.main.merge", "refs/heads/main"), ("submodule.active", "."),
                  ("submodule.pin-control.url", "../pin-control.git"), ("submodule.pin-control.active", "true"),
                  ("submodule.alternateLocation", "superproject"), ("submodule.alternateErrorStrategy", "die")))
    held = set()
    for entry in filter(None, answer(scene.stack, "config", "--list", "--local", "-z").split("\0")):
        key = entry.partition("\n")[0]
        section, _, rest = key.partition(".")
        subsection, _, variable = rest.rpartition(".")
        held.add(f"{section}.*.{variable}" if subsection else key)
    lacking = sorted(set(STACK_CONFIG) - held)
    if lacking:
        raise Refusal(f"the allowlisted configuration control's clone holds no {', '.join(lacking)}")


def partial(name: str, url: str) -> tuple[tuple[str, str | None], ...]:
    """The keys that make the clone a partial clone whose promisor remote is `name`, at `url`."""
    return (("core.repositoryformatversion", "1"), ("extensions.partialClone", name), (f"remote.{name}.url", url),
            (f"remote.{name}.promisor", "true"))


#: The programs Git may start that no other control names, each key naming the recorder.
HELPERS = ("core.askPass", "core.pager", "core.editor", "diff.pin-control.textconv", "gpg.program",
           "core.alternateRefsCommand", "uploadpack.packObjectsHook")


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

    def unlisted(*keys: str) -> str:
        """The pin check's refusal of exactly `keys` of the stack's own configuration, each with its scope."""
        return UNLISTED + ", ".join(keys)

    controls = (
        ("the object store, a source edited, the pinned src/ tree's object overwritten by a tree holding the edit",
         forged_tree, checked, FORGED + "the pinned src/ tree"),
        ("the object store, a source edited, the pinned commit's object overwritten by a commit whose tree holds "
         "the edit", forged_commit, checked, FORGED + "the pinned commit"),
        ("the object store, a source edited, its pinned blob's object overwritten by the edit's", forged_blob,
         checked, edited + EDITED),
        ("the stack's attributes, a source's line endings changed, a conversion they give turning it back into the "
         "pinned blob", converted, checked, edited + EDITED),
        ("the superproject's own configuration, a program named as core.fsmonitor, its gitlink read",
         monitored_superproject, gitlink, ""),
        ("the stack's own configuration, a program named as core.fsmonitor, a source edited", monitored_stack,
         checked, unlisted("core.fsmonitor (local)")),
        ("the stack's own configuration, a key of each family of its allowlist, the pinned clone", allowlisted,
         checked, ""),
        ("the stack's own configuration, a partial clone whose promisor remote's upload-pack is a program, the "
         "pinned src/ tree's object missing",
         lambda s: keyed(s, (*partial("origin", str(s.stack)), ("remote.origin.uploadpack", None)), True), checked,
         unlisted("extensions.partialclone (local)", "remote.origin.promisor (local)",
                  "remote.origin.uploadpack (local)")),
        ("the stack's own configuration, a partial clone whose promisor remote is reached over ssh by a program "
         "(core.sshCommand), the pinned src/ tree's object missing",
         lambda s: keyed(s, (*partial("probe", "ssh://pin-control.invalid/stack"), ("core.sshCommand", None)), True),
         checked, unlisted("core.sshcommand (local)", "extensions.partialclone (local)",
                           "remote.probe.promisor (local)")),
        ("the stack's own configuration, extensions.partialClone alone, the pinned src/ tree's object missing",
         lambda s: keyed(s, (("core.repositoryformatversion", "1"), ("extensions.partialClone", "origin"),
                             ("remote.origin.url", str(s.stack))), True), checked,
         unlisted("extensions.partialclone (local)")),
        ("the stack's own configuration, remote.<name>.promisor alone, the pinned src/ tree's object missing",
         lambda s: keyed(s, (("remote.origin.url", str(s.stack)), ("remote.origin.promisor", "true")), True),
         checked, unlisted("remote.origin.promisor (local)")),
        ("the stack's own configuration, a program named as remote.<name>.uploadpack",
         lambda s: keyed(s, (("remote.origin.uploadpack", None),)), checked,
         unlisted("remote.origin.uploadpack (local)")),
        ("the stack's own configuration, a program named as core.sshCommand",
         lambda s: keyed(s, (("core.sshCommand", None),)), checked, unlisted("core.sshcommand (local)")),
        ("the stack's own configuration, a directory of programs named as core.hooksPath", hooked, checked,
         unlisted("core.hookspath (local)")),
        ("the stack's own configuration, a program named as credential.helper",
         lambda s: keyed(s, (("credential.helper", None),)), checked, unlisted("credential.helper (local)")),
        ("the stack's own configuration, a program named by each other key Git starts one for",
         lambda s: keyed(s, tuple((key, None) for key in HELPERS)), checked,
         unlisted("core.alternaterefscommand (local)", "core.askpass (local)", "core.editor (local)",
                  "core.pager (local)", "diff.pin-control.textconv (local)", "gpg.program (local)",
                  "uploadpack.packobjectshook (local)")),
        ("the stack's own configuration, an included file (include.path) naming a program as core.fsmonitor",
         included, checked, unlisted("core.fsmonitor (local)", "include.path (local)")),
        ("the stack's work tree's own configuration (extensions.worktreeConfig), a program named as core.fsmonitor",
         worktree_configured, checked, unlisted("core.fsmonitor (worktree)", "extensions.worktreeconfig (local)")),
        ("the stack's own configuration, a key no Git defines, as a later Git might add, naming a program",
         lambda s: keyed(s, (("pin-control.program", None),)), checked, unlisted("pin-control.program (local)")),
    )
    return [(what, spoiled(spoil), lambda r=read, n=needle: judged(r, n), needle)
            for what, spoil, read, needle in controls]
