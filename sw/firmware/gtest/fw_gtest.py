# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""fw_gtest.py - build, run and grade the firmware's GoogleTest binaries (#665 lane FT).

Both host gates (sw/firmware/ctrl/test/test_ctrl_firmware.py and
sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py) compile the firmware as C11, the
tests as C++ against the system's GoogleTest and GoogleMock, and link every
test binary with fw_gtest_main.cpp, which prints the tally. A binary passes
only when it exits 0 AND its log reads as a pass to scripts/suite_tally.py:
one tally in a shape the reader knows, no NOCOUNT, no failure in a tally and
no [FAIL] line. So a test that crashes, ends the program early or never runs
is a failure, never a quiet zero (README.md, "The tally").

A coverage build (Build.coverage) compiles the firmware and the tests at -O0
with gcov's instrumentation, the host models and stubs without it;
fw_coverage.py reads what the runs leave behind and measures only the
firmware's own sources.
"""

from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys
from collections.abc import Iterable, Mapping, Sequence
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import suite_tally  # noqa: E402

#: The harness every test binary links: main() and the tally listener.
MAIN_SOURCE = HERE / "fw_gtest_main.cpp"
#: C++20 for the designated initialisers the C tests used; warnings are errors.
CXX_FLAGS = ("-std=c++20", "-O1", "-g", "-Wall", "-Wextra", "-Werror")
#: The libraries every binary links, GoogleMock before the GoogleTest it uses.
TEST_LIBS = ("-lgmock", "-lgtest", "-pthread")
#: What a coverage build compiles the firmware with instead of its optimisation.
COVERAGE_FLAGS = ("-O0", "--coverage")
#: How long one test binary may run before it is a failure, never a pass.
RUN_TIMEOUT_S = 600


class BuildError(Exception):
    """A source did not compile or a binary did not link: the caller refuses."""


@dataclass
class Build:
    """How a gate builds: the compilers, coverage or not, and the jobs."""

    coverage: bool = False
    jobs: int = os.cpu_count() or 4
    #: compiled C++ objects by content key, shared by every arm of one run
    cache: dict[str, Path] = field(default_factory=dict)

    @property
    def cc(self) -> str:
        """The C compiler."""
        return os.environ.get("CC", "gcc")

    @property
    def cxx(self) -> str:
        """The C++ compiler."""
        return os.environ.get("CXX", "g++")

    def cxx_flags(self) -> list[str]:
        """The tests' flags; a coverage build instruments them too, so firmware
        code a test runs in its own object (a header's inline helper) counts."""
        return self.c_flags(CXX_FLAGS)

    def c_flags(self, flags: Sequence[str]) -> list[str]:
        """A module's C flags, with its optimisation replaced in a coverage build."""
        if not self.coverage:
            return list(flags)
        return [f for f in flags if not re.fullmatch(r"-O[0-3sgz]?", f)] + list(COVERAGE_FLAGS)


def run(argv: Sequence[str], cwd: Path | None = None, timeout: int | None = None,
        env: Mapping[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    """One subprocess, its output captured; a timeout, or a program that is not
    there, is a failed run. GoogleTest's own controls (GTEST_*) are dropped
    from its environment, so a shell's GTEST_FILTER or the like cannot narrow
    or reshape what a gate's binaries run (R506-1-S2)."""
    clean = {k: v for k, v in (os.environ if env is None else env).items() if not k.startswith("GTEST_")}
    try:
        return subprocess.run(list(argv), cwd=cwd, capture_output=True, text=True, check=False,
                              timeout=timeout, env=clean)
    except subprocess.TimeoutExpired as exc:
        # what the child printed before the kill, which the exception holds as bytes
        out = exc.stdout.decode(errors="replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        return subprocess.CompletedProcess(list(argv), 124, out, f"\ntimed out after {timeout} s")
    except OSError as exc:
        return subprocess.CompletedProcess(list(argv), 127, "", f"cannot run {argv[0]}: {exc.strerror}")


def _compile(argv: list[str], src: Path) -> None:
    res = run(argv)
    if res.returncode != 0:
        raise BuildError(f"{src.name} does not compile:\n{res.stderr}")


def compile_many(build: Build, units: Iterable[tuple[list[str], Path]]) -> None:
    """Compile (argv, source) pairs in parallel; the first error is raised."""
    work = list(units)
    with ThreadPoolExecutor(max_workers=max(1, build.jobs)) as pool:
        for future in [pool.submit(_compile, argv, src) for argv, src in work]:
            future.result()


def compile_c(build: Build, flags: Sequence[str], includes: Sequence[str], sources: Sequence[Path],
              out: Path, measured: bool = True) -> list[Path]:
    """C sources to objects under out/, one object per source. Only the
    firmware is `measured`: a host model or a stub is test equipment, and a
    coverage build leaves it uninstrumented."""
    out.mkdir(parents=True, exist_ok=True)
    objects = [out / f"{src.parent.name}_{src.stem}.o" for src in sources]
    use = build.c_flags(flags) if measured else list(flags)
    compile_many(build, [([build.cc, *use, *includes, "-c", str(src), "-o", str(obj)], src)
                         for src, obj in zip(sources, objects)])
    return objects


def compile_tests(build: Build, includes: Sequence[str], sources: Sequence[Path], out: Path,
                  extra: Sequence[str] = ()) -> list[Path]:
    """Test sources (C++) to objects. An object is reused across arms and
    planted copies when its source and its whole preprocessed text are the
    same, so a defect planted in a header rebuilds every test that sees it."""
    out.mkdir(parents=True, exist_ok=True)
    objects: list[Path] = []
    todo: list[tuple[list[str], Path]] = []
    for src in sources:
        flags = [*build.cxx_flags(), *includes, *extra]
        pre = run([build.cxx, *flags, "-E", "-P", str(src)])
        if pre.returncode != 0:
            raise BuildError(f"{src.name} does not preprocess:\n{pre.stderr}")
        key = hashlib.sha256("\0".join([str(src), *flags, pre.stdout]).encode()).hexdigest()
        obj = build.cache.get(key)
        if obj is None or not obj.exists():
            obj = out / f"{src.stem}-{key[:12]}.o"
            todo.append(([build.cxx, *flags, "-c", str(src), "-o", str(obj)], src))
            build.cache[key] = obj
        objects.append(obj)
    compile_many(build, todo)
    return objects


def main_object(build: Build, out: Path) -> Path:
    """fw_gtest_main.cpp's object, compiled once per run."""
    return compile_tests(build, [f"-I{HERE}"], [MAIN_SOURCE], out)[0]


def link(build: Build, objects: Sequence[Path], exe: Path) -> Path:
    """Link test and firmware objects with the harness's main into exe."""
    flags = ["--coverage"] if build.coverage else []
    res = run([build.cxx, *flags, *map(str, objects), "-o", str(exe), *TEST_LIBS])
    if res.returncode != 0:
        raise BuildError(f"{exe.name} does not link:\n{res.stderr}")
    return exe


def grade(rc: int, log: str) -> tuple[bool, str]:
    """(passed, why) for one binary's run, read the way the sweep reads a suite log."""
    checks, failures, matched, unparsed, skipped = suite_tally.scan(log)
    if suite_tally.is_nocount(checks, failures, matched, skipped):
        return False, "NOCOUNT: no tally, or a tally of nothing (the run did not finish)"
    if unparsed:
        return False, f"UNPARSED tally line: {unparsed[0]}"
    reason, failed = suite_tally.log_reports_failure(log)
    if failed:
        return False, reason
    if rc != 0:
        return False, f"exit status {rc} under a passing tally"
    return True, f"{checks} tests, 0 failures"


def run_binary(exe: Path, args: Sequence[str] = (), cwd: Path | None = None,
               env: Mapping[str, str] | None = None) -> tuple[bool, str]:
    """Run one test binary; (passed, its log ending in the verdict)."""
    res = run([str(exe), *args], cwd=cwd, timeout=RUN_TIMEOUT_S, env=env)
    log = res.stdout + res.stderr
    ok, why = grade(res.returncode, log)
    return ok, f"{log.rstrip()}\n  verdict: {'PASS' if ok else 'FAIL'} ({why}, exit {res.returncode})"


def failed_tests(log: str) -> set[str]:
    """The tests a log names on a [FAIL] line: what a planted defect is graded by."""
    return {m.group(1) for m in re.finditer(r"^\s*\[FAIL\] ([^\s:]+):", log, re.M)}


def toolchain() -> dict[str, str]:
    """The versions a run used, for its evidence: compilers, gcov and GoogleTest."""
    def first_line(argv: list[str]) -> str:
        """The first line a tool prints about itself, or "absent"."""
        res = run(argv)
        return (res.stdout or res.stderr).splitlines()[0].strip() if res.returncode == 0 else "absent"
    build = Build()
    return {"cc": first_line([build.cc, "--version"]), "cxx": first_line([build.cxx, "--version"]),
            "gcov": first_line(["gcov", "--version"]),
            "gtest": first_line(["pkg-config", "--modversion", "gtest"]),
            "gmock": first_line(["pkg-config", "--modversion", "gmock"])}
