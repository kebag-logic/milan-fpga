#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""tally_selftest.py - the tally listener's planted cases (#665 lane FT).

Builds tally_cases.cpp with the harness's main (fw_gtest_main.cpp), runs it
once per case with --gtest_filter, and requires each log to read as planted:

  * the control (one passing test) passes, with a tally of one test;
  * a failing assertion, a crash (SIGSEGV), an abort, an exit(0) inside a
    test, a skipped test, an uncaught exception, a disabled test and a
    failure in a suite's set-up each fail: the run is refused, a [FAIL] line
    names the test, and scripts/suite_tally.py --verdict, the sweep's own
    reader, exits 1 on the log;
  * an _exit(0) inside a test and a run that selects no test leave no tally,
    or a tally of nothing, and the sweep's tally refuses both as NOCOUNT.

The grading is fw_gtest.grade(), the one every firmware arm uses, so a
listener or a grader that lets any of these pass reddens this self-test.

Usage:
    python3 sw/firmware/gtest/tally_selftest.py

Exit 0 = every case read as planted; 1 = a case did not; 2 = the cases
could not be built.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import fw_gtest  # noqa: E402

TALLY = fw_gtest.ROOT / "scripts" / "suite_tally.py"


@dataclass(frozen=True)
class Case:
    """One planted run: its filter, whether it must pass, the test a [FAIL]
    line must name, and whether the sweep's tally must call it NOCOUNT."""

    what: str
    gtest_filter: str
    passes: bool
    names: str = ""
    nocount: bool = False


CASES = (
    Case("a passing test (the control)", "Pass.*", True),
    Case("a failing assertion", "Fail.*", False, "Fail.Expect"),
    Case("a crash on SIGSEGV", "Crash.Segv", False, "Crash.Segv"),
    Case("an abort", "Crash.Abort", False, "Crash.Abort"),
    Case("exit(0) inside a test", "Exit.Zero", False, "Exit.Zero"),
    Case("a skipped test", "Skip.*", False, "Skip.Silent"),
    Case("an uncaught exception", "Throw.*", False, "Throw.Uncaught"),
    Case("a disabled test", "Disabled.*", False, "Disabled.DISABLED_NeverRuns"),
    Case("a failure in a suite's set-up", "SetUpFails.*", False, "SetUpFails"),
    Case("_exit(0) inside a test", "Exit.Immediate", False, nocount=True),
    Case("no test selected", "NoSuchSuite.*", False, nocount=True),
)


def build(out: Path) -> Path:
    """The planted cases, linked with the harness's main."""
    b = fw_gtest.Build()
    includes = [f"-I{HERE}"]
    objects = fw_gtest.compile_tests(b, includes, [HERE / "tally_cases.cpp"], out) + [fw_gtest.main_object(b, out)]
    return fw_gtest.link(b, objects, out / "tally_cases")


def verdict_cli(log: Path) -> int:
    """scripts/suite_tally.py --verdict on one log: the sweep's own reading."""
    return subprocess.run([sys.executable, str(TALLY), "--verdict", str(log)], capture_output=True,
                          text=True, check=False).returncode


def nocount_cli(log: Path, work: Path) -> bool:
    """Whether scripts/suite_tally.py, given the log as a suite's, calls it NOCOUNT."""
    suite = work / "nocount" / log.stem
    suite.mkdir(parents=True, exist_ok=True)
    (suite / f"{log.stem}.log").write_text(log.read_text(encoding="utf-8"), encoding="utf-8")
    res = subprocess.run([sys.executable, str(TALLY), str(suite), "--quiet"], capture_output=True, text=True,
                         check=False)
    return res.returncode == 1 and f"NOCOUNT  {log.stem}" in res.stdout


def grade_case(case: Case, exe: Path, work: Path) -> list[str]:
    """Run one case; what it did that the plant says it must not."""
    res = fw_gtest.run([str(exe), f"--gtest_filter={case.gtest_filter}"], timeout=fw_gtest.RUN_TIMEOUT_S)
    log_text = res.stdout + res.stderr
    log = work / f"{case.gtest_filter.replace('*', 'all').replace('.', '_')}.log"
    log.write_text(log_text, encoding="utf-8")
    ok, why = fw_gtest.grade(res.returncode, log_text)
    wrong = []
    if ok != case.passes:
        wrong.append(f"graded {'PASS' if ok else 'FAIL'} ({why})")
    if case.names and case.names not in fw_gtest.failed_tests(log_text):
        wrong.append(f"no [FAIL] line names {case.names}")
    if case.nocount != why.startswith("NOCOUNT"):
        wrong.append(f"NOCOUNT expected {case.nocount}, the grade says: {why}")
    if case.nocount and not nocount_cli(log, work):
        wrong.append("scripts/suite_tally.py does not refuse it as NOCOUNT")
    if not case.nocount and verdict_cli(log) != (0 if case.passes else 1):
        wrong.append("scripts/suite_tally.py --verdict disagrees")
    print(f"[{'ok' if not wrong else 'FAIL'}] {case.what}: exit {res.returncode}, {why}")
    return wrong


def main() -> int:
    """Build the cases and grade each one."""
    with tempfile.TemporaryDirectory(prefix="fw-tally.") as tmp:
        work = Path(tmp)
        try:
            exe = build(work)
        except fw_gtest.BuildError as exc:
            print(f"REFUSED: {exc}")
            return 2
        failures = 0
        for case in CASES:
            wrong = grade_case(case, exe, work)
            for w in wrong:
                print(f"    {w}")
            failures += 1 if wrong else 0
    print(f"tally self-test: {len(CASES) - failures} of {len(CASES)} planted cases read as planted")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
