# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_build.py - the build helpers of the control-plane firmware's host test.

The firmware is compiled from a Tree: the checkout, or a copy a planted defect
was written into (ctrl_mutants.py), with every object and executable under the
tree's own output directory, never in the checkout. The tests are GoogleTest
(sw/firmware/gtest/README.md): always compiled from the checkout's test
sources against the tree's headers, so a defect planted in a .c file reuses
every test object and one planted in a header rebuilds the tests that see it.

The ADP, ACMP and MAAP cores and the wire layer are the TSN stack's, from the
pinned tsn-c-stack submodule (#697): a tree names them, and the stack's own
core tests, with STACK_PREFIX, and builds them from its stack (the submodule,
or a copy a defect was planted in). The firmware includes only the stack's
public headers (its include/), and nothing of the stack includes the firmware
(ctrl_boundary.py).
"""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import stat
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from types import FrameType

HERE = Path(__file__).resolve().parent
CTRL = HERE.parent
ROOT = CTRL.parents[2]
HARNESS = ROOT / "sw/firmware/gtest"
sys.path.insert(0, str(HARNESS))

import fw_gtest  # noqa: E402

PP = ROOT / "protocol-processor"
PP_ADP_SIM = "tb/adp_engine/sim_main.cpp"
PP_ADP_PKG = PP / "hdl/adp/pp_adp_pkg.sv"
TB_MBX = ROOT / "tb/verilator/mbx"
TB_COMMON = ROOT / "tb/common"

#: The TSN stack: the tsn-c-stack submodule at its gitlink (#697).
STACK = ROOT / "third_party/tsn-c-stack"
#: A source or test named with this prefix is the stack's, the rest of the name
#: inside it; every other name is the ctrl tree's.
STACK_PREFIX = "tsn-c-stack/"
#: The stack's parts a tree builds from: its sources and its public headers. Its
#: tests are always the checkout's, as the ctrl tree's are.
STACK_PARTS = ("src", "include")
#: The stack's public headers, the only part of it the firmware includes.
STACK_INCLUDE = "include"
#: The stack's core tests and their fakes (acmp_fake.hpp), in the checkout.
STACK_TESTS = STACK / "tests"

#: The firmware every target links: the driver, the loop, the port layer, ADP, ACMP, the app.
#: The order is the link order of the measured images (ctrl_image.py, ctrl_srp_image.py).
PORTABLE = ("mbx/mbx.c", "loop/ctrl_loop.c", "port/ctrl_pool.c", "port/ctrl_debug.c", "port/shlan_port.c",
            "tsn-c-stack/src/adp.c", "adp/adp_mbx.c", "tsn-c-stack/src/maap.c", "maap/maap_mbx.c",
            "maap/maap_csr.c", "tsn-c-stack/src/acmp.c", "acmp/acmp_mbx.c", "acmp/acmp_nvm.c", "app/ctrl_app.c")
#: The host side: the model and mbx_hal.h on it. Test equipment, never measured.
HOST = ("host/mbx_model.c", "host/mbx_plat_host.c")
INCLUDE_DIRS = ("mbx", "host", "port", "loop", "adp", "maap", "acmp", "app", "test")
#: The saved-state store's state port (nvm_state.h), which acmp_nvm.c serves.
NVM_DIR = ROOT / "sw/firmware/ctrl_nvm"
C_FLAGS = ("-std=c11", "-O2", "-DNDEBUG", "-Wall", "-Wextra", "-Werror", "-pedantic")

RV32_FLAGS = ("-march=rv32i", "-mabi=ilp32", "-ffreestanding", "-fno-stack-protector", "-Os", "-DNDEBUG",
              "-std=c11", "-Wall",
              "-Wextra", "-Werror", "-pedantic", "-fstack-usage", "-DCTRL_MBX_BASE=0x80000000u")
#: Runtime interfaces an object-only check may leave undefined, including the
#: assertion handler when a debug build enables a protocol's re-entry guard.
RV32_LIBC = frozenset({"memset", "memcpy", "vsnprintf", "__assert_fail"})


class Refusal(Exception):
    """The gate cannot run as asked; exit 2, never a pass."""


@dataclass(frozen=True)
class Tree:
    """Where the firmware sources come from and where its builds go."""

    src: Path
    out: Path
    reuse: Path
    build: fw_gtest.Build = field(default_factory=lambda: fw_gtest.Build(jobs=4))
    #: the stack's root: its src/ and include/ (the submodule, or a planted copy)
    stack: Path = STACK


@dataclass(frozen=True)
class Outcome:
    """One arm's verdict and its output."""

    arm: str
    rc: int
    log: str


#: One subprocess, its output captured: the harness's runner, for the builders that import it from here. What
#: decides the pin may not reach it (ctrl_pin.census).
run = fw_gtest.run


def includes(tree: Tree) -> list[str]:
    """The firmware's include path, from the tree being built and its stack's public headers, then the harness."""
    return ([f"-I{tree.src / d}" for d in INCLUDE_DIRS] + [f"-I{tree.stack / STACK_INCLUDE}"] +
            [f"-I{NVM_DIR}", f"-I{HARNESS}"])


def compile_c(tree: Tree, sources: list[Path], tag: str, extra: tuple[str, ...] = (),
              measured: bool = True) -> list[Path]:
    """Compile C sources to objects under out/<tag>; a compile error refuses the arm."""
    try:
        return fw_gtest.compile_c(tree.build, C_FLAGS, [*includes(tree), *extra], sources, tree.out / tag, measured)
    except fw_gtest.BuildError as exc:
        raise Refusal(str(exc)) from exc


def firmware(tree: Tree, names: tuple[str, ...], tag: str) -> list[Path]:
    """The firmware sources `names` (measured) and the host model (not) as objects."""
    return (compile_c(tree, sources(tree, names), tag) +
            compile_c(tree, sources(tree, HOST), f"{tag}/host", measured=False))


def test_source(name: str) -> Path:
    """A test source of the checkout: the stack's tests/ for a STACK_PREFIX name, else this test/."""
    return STACK / name.removeprefix(STACK_PREFIX) if name.startswith(STACK_PREFIX) else HERE / name


def compile_tests(tree: Tree, names: tuple[str, ...], tag: str, extra: tuple[str, ...] = ()) -> list[Path]:
    """The GoogleTest sources `names` (from the checkout's test/, or the stack's tests/) against the
    tree's headers; the stack's test fakes (acmp_fake.hpp) are the checkout's too."""
    try:
        return fw_gtest.compile_tests(tree.build, [*includes(tree), f"-I{STACK_TESTS}", *extra],
                                      [test_source(n) for n in names], tree.out / tag)
    except fw_gtest.BuildError as exc:
        raise Refusal(str(exc)) from exc


def label(tree: Tree, text: str) -> Path:
    """The tally label of a binary whose test files name none: the stack's tests carry no FW_TALLY_LABEL."""
    try:
        return fw_gtest.label_object(tree.build, text, tree.out / "labels")
    except fw_gtest.BuildError as exc:
        raise Refusal(str(exc)) from exc


def link(tree: Tree, name: str, objects: list[Path]) -> Path:
    """Link objects with the harness's main into out/<name>."""
    try:
        main = fw_gtest.main_object(tree.build, tree.out / "harness")
        return fw_gtest.link(tree.build, [*objects, main], tree.out / name)
    except fw_gtest.BuildError as exc:
        raise Refusal(str(exc)) from exc


def execute(arm: str, exe: Path) -> Outcome:
    """Run one test binary and grade it as the sweep grades a suite log."""
    ok, log = fw_gtest.run_binary(exe)
    return Outcome(arm, 0 if ok else 1, log)


def source(src: Path, stack: Path, name: str) -> Path:
    """One firmware source: the stack's for a STACK_PREFIX name, else the ctrl tree's."""
    return stack / name.removeprefix(STACK_PREFIX) if name.startswith(STACK_PREFIX) else src / name


def sources(tree: Tree, names: tuple[str, ...]) -> list[Path]:
    """Paths of firmware sources inside the tree and its stack."""
    return [source(tree.src, tree.stack, n) for n in names]


#: The graft file every git command of the pin proof is given: a path under a file, which no directory can
#: be, so no graft file is ever read.
NO_GRAFTS = str(Path(os.devnull) / "no-grafts")
#: The whole environment of every git command of the pin proof, its allowlist: these settings and nothing of the
#: caller's, so no variable it inherits (GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE, GIT_OBJECT_DIRECTORY,
#: GIT_ALTERNATE_OBJECT_DIRECTORIES, GIT_REPLACE_REF_BASE, GIT_CONFIG_*, GIT_ATTR_*, HOME and the rest) can
#: redirect Git's repository, object store, configuration or replacement refs. Replacement objects (refs/replace)
#: are ignored, the graft file does not exist, and no configuration but the repository's own is read.
GIT_ENVIRONMENT = {"GIT_NO_REPLACE_OBJECTS": "1", "GIT_GRAFT_FILE": NO_GRAFTS, "GIT_CONFIG_NOSYSTEM": "1",
                   "GIT_CONFIG_GLOBAL": os.devnull}


def git_env() -> dict[str, str]:
    """The environment of every git command of the pin proof: GIT_ENVIRONMENT, so git reads the real objects
    only, and from no repository, object store or configuration the caller's environment names."""
    return dict(GIT_ENVIRONMENT)


@dataclass(frozen=True)
class GitRun:
    """What one git command of the pin proof printed, and its exit status."""

    returncode: int
    stdout: str
    stderr: str


#: The Git program the pin proof runs: the one PATH names when this module is loaded (None: PATH names none). The
#: helper starts it by this path, and the audit hook lets the helper start no other.
GIT = shutil.which("git")
#: What decides the pin: these functions of this module, and all they call.
DECISION = ("stack_gitlink", "stack_pin", "main")
#: The audit event a module of the pin proof raises to put its own code under the audit hook (ctrl_pin.py raises
#: it; this module's code is under it from the helper's definition on).
PROOF_EVENT = "ctrl_build.proof"
#: Every audit event of a process start that CPython raises, on any platform; and of a thread's start, since a
#: thread could change a process start's arguments after the hook has read them.
LAUNCH_EVENTS = frozenset({"subprocess.Popen", "os.system", "os.exec", "os.posix_spawn", "os.spawn", "os.fork",
                           "os.forkpty", "os.startfile", "pty.spawn", "webbrowser.open", "_posixsubprocess.fork_exec",
                           "_winapi.CreateProcess", "_thread.start_new_thread", "_thread.start_joinable_thread"})
#: The audit events of dynamic code (exec; compile, which exec and eval of a string raise too), and of what would
#: reach or change the hook's own state: the collector's lists of objects, and a trace or profile function, which
#: can rewrite a running frame's variables.
DYNAMIC_EVENTS = frozenset({"exec", "compile", "gc.get_objects", "gc.get_referrers", "gc.get_referents",
                            "sys.settrace", "sys.setprofile"})
#: The attributes of a function whose replacement changes what it runs.
RUNS = frozenset({"__code__", "__defaults__", "__kwdefaults__"})
#: What the audit hook writes on the standard error before each refusal it raises, so a refusal that is caught
#: and ignored is still read (ctrl_pin.exercised).
HOOK_REFUSED = "the pin proof's audit hook refused: "


class AuditRefusal(Refusal):
    """A refusal of the pin proof's audit hook (audited): the line of the proof that asked, and what it asked for."""


def environment_judge(own: dict[str, str]) -> Callable[[str, object], str | None]:
    """The audit hook's judge of the environment the helper starts Git with, binding as it is made, as the hook
    does, all it judges by (audited makes it when it installs the hook). An environment is the helper's when it is
    a plain dict (on CPython 3.14's fork_exec, the list of its entries, each key once) whose every key and value is
    a plain str, so that what Git is given is what was judged; when it sets GIT_NO_REPLACE_OBJECTS=1 and
    GIT_GRAFT_FILE to an absolute path under a file; and when it is `own` (GIT_ENVIRONMENT), key for key."""
    want, kind, text, raw, mapping, listed, decode, size = dict(own), type, str, bytes, dict, list, os.fsdecode, len
    stat_of, is_dir, failed = os.stat, stat.S_ISDIR, (OSError, ValueError)

    def judged(event: str, env: object) -> str | None:
        """Why the helper may not start Git (`event`) with `env` (None: it may)."""
        if kind(env) is listed:
            given = size(env)
            env = {decode(k): decode(v) for k, _, v in (e.partition(b"=") for e in env if kind(e) is raw)}
            if size(env) != given:
                return f"has the helper start Git ({event}) with an environment whose entries are not each a key " \
                       f"given once, so what Git is given is not what was judged"
        if kind(env) is not mapping:
            return f"has the helper start Git ({event}) without GIT_NO_REPLACE_OBJECTS=1, so Git would read a " \
                   f"replacement object"
        for key, value in env.items():
            if kind(key) is not text or kind(value) is not text:
                return f"has the helper start Git ({event}) with an environment whose keys and values are not all " \
                       f"plain str, so what Git is given is not what was judged"
        if env.get("GIT_NO_REPLACE_OBJECTS") != "1":
            return f"has the helper start Git ({event}) without GIT_NO_REPLACE_OBJECTS=1, so Git would read a " \
                   f"replacement object"
        graft = env.get("GIT_GRAFT_FILE")
        try:
            under = kind(graft) is text and graft.startswith("/") and not is_dir(stat_of(graft.rpartition("/")[0])
                                                                                .st_mode)
        except failed:
            under = False
        if not under:
            return f"has the helper start Git ({event}) with GIT_GRAFT_FILE {graft}, a path that can exist, so Git " \
                   f"would read a graft file"
        for key in [*env, *want]:
            if env.get(key) != want.get(key):
                return f"has the helper start Git ({event}) " + (f"without the pin proof's own {key}={want[key]}"
                                                                 if key in want else
                                                                 f"with {key} in its environment, which the pin "
                                                                 f"proof's own does not set")
        return None

    return judged


def audited(helper: Callable[..., GitRun]) -> Callable[..., GitRun]:
    """The helper, after installing beside it, before the pin proof's first Git call, the proof's audit hook (PEP
    578), which binds as it is installed all it judges by (THE HOOK, ctrl_pin.py). While the proof runs (a function
    of DECISION in any thread, or the top level of one of its modules), it refuses every process or thread start
    but the helper's: the subprocess module starting GIT, as a string, for the helper's own code, with exactly the
    proof's own environment (GIT_ENVIRONMENT, environment_judge). It refuses
    DYNAMIC_EVENTS and an import of importlib while a function of DECISION runs, or where the proof's own code (from
    its files, or in its namespaces) asks for them, the helper's included; and, at any time, a replacement of what
    a function of the proof runs (RUNS). Each refusal is an AuditRefusal naming the proof's line that asked."""
    proof, code, program, decision, starts, dynamic = [helper.__globals__], helper.__code__, GIT, DECISION, \
        LAUNCH_EVENTS, DYNAMIC_EVENTS
    files = frozenset({code.co_filename, f"{HERE}/ctrl_build.py", f"{HERE}/ctrl_pin.py",
                       f"{code.co_filename.rpartition('/')[0]}/ctrl_pin.py"})
    runs, joined, said, refusal, root = RUNS, PROOF_EVENT, HOOK_REFUSED, AuditRefusal, f"{ROOT}/"
    frame_at, frames, write, decode, judged = sys._getframe, sys._current_frames, os.write, os.fsdecode, \
        environment_judge(GIT_ENVIRONMENT)
    kind, text, raw, ordered, function = type, str, bytes, tuple, type(helper)

    def ours(frame: FrameType) -> bool:
        """Whether `frame` runs the code of a module of the pin proof: from its files, or in its namespaces."""
        if frame.f_code.co_filename in files:
            return True
        for namespace in proof:
            if frame.f_globals is namespace:
                return True
        return False

    def running(loading: bool) -> bool:
        """Whether, in any thread, a function of DECISION runs (or, `loading`, a proof module's top level)."""
        for frame in frames().values():
            while frame is not None:
                if (frame.f_code.co_name in decision and frame.f_globals is proof[0]) or \
                        (loading and frame.f_code.co_name == "<module>" and ours(frame)):
                    return True
                frame = frame.f_back
        return False

    def refuse(frame: FrameType, what: str) -> None:
        """Refuse `what`, asked at the proof's innermost line on `frame`'s stack (`frame`'s own, if none)."""
        at = frame
        while at is not None and not ours(at):
            at = at.f_back
        at = frame if at is None else at
        message = f"{at.f_code.co_filename.removeprefix(root)}:{at.f_lineno} {what}"
        write(2, f"{said}{message}\n".encode(errors="backslashreplace"))
        raise refusal(message)

    def unlike(event: str, args: tuple, frame: FrameType) -> str | None:
        """Why a process start while the proof runs is not the helper's (None: it is)."""
        caller = frame
        while caller is not None and caller.f_globals.get("__name__") == "subprocess":
            caller = caller.f_back
        forked = event == "_posixsubprocess.fork_exec"
        if caller is None or caller.f_code is not code or event not in ("subprocess.Popen", "os.posix_spawn") and \
                not forked:
            first = args[1] if event == "os.spawn" else args[0] if args else "a copy of this interpreter"
            shown = " or ".join(decode(f) for f in first) if forked else decode(first) if kind(first) in (text, raw) \
                else first
            return f"starts {shown} ({event}) while the pin proof runs, not by the helper"
        given, env = args[0], args[2] if event != "subprocess.Popen" else args[3]
        if not (kind(given) is text and given == program) and not (forked and kind(given) is ordered and
                                                                      {decode(g) for g in given} == {program}):
            return f"has the helper start {given} ({event}), not the Git program PATH names, {program}"
        return judged(event, env)

    def hook(event: str, args: tuple) -> None:
        """The pin proof's audit hook."""
        if event == joined:
            proof.append(frame_at(1).f_globals)
        elif event in starts:
            if running(True) and (why := unlike(event, args, frame_at(1))):
                refuse(frame_at(1), why)
        elif event in dynamic or event == "import" and kind(args[0]) is text and \
                (args[0] == "importlib" or args[0].startswith("importlib.")):
            if ours(frame_at(1)) or running(False):
                asked = f"an import of {args[0]}" if event == "import" else event
                refuse(frame_at(1), f"asks for {asked} in the pin proof: dynamic code, or a reach into the audit "
                                    f"hook's own state")
        elif event == "object.__setattr__" and kind(args[0]) is function and args[1] in runs:
            for namespace in proof:
                if args[0].__globals__ is namespace:
                    refuse(frame_at(1), f"replaces {args[1]} of {args[0].__qualname__}, a function of the pin proof")

    sys.addaudithook(hook)
    return helper


@audited
def git(directory: Path, *args: str, stdin: str | None = None) -> GitRun:
    """One git command in `directory`, its output captured: the helper, the only code of the pin proof's modules
    (this one and ctrl_pin.py) that names a process-launch facility, and the only one whose process the pin
    proof's audit hook lets start while the proof runs (audited): GIT, with git_env's environment, the whole of it."""
    import subprocess
    res = subprocess.run(["git", "-C", str(directory), *args], executable=GIT, input=stdin, capture_output=True,
                         check=False, env=git_env(), encoding="utf-8", errors="surrogateescape")
    return GitRun(res.returncode, res.stdout, res.stderr)


def stack_gitlink(root: Path = ROOT) -> str:
    """The tsn-c-stack revision the repository at `root` records: one stage-0 gitlink, or a Refusal."""
    rel = STACK.relative_to(ROOT).as_posix()
    entry = git(root, "ls-files", "--stage", "--", rel).stdout.split()
    if len(entry) != 4 or entry[0] != "160000" or entry[2] != "0":
        raise Refusal(f"{rel} is not one stage-0 gitlink")
    return entry[1]


def blob_id(path: Path, algorithm: str) -> str:
    """The object id git gives `path`'s content as a blob (a symbolic link's is its target), hashed here from
    the file's own bytes: never read from an index, and through no attribute or filter."""
    data = os.readlink(path).encode() if path.is_symlink() else path.read_bytes()
    return hashlib.new(algorithm, b"blob %d\0" % len(data) + data).hexdigest()


def on_disk(stack: Path, algorithm: str) -> dict[str, tuple[str, str, str]]:
    """Every entry of the stack's checkout but its own .git, as a tree records it (mode, type, blob id): a
    directory is a tree, a symbolic link a blob of its target, a file a blob of its bytes, executable when its
    owner may execute it; anything else is of no type a tree holds."""
    found = {}
    for here, dirs, files in os.walk(stack):
        if Path(here) == stack:
            dirs[:] = [d for d in dirs if d != ".git"]
            files = [f for f in files if f != ".git"]
        for name in dirs + files:
            path = Path(here) / name
            rel, mode = path.relative_to(stack).as_posix(), path.lstat().st_mode
            if stat.S_ISLNK(mode):
                found[rel] = ("120000", "blob", blob_id(path, algorithm))
            elif stat.S_ISDIR(mode):
                found[rel] = ("040000", "tree", "")
            elif stat.S_ISREG(mode):
                found[rel] = ("100755" if mode & stat.S_IXUSR else "100644", "blob", blob_id(path, algorithm))
            else:
                found[rel] = ("", "", "")
    return found


def stack_pin(stack: Path = STACK, pin: str | None = None) -> str:
    """Refuse a stack checkout that is not at the recorded gitlink, or that is not the gitlink's whole tree:
    the same paths, each of the same type and mode, every file and symbolic link hashed as git hashes a blob
    and equal to the tree's. git reads the real objects only (git_env), so a replacement or a graft changes
    nothing it reads; and the index is never consulted, so an edit hidden from `git status` (assume-unchanged,
    skip-worktree) is refused like any other: every gate builds the pinned stack or none."""
    pin = pin or stack_gitlink()
    top = git(stack, "rev-parse", "--show-toplevel")
    if top.returncode or Path(top.stdout.strip()).resolve() != stack.resolve():
        raise Refusal(f"{stack} is not its own checkout: initialise the tsn-c-stack submodule")
    head = git(stack, "rev-parse", "HEAD").stdout.strip()
    if head != pin:
        raise Refusal(f"tsn-c-stack at {head or 'no HEAD'} is not the pinned {pin}")
    algorithm = git(stack, "rev-parse", "--show-object-format").stdout.strip()
    tree = git(stack, "ls-tree", "-r", "-t", "-z", "--full-tree", pin)
    if tree.returncode or algorithm not in hashlib.algorithms_available:
        raise Refusal(f"cannot read the pinned tree {pin[:8]} of {stack}: {tree.stderr.strip()}")
    want = {}
    for entry in filter(None, tree.stdout.split("\0")):
        meta, name = entry.split("\t", 1)
        mode, kind, oid = meta.split()
        want[name] = (mode, kind, "" if kind == "tree" else oid)
    found = on_disk(stack, algorithm)
    differ = sorted(name for name in want.keys() | found.keys() if want.get(name) != found.get(name))
    if differ:
        raise Refusal(f"tsn-c-stack differs from the pinned {pin[:8]}: {', '.join(differ)}")
    return head


#: Where each stack file lived in sw/firmware/ctrl before #697 moved the cores
#: into the submodule (the file map of the stack's import record). A tree of an
#: older revision (ctrl_image.py --base, ctrl_srp_image.py --ctrl-source) still
#: holds them there.
LEGACY = {"src/adp.c": "adp/adp.c", "src/acmp.c": "acmp/acmp.c", "src/maap.c": "maap/maap.c",
          "include/adp.h": "adp/adp.h", "include/acmp.h": "acmp/acmp.h", "include/maap.h": "maap/maap.h",
          "include/wire.h": "wire/wire.h"}


def legacy_stack(ctrl: Path, into: Path) -> Path | None:
    """For a ctrl tree from before #697, which holds its own cores, a copy of them in the stack's layout
    under `into`; None for a tree that holds none. An older tree holds fewer (no ACMP before lane F3), and
    a source the copy lacks is one its tree lacks."""
    held = {new: old for new, old in LEGACY.items() if (ctrl / old).is_file()}
    if not held:
        return None
    for new, old in held.items():
        (into / new).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ctrl / old, into / new)
    return into


def main(argv: list[str] | None = None) -> int:
    """The pin check from a command line, for the gates that are not Python (the mailbox bench's Makefile):
    exit 0 with the pinned revision, or 2 with the refusal."""
    ap = argparse.ArgumentParser(description="Refuse a tsn-c-stack checkout off its gitlink or differing from it.")
    ap.add_argument("--stack-pin", type=Path, nargs="?", const=STACK, required=True, metavar="DIR",
                    help="the stack checkout a gate builds (default: the submodule)")
    args = ap.parse_args(argv)
    try:
        print(f"tsn-c-stack at {stack_pin(args.stack_pin.resolve())}")
    except Refusal as exc:
        print(f"REFUSED: {exc}")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
