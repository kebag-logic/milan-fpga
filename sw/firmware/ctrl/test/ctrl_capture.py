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
with the real C compiler), which records the invocation and then runs the real
compiler with the same arguments, so every object, binary and image is what it
would be without the capture. Python processes it starts load an audit hook
(DIR/hook/sitecustomize.py) that names, for every process they start, the
checkout's files on their Python stack, and records any compiler a builder
runs by a path no wrapper stands on (a compile the capture would miss), so the
boundary can refuse it. Runs append to the same DIR; DIR/manifest.jsonl lists
each command, its directory and its exit status. The exit status is the
command's.

THE READER. load(DIR) gives every invocation the capture holds, each with the
builders it came from: the checkout's files on the Python stack of the process
that ran the compiler, and the script or Makefile of each ancestor process.

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

import ctrl_shim

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
#: The recorder's name in a capture's bin/.
RECORDER = ".ctrl-recorder"
#: A C or C++ compiler's name, prefixed (x86_64-linux-gnu-, riscv32-linux-) or versioned (-13) or neither.
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
    for part in (bin_dir, hook, capture / "text"):
        part.mkdir(parents=True, exist_ok=True)
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
                "CTRL_CAPTURE_BIN": str(bin_dir), "CTRL_CAPTURE_ROOT": str(ROOT), "CTRL_CAPTURE_FROM": "",
                "CTRL_CAPTURE_TOP": str(os.getpid()),
                "PYTHONPATH": os.pathsep.join(p for p in (str(hook), os.environ.get("PYTHONPATH", "")) if p)})
    return env


def run(capture: Path, argv: list[str], cwd: Path | None = None, env_extra: dict[str, str] | None = None,
        **kwargs) -> subprocess.CompletedProcess:
    """One command under the capture, listed in its manifest."""
    env = {**install(capture), **(env_extra or {})}
    start = time.monotonic()
    res = subprocess.run(argv, cwd=cwd, env=env, check=False, **kwargs)
    line = json.dumps({"argv": argv, "cwd": str(cwd or Path.cwd()), "rc": res.returncode,
                       "seconds": round(time.monotonic() - start, 1)}) + "\n"
    with (capture.resolve() / "manifest.jsonl").open("a", encoding="utf-8") as out:
        out.write(line)
    return res


# ---- the reader -------------------------------------------------------------------------------


@dataclass(frozen=True)
class Invocation:
    """One recorded compile: the name it was called by, its arguments and directory, each source with its
    language and digest, its -D and -U flags, the directories it searches, the files it reads first, the texts
    the capture kept for it (path to digest), and the checkout's builder files it came from."""

    tool: str
    args: tuple[str, ...]
    cwd: str
    sources: tuple[tuple[str, str, str], ...]
    flags: tuple[str, ...]
    dirs: tuple[str, ...]
    forced: tuple[str, ...]
    kept: tuple[tuple[str, str], ...]
    builders: frozenset[str]


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
    """The checkout's builder files an ancestor process names: a Python process's script, a make's Makefile."""
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


def invocation(raw: dict, kept: Callable[[str], object], chained: Callable[[str], frozenset[str]]) -> Invocation:
    """One record, read: the headers kept beside it are a kept text (`kept` reads one), and its ancestry's
    builders are read once per ancestry (`chained`)."""
    builders = set(json.loads(raw.get("from") or "[]")) | chained(raw["chain"])
    cwd = raw["cwd"]
    seen = ctrl_shim.parse(raw["tool"], raw["args"])
    dirs = tuple(dict.fromkeys(resolved(cwd, d) for _, d in seen["dirs"]))
    beside = kept(raw["kept"]) if raw["kept"] else {}
    return Invocation(raw["tool"], tuple(raw["args"]), cwd, tuple(tuple(s) for s in raw["sources"]),
                      tuple(seen["flags"]), dirs, tuple(raw["forced"]), tuple(sorted(beside.items())),
                      frozenset(builders))


def load(where: Path, required: bool = True) -> Capture:
    """A capture, read; one that is missing or unreadable is refused by name, and so is an empty one unless it is
    not `required` (a control's planted builder may compile nothing the wrappers see)."""
    records, manifest = where / "records.jsonl", where / "manifest.jsonl"
    if not manifest.is_file() or required and not records.is_file():
        raise CaptureError(f"no capture at {where}: it holds no {'manifest' if not manifest.is_file() else 'records'}")
    invocations, bypassed = [], []

    @lru_cache(maxsize=None)
    def kept(digest: str) -> object:
        return json.loads((where / "text" / digest).read_text(encoding="utf-8"))

    @lru_cache(maxsize=None)
    def chained(name: str) -> frozenset[str]:
        return frozenset(builder for cwd, argv in kept(name) for builder in script_of(cwd, argv))

    lines = records.read_text(encoding="utf-8").splitlines() if records.is_file() else []
    for number, line in enumerate(lines, 1):
        try:
            raw = json.loads(line)
            if "bypass" in raw:
                bypassed.append({**raw, "from": json.loads(raw.get("from") or "[]")})
            else:
                invocations.append(invocation(raw, kept, chained))
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
