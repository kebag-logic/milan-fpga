# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_pin_env.py - the pin proof's controls of the environment it inherits (#697).

The pin proof's helper (ctrl_build.git) starts Git with the proof's own
environment, the whole of it (ctrl_build.GIT_ENVIRONMENT), and its audit hook
refuses any other (THE HOOK, ctrl_pin.py). These controls set, in the
environment of the process that runs the proof, each variable that would
redirect what Git reads if it reached Git:
- the repository: GIT_DIR, GIT_WORK_TREE, GIT_COMMON_DIR and GIT_INDEX_FILE;
- the object store: GIT_OBJECT_DIRECTORY and GIT_ALTERNATE_OBJECT_DIRECTORIES;
- the replacement refs: GIT_REPLACE_REF_BASE;
- the configuration: GIT_CONFIG_COUNT with its keys and values,
  GIT_CONFIG_PARAMETERS, GIT_CONFIG_GLOBAL, GIT_CONFIG_SYSTEM, HOME and
  XDG_CONFIG_HOME;
- the attributes: GIT_ATTR_SOURCE.
Each runs the pin proof as the checkout holds it, under its audit hook, in a
fresh interpreter (ctrl_pin.proof_run), on a clone of the stack prepared so
that the variable, if it reached Git, would change the verdict:
- an edited clone accepted, its edit committed in another repository;
- the gitlink read from another index, the clone at that revision;
- the pinned tree read from another store, or from none;
- a program the configuration names started by Git: core.fsmonitor, which Git
  runs when it reads an index, here a recorder.
Each must end in the verdict the clone itself earns, and no program the
configuration names may run. Two set what Git applies only when it hashes a
file through its filters, which the proof never does: a clean filter given
through GIT_CONFIG_COUNT, and one whose attribute is given through
GIT_ATTR_SOURCE. Each would turn the edit back into the pinned blob, as the
control checks. With every variable at once, the pinned clone is accepted.
GIT_REPLACE_REF_BASE is also held by GIT_NO_REPLACE_OBJECTS=1, so its control
fails only if both settings are lost. A last control gives the hook's judge of
the environment the list CPython 3.14's fork_exec gives, with a key twice.
"""

from __future__ import annotations

import shutil
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from ctrl_build import GIT_ENVIRONMENT, ROOT, STACK, Refusal, environment_judge, git

#: The gitlink's path in the checkout, which another index records.
GITLINK = STACK.relative_to(ROOT).as_posix()
#: The program the configuration controls name: Git runs it and it records that it ran (in `ran`, beside it), then
#: fails, which Git reads as "read every file".
RECORDER = '#!/bin/sh\necho "$0 $*" >> "$(dirname "$0")/ran"\nexit 1\n'
#: The source each control edits, and the filter that would turn its edit back into the pinned blob.
EDITED, FILTER = "src/adp.c", "pin-control"


def answer(directory: Path, *args: str, stdin: str | None = None) -> str:
    """What a git command in `directory` prints; a failure refuses the control's setup."""
    res = git(directory, *args, stdin=stdin)
    if res.returncode:
        raise Refusal(f"an inherited-environment control's setup failed ({' '.join(args[:2])}): {res.stderr.strip()}")
    return res.stdout


@dataclass(frozen=True)
class Scene:
    """Where one control works: the stack clone, its pinned revision, and a directory of its own beside it."""

    stack: Path
    pin: str
    own: Path

    def edit(self) -> None:
        """The clone's EDITED with a line added."""
        source = self.stack / EDITED
        source.write_bytes(source.read_bytes() + b"\n")

    def edited(self) -> str:
        """EDITED with a line added, as text, from the pinned blob: the clone itself is left as it is."""
        return answer(self.stack, "cat-file", "blob", f"{self.pin}:{EDITED}") + "\n"

    def recorder(self) -> str:
        """The recorder program, in this control's own directory."""
        program = self.own / "recorder"
        program.write_text(RECORDER, encoding="utf-8")
        program.chmod(0o755)
        return str(program)

    def filtered(self, *config: str) -> None:
        """Check that the clean filter (FILTER, `config` naming its attribute or the filter) turns the edit back
        into the pinned blob, or the control would prove nothing."""
        size = len(answer(self.stack, "cat-file", "blob", f"{self.pin}:{EDITED}").encode())
        through = answer(self.stack, *config, "-c", f"filter.{FILTER}.clean=head -c {size}", "hash-object",
                         "--stdin", f"--path={EDITED}", stdin=self.edited()).strip()
        if through != answer(self.stack, "rev-parse", f"{self.pin}:{EDITED}").strip():
            raise Refusal("an inherited-environment control's clean filter does not give the pinned blob")


def repository(scene: Scene) -> dict[str, str]:
    """Another repository, whose HEAD and whose index's gitlink are a commit holding the edit."""
    other = scene.own / "repository"
    answer(scene.own, "clone", "--quiet", "--no-hardlinks", str(scene.stack), str(other))
    (other / EDITED).write_text(scene.edited(), encoding="utf-8")
    answer(other, "-c", "user.name=pin control", "-c", "user.email=pin-control@invalid", "commit", "--quiet",
           "--all", "--message=edited")
    commit = answer(other, "rev-parse", "HEAD").strip()
    answer(other, "update-index", "--add", "--cacheinfo", f"160000,{commit},{GITLINK}")
    return {"GIT_DIR": str(other / ".git")}


def index(scene: Scene) -> dict[str, str]:
    """An index whose gitlink is the stack's previous revision."""
    answer(scene.own, "init", "--quiet", "index")
    previous = answer(scene.stack, "rev-parse", f"{scene.pin}~1").strip()
    answer(scene.own / "index", "update-index", "--add", "--cacheinfo", f"160000,{previous},{GITLINK}")
    return {"GIT_INDEX_FILE": str(scene.own / "index/.git/index")}


def empty(scene: Scene) -> Path:
    """An empty repository's own directory."""
    answer(scene.own, "init", "--quiet", "empty")
    return scene.own / "empty/.git"


def alternate(scene: Scene) -> dict[str, str]:
    """A copy of the clone's objects."""
    store = scene.stack / ".git/objects"
    for entry in store.iterdir():
        if entry.name != "info":
            (shutil.copytree if entry.is_dir() else shutil.copy2)(entry, scene.own / "alternate" / entry.name)
    return {"GIT_ALTERNATE_OBJECT_DIRECTORIES": str(scene.own / "alternate")}


def unstored(scene: Scene) -> None:
    """The clone's own objects removed: its checkout and its HEAD stay."""
    for entry in (scene.stack / ".git/objects").iterdir():
        if entry.name != "info":
            (shutil.rmtree if entry.is_dir() else Path.unlink)(entry)


def swapped(scene: Scene) -> dict[str, str]:
    """Under another replacement base, the pinned src/ tree replaced by one holding the edit."""
    blob = answer(scene.stack, "hash-object", "-w", "--stdin", stdin=scene.edited()).strip()
    src = answer(scene.stack, "rev-parse", f"{scene.pin}:src").strip()
    entries = [f"{meta}\t{name}" if name != "adp.c" else f"{meta.rsplit(' ', 1)[0]} {blob}\t{name}"
               for meta, name in (e.split("\t", 1) for e in filter(None, answer(scene.stack, "ls-tree", "-z", src)
                                                                    .split("\0")))]
    new = answer(scene.stack, "mktree", "-z", stdin="\0".join(entries) + "\0").strip()
    answer(scene.stack, "update-ref", f"refs/swap/{src}", new)
    return {"GIT_REPLACE_REF_BASE": "refs/swap/"}


def configured(scene: Scene, how: str) -> dict[str, str]:
    """core.fsmonitor naming the recorder, through one way the environment gives Git configuration (`how`)."""
    program = scene.recorder()
    text = f"[core]\n\tfsmonitor = {program}\n"
    if how in ("GIT_CONFIG_GLOBAL", "GIT_CONFIG_SYSTEM"):
        (scene.own / "config").write_text(text, encoding="utf-8")
        return {how: str(scene.own / "config")}
    if how == "HOME":
        (scene.own / ".gitconfig").write_text(text, encoding="utf-8")
        return {"HOME": str(scene.own)}
    if how == "XDG_CONFIG_HOME":
        (scene.own / "git").mkdir()
        (scene.own / "git/config").write_text(text, encoding="utf-8")
        return {"XDG_CONFIG_HOME": str(scene.own)}
    if how == "GIT_CONFIG_PARAMETERS":
        return {how: f"'core.fsmonitor'='{program}'"}
    return {"GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "core.fsmonitor", "GIT_CONFIG_VALUE_0": program}


def filter_given(scene: Scene) -> dict[str, str]:
    """A clean filter given through GIT_CONFIG_COUNT, its attribute in the clone's own attributes."""
    (scene.stack / ".git/info/attributes").write_text(f"{EDITED} filter={FILTER}\n", encoding="utf-8")
    scene.filtered()
    size = len(answer(scene.stack, "cat-file", "blob", f"{scene.pin}:{EDITED}").encode())
    return {"GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": f"filter.{FILTER}.clean",
            "GIT_CONFIG_VALUE_0": f"head -c {size}"}


def attributes_given(scene: Scene) -> dict[str, str]:
    """A tree whose .gitattributes gives the edited source the clean filter, the filter in the clone's own
    configuration."""
    blob = answer(scene.stack, "hash-object", "-w", "--stdin", stdin=f"{EDITED} filter={FILTER}\n").strip()
    tree = answer(scene.stack, "mktree", stdin=f"100644 blob {blob}\t.gitattributes\n").strip()
    size = len(answer(scene.stack, "cat-file", "blob", f"{scene.pin}:{EDITED}").encode())
    answer(scene.stack, "config", f"filter.{FILTER}.clean", f"head -c {size}")
    scene.filtered(f"--attr-source={tree}")
    return {"GIT_ATTR_SOURCE": tree}


#: Each control: what it sets; the variables, from its own state (the clone's checkout and HEAD left as they
#: are); what is done to the clone; and the words its verdict must hold.
INHERITED: tuple[tuple[str, Callable[[Scene], dict[str, str]], Callable[[Scene], None], str], ...] = (
    ("GIT_DIR, a repository whose HEAD and gitlink are a commit holding the clone's edit", repository, Scene.edit,
     "differs from the pinned"),
    ("GIT_INDEX_FILE, an index whose gitlink is the revision the clone is checked out at", index,
     lambda s: answer(s.stack, "checkout", "--quiet", f"{s.pin}~1"), "is not the pinned"),
    ("GIT_WORK_TREE, another directory", lambda s: {"GIT_WORK_TREE": str(s.own)}, Scene.edit,
     "differs from the pinned"),
    ("GIT_COMMON_DIR, an empty repository's", lambda s: {"GIT_COMMON_DIR": str(empty(s))}, Scene.edit,
     "differs from the pinned"),
    ("GIT_OBJECT_DIRECTORY, an empty store", lambda s: {"GIT_OBJECT_DIRECTORY": str(empty(s) / "objects")},
     Scene.edit, "differs from the pinned"),
    ("GIT_ALTERNATE_OBJECT_DIRECTORIES, the clone's objects, which its own store no longer holds", alternate,
     unstored, "cannot read the pinned tree"),
    ("GIT_REPLACE_REF_BASE, a base under which the pinned src/ tree is replaced by one holding the edit", swapped,
     Scene.edit, "differs from the pinned"),
    ("GIT_CONFIG_COUNT, its key and value, core.fsmonitor naming a program", lambda s: configured(s, ""),
     Scene.edit, "differs from the pinned"),
    ("GIT_CONFIG_PARAMETERS, core.fsmonitor naming a program", lambda s: configured(s, "GIT_CONFIG_PARAMETERS"),
     Scene.edit, "differs from the pinned"),
    ("GIT_CONFIG_GLOBAL, a file whose core.fsmonitor names a program", lambda s: configured(s, "GIT_CONFIG_GLOBAL"),
     Scene.edit, "differs from the pinned"),
    ("GIT_CONFIG_SYSTEM, a file whose core.fsmonitor names a program", lambda s: configured(s, "GIT_CONFIG_SYSTEM"),
     Scene.edit, "differs from the pinned"),
    ("HOME, a directory whose .gitconfig names a program", lambda s: configured(s, "HOME"), Scene.edit,
     "differs from the pinned"),
    ("XDG_CONFIG_HOME, a directory whose git/config names a program", lambda s: configured(s, "XDG_CONFIG_HOME"),
     Scene.edit, "differs from the pinned"),
    ("GIT_CONFIG_COUNT, its key and value, a clean filter turning the edit back into the pinned blob",
     filter_given, Scene.edit, "differs from the pinned"),
    ("GIT_ATTR_SOURCE, a tree giving the edited source a clean filter that turns it back into the pinned blob",
     attributes_given, Scene.edit, "differs from the pinned"),
)


def judged_twice() -> tuple[bool, str]:
    """The audit hook's judge of the helper's environment given, as CPython 3.14's fork_exec gives it, a list of
    entries with GIT_NO_REPLACE_OBJECTS twice, the first 0, which is the one Git reads."""
    entries = [b"GIT_NO_REPLACE_OBJECTS=0", *(f"{key}={value}".encode() for key, value in GIT_ENVIRONMENT.items())]
    why = environment_judge(GIT_ENVIRONMENT)("_posixsubprocess.fork_exec", entries)
    return why is None, why or "no refusal"


def merged(into: dict[str, str], more: dict[str, str]) -> None:
    """`more`'s variables added to `into`, GIT_CONFIG_COUNT's entries after those `into` already holds."""
    first, count = int(into.get("GIT_CONFIG_COUNT", "0")), int(more.get("GIT_CONFIG_COUNT", "0"))
    for n in range(count):
        into[f"GIT_CONFIG_KEY_{first + n}"] = more[f"GIT_CONFIG_KEY_{n}"]
        into[f"GIT_CONFIG_VALUE_{first + n}"] = more[f"GIT_CONFIG_VALUE_{n}"]
    into.update({k: v for k, v in more.items() if not k.startswith(("GIT_CONFIG_COUNT", "GIT_CONFIG_KEY_",
                                                                    "GIT_CONFIG_VALUE_"))})
    if count:
        into["GIT_CONFIG_COUNT"] = str(first + count)


def inherited_arms(stack: Path, pin: str, work: Path,
                   run: Callable[[Path, dict[str, str]], tuple[int, str]]) -> list[tuple]:
    """The pin controls of the inherited environment, as ctrl_pin.pin_controls runs them (each after a fresh clone
    of the stack at `stack`, pinned at `pin`): each control of INHERITED, the pinned clone with every variable at
    once, and the judge given entries with a key twice. `run` runs the proof on a stack checkout with variables
    added to the environment it inherits: its exit status and output."""
    own = work / "inherited"
    given: dict[str, str] = {}

    def prepare(controls: tuple, spoiled: bool) -> None:
        """Each control's own directory afresh and its variables; then (`spoiled`) what it does to the clone."""
        if own.exists():
            shutil.rmtree(own)
        given.clear()
        for n, (_, variables, _, _) in enumerate(controls):
            (own / str(n)).mkdir(parents=True)
            merged(given, variables(Scene(stack, pin, own / str(n))))
        for _, _, spoil, _ in controls if spoiled else ():
            spoil(Scene(stack, pin, own / "0"))

    def verdict(needle: str) -> tuple[bool, str]:
        """The proof's verdict on the clone with the variables inherited: accepted at the pin, and its last word.
        A program the configuration names that Git ran fails the control, whatever the verdict."""
        rc, out = run(stack, dict(given))
        ran = sorted(own.rglob("ran"))
        if ran:
            return bool(needle), f"Git ran a program the inherited configuration names: " \
                                 f"{ran[0].read_text(encoding='utf-8').splitlines()[0]}"
        said = [ln.removeprefix("REFUSED: ") for ln in out.splitlines()
                if ln.startswith(("REFUSED: ", "tsn-c-stack at "))]
        detail = said[-1] if said else f"exit {rc}, no pin verdict: {out.strip()[-200:]}"
        return rc == 0 and detail == f"tsn-c-stack at {pin}", detail

    arms = [(f"the inherited environment, {control[0]}", lambda c=control: prepare((c,), True),
             lambda n=control[3]: verdict(n), control[3]) for control in INHERITED]
    return [*arms, ("the inherited environment, every variable above at once, the pinned clone",
                    lambda: prepare(INHERITED, False), lambda: verdict(""), ""),
            ("the audit hook's environment judge, fork_exec's entries with GIT_NO_REPLACE_OBJECTS twice",
             lambda: None, judged_twice, "not each a key given once")]
