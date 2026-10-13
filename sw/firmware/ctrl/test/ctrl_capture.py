#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_capture.py - the firmware builders' compiler invocations, recorded as they run (#697).

THE CAPTURE. `ctrl_capture.py --out DIR -- COMMAND...` runs COMMAND with a
directory of recording wrappers (DIR/bin) first on PATH: one for every C or
C++ compiler name the PATH holds (gcc, g++, cc, c++, cpp, clang, clang++, and
their prefixed and versioned names), one for the RV32 compiler (MILAN_RV32_CC
names it, its sibling tools beside it), and one for CC and CXX where they are
set. Each wrapper runs the recorder (ctrl_shim.RECORDER, compiled into DIR/bin
with the real C compiler), which has the real compiler expand the invocation
(ctrl_expand, THE EXPANSION: its own report of the macros, the directories and
the files read first its arguments give) and list what each source's compile
reads (ctrl_shim, THE DEPENDENCY PASS), records it, and then runs the real
compiler with the same arguments, so every object, binary and image is what it
would be without the capture. Python processes it starts load an audit hook
(DIR/hook/sitecustomize.py) that names, for every process they start, the
checkout's files on their Python stack, and records any compiler a builder
runs by a path no wrapper stands on (a compile the capture would miss), so the
boundary can refuse it. Runs append to the same DIR; DIR/manifest.jsonl lists
each command, its directory and its exit status. The exit status is the
command's.

THE READER. load(DIR) gives every invocation the capture holds, each with the
compiler's own expansion of it (Expansion, read from the kept report), each
source's dependency list (Deps, read from the kept list, or why the recorder
has none) and the builders it came from: the checkout's files on the Python
stack of the process that ran the compiler, and the script or Makefile of the
command the capture ran (CTRL_CAPTURE_RUN, which run() sets and every process
below inherits), which is also kept apart as the run it came from: a builder
another builder runs is among the builders of its compiles, never their run.

Usage:
    python3 sw/firmware/ctrl/test/ctrl_capture.py --out DIR -- python3 sw/firmware/ctrl/test/test_ctrl_firmware.py
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from functools import cached_property, lru_cache
from pathlib import Path

import ctrl_expand
import ctrl_shim

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
#: The recorder's name in a capture's bin/.
RECORDER = ".ctrl-recorder"
#: A C or C++ compiler's name, prefixed with a target's name or suffixed with a version (-13), or neither.
COMPILER = re.compile(r"^(?:[\w.+-]+-)?(?:gcc|g\+\+|c\+\+|cc|cpp|clang|clang\+\+)(?:-\d+(?:\.\d+)*)?$")
#: The audit hook every Python process of a capture loads: it names the builders on the stack of each process
#: it starts (CTRL_CAPTURE_FROM, after its own parent's), and records a compiler run by a path that is no
#: wrapper. It then loads the sitecustomize it shadows, if there is one.
HOOK = r'''"""The capture's audit hook (ctrl_capture.py), generated for one capture."""
import json as _json
import os as _os
import re as _re
import sys as _sys

_ROOT = _os.environ.get("CTRL_CAPTURE_ROOT", "")
_BIN = _os.environ.get("CTRL_CAPTURE_BIN", "")
_DIR = _os.environ.get("CTRL_CAPTURE_DIR", "")
_PARENT = _json.loads(_os.environ.get("CTRL_CAPTURE_FROM") or "[]")
_COMPILER = _re.compile(%(compiler)r)


def _builders():
    found = list(_PARENT)
    frame = _sys._getframe(2)
    while frame is not None:
        name = frame.f_code.co_filename
        if name.startswith(_ROOT + "/") and name[len(_ROOT) + 1:] not in found:
            found.append(name[len(_ROOT) + 1:])
        frame = frame.f_back
    return _json.dumps(found)


def _bypass(program, argv, env, builders):
    if not program or not _COMPILER.match(_os.path.basename(str(program))):
        return
    path = str(program)
    if "/" not in path:
        import shutil as _shutil
        path = _shutil.which(path, path=(env if env is not None else _os.environ).get("PATH")) or ""
        if not path:
            return
    if _os.path.dirname(_os.path.abspath(path)) == _BIN:
        return
    line = _json.dumps({"bypass": path, "args": [str(a) for a in argv or ()], "cwd": _os.getcwd(),
                        "from": builders}) + "\n"
    fd = _os.open(_os.path.join(_DIR, "records.jsonl"), _os.O_WRONLY | _os.O_APPEND | _os.O_CREAT, 0o644)
    try:
        _os.write(fd, line.encode("utf-8"))
    finally:
        _os.close(fd)


def _hook(event, args):
    if event not in ("subprocess.Popen", "os.posix_spawn", "os.exec", "os.spawn", "os.system"):
        return
    if event != "subprocess.Popen" and _sys._getframe(1).f_code.co_filename.endswith("subprocess.py"):
        return
    builders = _builders()
    if event == "os.system":
        env, program, argv = None, None, ()
    elif event == "subprocess.Popen":
        program, argv, env = args[0], args[1], args[3]
        if isinstance(argv, (str, bytes)):
            argv = [argv]
        if program is None and argv:
            program = argv[0]
    else:
        program, argv, env = args[0], args[1], args[2] if len(args) > 2 else None
    _bypass(program, argv, env, builders)
    if env is None:
        _os.environ["CTRL_CAPTURE_FROM"] = builders
    else:
        try:
            env["CTRL_CAPTURE_FROM"] = builders
        except TypeError:
            pass


if _ROOT and _DIR:
    _sys.addaudithook(_hook)

_HERE = _os.path.dirname(_os.path.abspath(__file__))
import importlib.machinery as _machinery  # noqa: E402
import importlib.util as _util  # noqa: E402
_spec = _machinery.PathFinder.find_spec("sitecustomize", [p for p in _sys.path if _os.path.abspath(p or ".") != _HERE])
if _spec is not None and _spec.loader is not None:
    _module = _util.module_from_spec(_spec)
    _spec.loader.exec_module(_module)
''' % {"compiler": COMPILER.pattern}


class CaptureError(Exception):
    """The capture cannot be made or read as asked."""


def path_without(bin_dir: Path) -> str:
    """PATH with the capture's wrappers taken out."""
    return os.pathsep.join(p for p in os.environ.get("PATH", "").split(os.pathsep)
                           if p and Path(p).resolve() != bin_dir.resolve())


def wrapper(bin_dir: Path, name: str, real: str, capture: Path) -> Path:
    """One recording wrapper: the recorder (ctrl_shim.RECORDER), then the real compiler."""
    path = bin_dir / name
    words = [str(bin_dir / RECORDER), str(capture), name, real]
    path.write_text("#!/bin/sh\nexec " + " ".join(shlex.quote(w) for w in words) + ' "$@"\n', encoding="utf-8")
    path.chmod(0o755)
    return path


def recorder(bin_dir: Path, compilers: dict[str, str]) -> None:
    """The recorder, compiled into bin/ with the real C compiler, unless the one there is of this text."""
    source, binary = bin_dir / f"{RECORDER}.c", bin_dir / RECORDER
    if binary.is_file() and source.is_file() and source.read_text(encoding="utf-8") == ctrl_shim.RECORDER:
        return
    cc = compilers.get("cc") or compilers.get("gcc")
    if cc is None:
        raise CaptureError("no C compiler on PATH to build the capture's recorder with")
    part = bin_dir / f"{RECORDER}.{os.getpid()}"
    text = part.with_name(part.name + ".c")
    text.write_text(ctrl_shim.RECORDER, encoding="utf-8")
    res = subprocess.run([cc, "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-o", str(part), str(text)],
                         capture_output=True, text=True, check=False)
    if res.returncode:
        raise CaptureError(f"the capture's recorder does not compile: {res.stderr.strip()}")
    os.replace(text, source)
    os.replace(part, binary)


def rv32_compiler() -> str | None:
    """The RV32 compiler the builders would take (fw_rv32.compiler), before the capture wraps it."""
    sys.path.insert(0, str(ROOT / "sw/firmware/gtest"))
    import fw_rv32  # noqa: PLC0415 - the RV32 choice is fw_rv32's own
    return fw_rv32.compiler()


#: The environment of each capture installed by this process, made once (its runs may start at once).
INSTALLED: dict[Path, dict[str, str]] = {}
INSTALLING = threading.Lock()


def install(capture: Path) -> dict[str, str]:
    """The capture's wrappers and hook, written once per process; the environment a command runs under."""
    capture = capture.resolve()
    with INSTALLING:
        if capture not in INSTALLED or not (capture / "hook" / "sitecustomize.py").is_file():
            INSTALLED[capture] = installed(capture)
        return dict(INSTALLED[capture])


def installed(capture: Path) -> dict[str, str]:
    """The capture's wrappers (a sibling of the RV32 compiler that is no compiler, linked as it is) and hook."""
    bin_dir, hook = capture / "bin", capture / "hook"
    for part in (bin_dir, hook, capture / "text", capture / "expand" / "in", capture / "deps"):
        part.mkdir(parents=True, exist_ok=True)
    # the capture's start: a file whose inode changed since was written by a run of the capture (ctrl_shim's own)
    if not (capture / "start").is_file():
        (capture / "start").write_text(f"{time.time_ns()}\n", encoding="utf-8")
    search = path_without(bin_dir)
    env = {**os.environ, "PATH": search}
    rv32 = rv32_compiler()
    wrapped: dict[str, str] = {}
    for folder in search.split(os.pathsep):
        if not Path(folder).is_dir():
            continue
        for entry in sorted(Path(folder).iterdir()):
            if COMPILER.match(entry.name) and entry.name not in wrapped and os.access(entry, os.X_OK) and \
                    entry.is_file():
                wrapped[entry.name] = str(entry)
    recorder(bin_dir, wrapped)
    for name, real in wrapped.items():
        wrapper(bin_dir, name, real, capture)
    if rv32 is not None:
        real = Path(rv32)
        prefix = real.name.removesuffix("gcc")
        for sibling in sorted(real.parent.iterdir()):
            if not sibling.name.startswith(prefix) or sibling.name in wrapped:
                continue
            target = bin_dir / sibling.name
            if COMPILER.match(sibling.name):
                wrapper(bin_dir, sibling.name, str(sibling), capture)
            elif not target.is_symlink():
                target.symlink_to(sibling)
        env["MILAN_RV32_CC"] = str(bin_dir / real.name)
    for var in ("CC", "CXX"):
        if os.environ.get(var):
            real = shutil.which(os.environ[var], path=search)
            if real is None:
                raise CaptureError(f"{var}={os.environ[var]} is no program")
            name = Path(real).name
            if wrapped.get(name, real) != real:
                raise CaptureError(f"{var}={os.environ[var]} shadows another {name}")
            env[var] = str(wrapper(bin_dir, name, real, capture))
    (hook / "sitecustomize.py").write_text(HOOK, encoding="utf-8")
    env.update({"PATH": os.pathsep.join([str(bin_dir), search]), "CTRL_CAPTURE_DIR": str(capture),
                "CTRL_CAPTURE_START": str(capture / "start"), "CTRL_CAPTURE_PYTHON": sys.executable,
                "CTRL_CAPTURE_EXPAND": str(HERE / "ctrl_expand.py"),
                "CTRL_CAPTURE_BIN": str(bin_dir), "CTRL_CAPTURE_ROOT": str(ROOT), "CTRL_CAPTURE_FROM": "",
                "PYTHONPATH": os.pathsep.join(p for p in (str(hook), os.environ.get("PYTHONPATH", "")) if p)})
    return env


def run(capture: Path, argv: list[str], cwd: Path | None = None, env_extra: dict[str, str] | None = None,
        **kwargs) -> subprocess.CompletedProcess:
    """One command under the capture, listed in its manifest; its records name the command's builder file
    (CTRL_CAPTURE_RUN: its Python script or its Makefile, when one of the checkout's)."""
    env = {**install(capture), **(env_extra or {}),
           "CTRL_CAPTURE_RUN": json.dumps(script_of(str((cwd or Path.cwd()).resolve()), argv))}
    start = time.monotonic()
    res = subprocess.run(argv, cwd=cwd, env=env, check=False, **kwargs)
    line = json.dumps({"argv": argv, "cwd": str(cwd or Path.cwd()), "rc": res.returncode,
                       "seconds": round(time.monotonic() - start, 1)}) + "\n"
    with (capture.resolve() / "manifest.jsonl").open("a", encoding="utf-8") as out:
        out.write(line)
    return res


# ---- the reader -------------------------------------------------------------------------------


@dataclass(frozen=True)
class Baseline:
    """The same driver's expansion with no argument, in one language: what the implementation predefines (name,
    parameters, replacement), and the files it reads and the directories it searches on its own (resolved)."""

    builtins: tuple[tuple[str, str, str], ...]
    own: frozenset[str]


@dataclass(frozen=True)
class Expansion:
    """The compiler's own expansion of one invocation (ctrl_expand, THE EXPANSION): why it is no expansion ("" when
    it is one), its translation units, every directory it searched (resolved, the baseline's left out), every file
    it entered and every real input it read (a precompiled header's maker's), each as printed with its resolved
    path, digest and whether it is an installed tool's, every precompiled header it read first (as printed, and
    resolved), and the baseline of each of its languages."""

    digest: str
    error: str
    units: tuple[ctrl_expand.Unit, ...]
    dirs: tuple[str, ...]
    entered: tuple[tuple[str, str, str, bool], ...]
    mains: tuple[tuple[str, str, str, bool], ...]
    pch: tuple[tuple[str, str], ...]
    baseline: tuple[tuple[str, Baseline], ...]

    def base(self, language: str) -> Baseline | None:
        """The baseline in a language."""
        return dict(self.baseline).get(language)


@dataclass(frozen=True)
class Deps:
    """What one source's compile reads, as its dependency pass listed it (ctrl_shim, THE DEPENDENCY PASS): every
    file but the source itself, resolved, and the tree of those its own #include lines read, each at its depth
    with its index in `files` (-1 for the source)."""

    files: tuple[str, ...]
    tree: tuple[tuple[int, int], ...]

    def edges(self, source: str) -> list[tuple[str, str]]:
        """Every (includer, file) the tree holds: each file with the file whose #include line read it there."""
        found: list[tuple[str, str]] = []
        stack = [source]
        for depth, index in self.tree:
            del stack[depth:]
            path = source if index < 0 else self.files[index]
            found.append((stack[-1], path))
            stack.append(path)
        return found


@dataclass(frozen=True)
class Source:
    """One input of a recorded compile: its path (resolved), the language the compiler's expansion gave it ("other"
    for a linker input), and, for a source it compiles, its dependency list, or why the recorder has none."""

    path: str
    lang: str
    deps: Deps | None
    error: str


@dataclass(frozen=True)
class Invocation:
    """One recorded compile: the name it was called by, its arguments and directory, each input (Source), the
    compiler's expansion of it (None when it names no input, which compiles nothing, or, with `failed` saying why,
    when the capture could not have it made), the expansions of the compiles that made each precompiled header it
    read first, the checkout's builder files it came from, the compile's exit status, and the builder file of the
    command the capture ran that it came from (its run)."""

    tool: str
    args: tuple[str, ...]
    cwd: str
    sources: tuple[Source, ...]
    expansion: Expansion | None
    failed: str
    first: tuple[Expansion, ...]
    builders: frozenset[str]
    rc: int = 0
    run: frozenset[str] = frozenset()


@dataclass(frozen=True)
class Capture:
    """A capture: where its texts are kept, its commands, its invocations, and the compiles that bypassed it;
    and, for captures joined by +, the parts it was joined from (so what is read from each is read once)."""

    stores: tuple[Path, ...]
    commands: tuple[dict, ...]
    invocations: tuple[Invocation, ...]
    bypassed: tuple[dict, ...]
    parts: tuple[Capture, ...] = ()

    def text(self, digest: str) -> str:
        """A kept text."""
        for store in self.stores:
            if (store / "text" / digest).is_file():
                return (store / "text" / digest).read_bytes().decode("utf-8", "replace")
        raise CaptureError(f"no capture keeps the text {digest}")

    @cached_property
    def builders(self) -> frozenset[str]:
        """Every builder file some invocation came from."""
        if self.parts:
            return frozenset().union(*(part.builders for part in self.parts))
        return frozenset().union(*(inv.builders for inv in self.invocations))

    @cached_property
    def ran(self) -> frozenset[str]:
        """Every builder file whose own command, run by the capture, made some invocation."""
        if self.parts:
            return frozenset().union(*(part.ran for part in self.parts))
        return frozenset().union(*(inv.run for inv in self.invocations))

    @property
    def leaves(self) -> tuple[Capture, ...]:
        """The captures this one was joined from, or itself."""
        return self.parts or (self,)

    def __add__(self, other: Capture) -> Capture:
        """Two captures as one."""
        return Capture(self.stores + other.stores, self.commands + other.commands,
                       self.invocations + other.invocations, self.bypassed + other.bypassed,
                       self.leaves + other.leaves)


def script_of(cwd: str, argv: list[str]) -> list[str]:
    """The checkout's builder files a command names: a Python process's script, a make's Makefile."""
    if not argv:
        return []
    program = Path(argv[0]).name
    found: list[Path] = []
    if program.startswith("python"):
        at = 1
        while at < len(argv) and argv[at].startswith("-") and argv[at] not in ("-c", "-m", "-"):
            at += 2 if argv[at] in ("-X", "-W") else 1
        if at < len(argv) and not argv[at].startswith("-"):
            found.append(Path(cwd) / argv[at])
    elif program in ("make", "gmake") or program.endswith("make") and program != "cmake":
        where, files = Path(cwd), []
        at = 1
        while at < len(argv):
            arg = argv[at]
            if arg in ("-C", "--directory") and at + 1 < len(argv):
                where = where / argv[at + 1]
                at += 1
            elif arg.startswith("-C") and len(arg) > 2:
                where = where / arg[2:]
            elif arg in ("-f", "--file", "--makefile") and at + 1 < len(argv):
                files.append(argv[at + 1])
                at += 1
            elif arg.startswith("-f") and len(arg) > 2:
                files.append(arg[2:])
            at += 1
        found += [where / f for f in files] or [where / n for n in ("GNUmakefile", "makefile", "Makefile")
                                                 if (where / n).is_file()][:1]
    return [p.resolve().relative_to(ROOT).as_posix() for p in found if p.resolve().is_relative_to(ROOT)]


@lru_cache(maxsize=None)
def resolved(cwd: str, name: str) -> str:
    """A path a compile named, from its directory, resolved as the recorder resolves it."""
    return str((Path(cwd) / name).resolve())


def baseline(report: dict) -> Baseline:
    """A baseline report, read: its first unit's built-ins, and every file it entered and directory it searched."""
    seen = ctrl_expand.read(report["out"], report["err"])
    cwd = report["cwd"]
    own = {found[0] for found in report["entered"].values()}
    own |= {resolved(cwd, d) for d in (*seen.quote, *seen.bracket)}
    return Baseline(seen.units[0].builtins if seen.units else (), frozenset(own))


def expansion(digest: str, text: Callable[[str], str]) -> Expansion:
    """An expansion's kept report, read (`text` reads a kept text): its units, the directories it searched but the
    baseline's, the files it entered, its baselines, and ctrl_expand.refusal's reason when it is no expansion."""
    report = json.loads(text(digest))
    seen = ctrl_expand.read(report["out"], report["err"])
    bases = {language: baseline(json.loads(text(d))) for language, d in sorted(report["baseline"].items())}
    own = frozenset().union(*(b.own for b in bases.values())) if bases else frozenset()
    dirs = tuple(d for d in dict.fromkeys(resolved(report["cwd"], d) for d in (*seen.quote, *seen.bracket))
                 if d not in own)
    entered = tuple((printed, *found) for printed, found in sorted(report["entered"].items()))
    mains = tuple((printed, *found) for printed, found in sorted(report["mains"].items()))
    return Expansion(digest, ctrl_expand.refusal(report, seen), seen.units, dirs, entered, mains,
                     tuple(sorted(report["pch"].items())), tuple(bases.items()))


def deps(text: str) -> Deps:
    """A kept dependency list, read."""
    kept = json.loads(text)
    files = tuple(sys.intern(path) for path in kept["deps"])
    tree = tuple((int(depth), int(index)) for depth, index in kept["tree"])
    if any(depth < 1 or not -1 <= index < len(files) for depth, index in tree):
        raise ValueError("a dependency tree names a file its list does not hold")
    return Deps(files, tree)


def invocation(raw: dict, listed: Callable[[str], Deps], expanded: Callable[[str], Expansion],
               made_by: dict[str, tuple[Expansion, tuple[str, ...]]]) -> Invocation:
    """One record, read: its builders are the Python stack's that started it and the builder file of the command
    the capture ran (THE CAPTURE); each source's dependency list is a kept text (`listed` reads one), and so is
    the report of the compiler's expansion of it (`expanded` reads one). Each precompiled header it read first is
    the expansion of the compile the capture holds that made it (`made_by`, by output, the records before it), and
    what that compile read (its header and the files its list holds) is read by this one too: a dependency pass
    that reads the precompiled header, as the compile does, lists none of it (ctrl_shim, THE DEPENDENCY PASS)."""
    run = frozenset(json.loads(raw.get("run") or "[]"))
    builders = set(json.loads(raw.get("from") or "[]")) | run
    made = expanded(raw["expansion"]) if raw["expansion"] else None
    # an invocation naming no input compiles nothing, and the recorder expands nothing of it
    failed = raw["expand_error"] or ("" if made is not None or not raw["expanded"] else
                                     "the recorder holds no expansion of it")
    first, header = [], []
    for _, where in made.pch if made is not None else ():
        if where not in made_by:
            failed = failed or f"it reads the precompiled header {where} first, which no compile the capture holds made"
        else:
            first.append(made_by[where][0])
            header += made_by[where][1]
    if "rc" not in raw or any(len(entry) != 4 for entry in raw["sources"]):
        raise ValueError("a recorder that lists no dependencies made it: capture again")
    sources = []
    for path, lang, digest, error in raw["sources"]:
        deps = listed(digest) if digest else None
        if deps is not None and header:
            deps = Deps(deps.files + tuple(f for f in dict.fromkeys(header) if f not in deps.files), deps.tree)
        sources.append(Source(path, lang, deps, error))
    if made is not None and raw.get("output"):
        read = tuple(f for s in sources if s.deps is not None for f in (s.path, *s.deps.files))
        made_by[raw["output"]] = (made, read)
    return Invocation(raw["tool"], tuple(raw["args"]), raw["cwd"], tuple(sources), made, failed, tuple(first),
                      frozenset(builders), int(raw["rc"]), run)


def load(where: Path, required: bool = True) -> Capture:
    """A capture, read; one that is missing or unreadable is refused by name, and so is an empty one unless it is
    not `required` (a control's planted builder may compile nothing the wrappers see)."""
    records, manifest = where / "records.jsonl", where / "manifest.jsonl"
    if not manifest.is_file() or required and not records.is_file():
        raise CaptureError(f"no capture at {where}: it holds no {'manifest' if not manifest.is_file() else 'records'}")
    invocations, bypassed = [], []

    @lru_cache(maxsize=None)
    def listed(digest: str) -> Deps:
        """A kept dependency list, read once."""
        return deps((where / "text" / digest).read_text(encoding="utf-8"))

    @lru_cache(maxsize=None)
    def expanded(digest: str) -> Expansion:
        """A kept expansion report, read once."""
        return expansion(digest, lambda d: (where / "text" / d).read_text(encoding="utf-8"))

    lines = records.read_text(encoding="utf-8").splitlines() if records.is_file() else []
    made_by: dict[str, tuple[Expansion, tuple[str, ...]]] = {}
    for number, line in enumerate(lines, 1):
        try:
            raw = json.loads(line)
            if "bypass" in raw:
                bypassed.append({**raw, "from": json.loads(raw.get("from") or "[]")})
            else:
                invocations.append(invocation(raw, listed, expanded, made_by))
        except (OSError, ValueError, KeyError, TypeError) as exc:
            raise CaptureError(f"the capture at {where} has an unreadable record, line {number}: {exc}") from exc
    commands = tuple(json.loads(line) for line in manifest.read_text(encoding="utf-8").splitlines() if line)
    if required and not invocations:
        raise CaptureError(f"the capture at {where} is empty: it records no compiler invocation")
    unique = {(b["bypass"], tuple(b["args"]), b["cwd"]): b for b in bypassed}
    return Capture((where,), commands, tuple(invocations), tuple(unique.values()))


def main(argv: list[str] | None = None) -> int:
    """Run one command under the capture."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--out", type=Path, required=True, help="the capture directory (appended to)")
    ap.add_argument("command", nargs=argparse.REMAINDER, help="-- then the command")
    args = ap.parse_args(argv)
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        ap.error("no command")
    try:
        return run(args.out, command).returncode
    except CaptureError as exc:
        print(f"REFUSED: {exc}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
