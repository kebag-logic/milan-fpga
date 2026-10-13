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
Both repositories' keys are parsed by one parser (ctrl_build.parsed_key)
into a section, a subsection (none, empty or named) and a variable.
The stack's own configuration may hold only Git's own bookkeeping of a
clone and a submodule (ctrl_build.STACK_CONFIG, its allowlist, `*` standing
for a named subsection), and the pin check refuses every other key by its
name before it reads an object (ctrl_build.configured). One control holds
each family of keys it refuses, each key naming a recorder
(ctrl_pin_env.RECORDER) where it names a program:
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
accepted, and one holding submodule "".active, an allowlisted section and
variable with an empty subsection, is refused by that key. A clean filter in
the clone's own configuration is held by ctrl_pin.py's control.
The superproject's own configuration may not hold a key of the sections and
variables ctrl_build.SUPERPROJECT_REFUSED names, whatever its subsection: a
promisor remote and its transport (extensions.partialClone,
remote.promisor, remote.partialCloneFilter, remote.uploadpack,
core.sshCommand) and core.fsmonitor. The pin check refuses each by its name
before it reads the gitlink from the superproject's index
(ctrl_build.superproject_configured), so the superproject declares no
promisor remote in any key spelling Git reads, judged by section and
variable; its other keys are not judged. Eight controls read the gitlink of a
superproject whose index records the pin, as the proof reads the checkout's
(ctrl_build.stack_gitlink):
- its own configuration naming the recorder as core.fsmonitor;
- a partial clone whose sparse index lacks the tree that holds the gitlink, as
  R585-14 probed it: its promisor remote's upload-pack the recorder, which
  then serves the tree (SERVER), and its remote reached over ssh through
  core.sshCommand;
- that sparse index beside a promisor remote declared without a subsection
  (remote.promisor, remote.partialCloneFilter) or with an empty one
  (remote "".promisor), as R584-14 probed it, which Git names "" and reaches
  through the recorder by an ext:: URL rewrite (unnamed_promisor);
- an included file and its work tree's own configuration, each naming the
  recorder as core.fsmonitor.
Each ends in the refusal naming exactly the refused keys it planted, and the
recorder never runs. An eighth, the superproject configured as
actions/checkout and git submodule update --init leave it (its token as
http.<url>.extraheader, the stack's submodule entries), is read as the pin.
The helper also gives Git core.fsmonitor=false and GIT_NO_LAZY_FETCH=1,
defence in depth behind both repositories' checks.
"""

from __future__ import annotations

import shutil
from collections.abc import Callable
from pathlib import Path

from ctrl_build import (STACK_CONFIG, SUPERPROJECT_KEYS, UNLISTED, Refusal, family, parsed_key, stack_gitlink,
                        stack_pin)
from ctrl_pin_env import EDITED, GITLINK, RECORDER, Scene, answer, create

#: More objects than a fetch of the pin's history brings, so that the fetch unpacks each into a loose object
#: rather than keep the pack it is sent.
UNPACK_LIMIT = 1_000_000
#: The pin check's words for an object of the store that does not hash to its id.
FORGED = "holds a forged or corrupt object: "
#: The program a superproject's promisor remote's upload-pack control names: it records that it ran, as the
#: recorder does (ctrl_pin_env.RECORDER), then serves what it is asked for, so that a Git that fetched through it
#: would be given the tree the superproject lacks, read the gitlink, and accept.
SERVER = '#!/bin/sh\necho "$0 $*" >> "$(dirname "$0")/ran"\nexec git-upload-pack "$@"\n'


def loose(scene: Scene) -> None:
    """The clone made again with every object of the pin's history loose in its own store, none packed and none
    in another store: fetched from the clone into a new repository, then checked out at the pin."""
    packed = scene.own / "packed"
    scene.stack.rename(packed)
    create(scene.stack)
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


def superproject(scene: Scene, keys: tuple[tuple[str, str], ...]) -> None:
    """A superproject whose index's gitlink is the pin, `keys` set in its own configuration."""
    top = scene.own / "superproject"
    create(top)
    answer(top, "update-index", "--add", "--cacheinfo", f"160000,{scene.pin},{GITLINK}")
    for key, value in keys:
        answer(top, "config", key, value)


def checked_out(scene: Scene) -> None:
    """A superproject whose gitlink is the pin, its own configuration holding what actions/checkout writes there
    (the remote, gc.auto, the token as http.<url>.extraheader) and what git submodule update --init writes for
    the stack (its url, and active)."""
    superproject(scene, (("remote.origin.url", "https://github.com/kebag-logic/milan-fpga"),
                         ("remote.origin.fetch", "+refs/heads/*:refs/remotes/origin/*"), ("gc.auto", "0"),
                         ("http.https://github.com/.extraheader", "AUTHORIZATION: basic pin-control"),
                         (f"submodule.{GITLINK}.url", "https://github.com/kebag-logic/tsn-c-stack.git"),
                         (f"submodule.{GITLINK}.active", "true")))


def superproject_included(scene: Scene) -> None:
    """A superproject whose gitlink is the pin, its own configuration including (include.path) a file that names
    the recorder as core.fsmonitor, and its work tree's own configuration (extensions.worktreeConfig) naming it."""
    (scene.own / "included").write_text(f"[core]\n\tfsmonitor = {scene.recorder()}\n", encoding="utf-8")
    superproject(scene, (("include.path", str(scene.own / "included")), ("extensions.worktreeConfig", "true")))
    answer(scene.own / "superproject", "config", "--worktree", "core.fsmonitor", scene.recorder())


def sparse_superproject(scene: Scene, keys: Callable[[Path], tuple[tuple[str, str | None], ...]]) -> None:
    """A superproject whose sparse index holds the gitlink (the pin) under a sparse directory whose tree its own
    store lacks, as R585-14 probed it: fetched, every object loose, from an origin beside it that holds the tree,
    made sparse outside another directory, then checked out, then that tree's object removed; then `keys`
    (given the origin's path) set in its own configuration, a value None naming the recorder. A Git reading the
    gitlink must fetch the tree first."""
    origin, top, parent = scene.own / "origin", scene.own / "superproject", GITLINK.rpartition("/")[0]
    create(origin)
    (origin / "kept").mkdir()
    (origin / "kept/file").write_text("kept\n", encoding="utf-8")
    answer(origin, "add", "kept/file")
    answer(origin, "update-index", "--add", "--cacheinfo", f"160000,{scene.pin},{GITLINK}")
    answer(origin, "-c", "user.name=pin-control", "-c", "user.email=pin-control@invalid", "commit", "--quiet", "-m",
           "pin-control")
    create(top)
    answer(top, "-c", f"fetch.unpackLimit={UNPACK_LIMIT}", "fetch", "--quiet", "--no-tags", str(origin), "HEAD")
    answer(top, "update-ref", "HEAD", "FETCH_HEAD")
    answer(top, "sparse-checkout", "set", "--cone", "--sparse-index", "kept")
    answer(top, "checkout", "--quiet")
    tree = answer(top, "rev-parse", f"HEAD:{parent}").strip()
    if f"040000 {tree} 0\t{parent}/" not in answer(top, "ls-files", "--sparse", "--stage").splitlines():
        raise Refusal("the sparse superproject control's index holds no sparse directory around the gitlink")
    (top / ".git/objects" / tree[:2] / tree[2:]).unlink()
    if any((top / ".git/objects/pack").iterdir()):
        raise Refusal("the sparse superproject control's superproject keeps a pack, so it may still hold the tree")
    for key, value in keys(origin):
        answer(top, "config", key, scene.recorder() if value is None else value)


def served(scene: Scene) -> str:
    """The recorder that serves (SERVER), in the control's own directory, its record beside it."""
    program = scene.own / "server"
    program.write_text(SERVER, encoding="utf-8")
    program.chmod(0o755)
    return str(program)


def unnamed_promisor(scene: Scene, key: str, value: str) -> None:
    """A sparse superproject (sparse_superproject) whose own configuration declares a promisor remote by `key` alone,
    in a spelling without a subsection or with an empty one, as R584-14 probed it: Git names that remote "" and
    fetches from "" as a URL, which an empty url.<base>.insteadOf rewrites to an ext:: transport whose program is
    the recorder (protocol.ext.allow=always). The superproject's check refuses neither of those two keys, so its
    refusal names `key` alone."""
    sparse_superproject(scene, lambda _: ((key, value), (f"url.ext::{scene.recorder()}.insteadOf", ""),
                                          ("protocol.ext.allow", "always")))


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
    held = {family(*parsed_key(entry.partition("\n")[0]))
            for entry in filter(None, answer(scene.stack, "config", "--list", "--local", "-z").split("\0"))}
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


#: The spellings of a promisor remote without a subsection or with an empty one (unnamed_promisor), as R584-14
#: probed them: what each is, the key set and its value, and the key as Git lists it.
UNNAMED = (("remote.promisor, no subsection", "remote.promisor", "true", "remote.promisor"),
           ("remote.partialCloneFilter, no subsection", "remote.partialCloneFilter", "tree:0",
            "remote.partialclonefilter"),
           ('remote "".promisor, an empty subsection', "remote..promisor", "true", "remote..promisor"))


def refused(*keys: str) -> str:
    """The pin check's refusal of exactly `keys` of the superproject's own configuration, each with its scope."""
    return SUPERPROJECT_KEYS + ", ".join(keys)


def unlisted(*keys: str) -> str:
    """The pin check's refusal of exactly `keys` of the stack's own configuration, each with its scope."""
    return UNLISTED + ", ".join(keys)


def superproject_controls(gitlink: Callable[[], str]) -> tuple[tuple, ...]:
    """The controls of the superproject's own configuration (store_arms), each read by `gitlink`: what it is, how
    the superproject is made, how it is read, and the words its verdict must hold (none: the pin is read)."""
    return (
        ("the superproject's own configuration, a program named as core.fsmonitor, its gitlink read",
         lambda s: superproject(s, (("core.fsmonitor", s.recorder()),)), gitlink, refused("core.fsmonitor (local)")),
        ("the superproject's own configuration, a sparse index whose sparse directory holding the gitlink lacks its "
         "tree, a partial clone whose promisor remote's upload-pack is a program that serves it, its gitlink read",
         lambda s: sparse_superproject(s, lambda origin: (*partial("origin", str(origin)),
                                                          ("remote.origin.partialCloneFilter", "tree:0"),
                                                          ("remote.origin.uploadpack", served(s)))), gitlink,
         refused("extensions.partialclone (local)", "remote.origin.partialclonefilter (local)",
                 "remote.origin.promisor (local)", "remote.origin.uploadpack (local)")),
        ("the superproject's own configuration, a sparse index whose sparse directory holding the gitlink lacks its "
         "tree, a partial clone whose promisor remote is reached over ssh by a program (core.sshCommand), its gitlink "
         "read",
         lambda s: sparse_superproject(s, lambda _: (*partial("probe", "ssh://pin-control.invalid/superproject"),
                                                     ("core.sshCommand", None))), gitlink,
         refused("core.sshcommand (local)", "extensions.partialclone (local)", "remote.probe.promisor (local)")),
        *(("the superproject's own configuration, a sparse index whose sparse directory holding the gitlink lacks its "
           f"tree, a promisor remote declared by {what}, reached through a program by an ext:: URL rewrite, its "
           "gitlink read", lambda s, k=key, v=value: unnamed_promisor(s, k, v), gitlink, refused(f"{listed} (local)"))
          for what, key, value, listed in UNNAMED),
        ("the superproject's own configuration, an included file (include.path) and its work tree's own "
         "configuration each naming a program as core.fsmonitor, its gitlink read", superproject_included, gitlink,
         refused("core.fsmonitor (local)", "core.fsmonitor (worktree)")),
        ("the superproject's own configuration as actions/checkout and git submodule update --init write it, its "
         "gitlink read", checked_out, gitlink, ""))


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
        ("the stack's attributes, a source's line endings changed, a conversion they give turning it back into the "
         "pinned blob", converted, checked, edited + EDITED),
        *superproject_controls(gitlink),
        ("the stack's own configuration, a program named as core.fsmonitor, a source edited", monitored_stack,
         checked, unlisted("core.fsmonitor (local)")),
        ("the stack's own configuration, a key of each family of its allowlist, the pinned clone", allowlisted,
         checked, ""),
        ("the stack's own configuration, a key of an allowlisted family's section and variable with an empty "
         'subsection (submodule "".active), the pinned clone', lambda s: keyed(s, (("submodule..active", "true"),)),
         checked, unlisted("submodule..active (local)")),
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
