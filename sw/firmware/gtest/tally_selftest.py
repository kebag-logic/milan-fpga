#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""tally_selftest.py - the tally listener's planted cases (#665 lane FT).

Builds tally_cases.cpp with the harness's main (fw_gtest_main.cpp), runs it
once per case with --gtest_filter, and requires each log to read as planted:

  * its tally line, read with scripts/suite_tally.py's own scanner, carries
    exactly the case's `checks` and `failures`, and the RESULT line under it
    says PASS when there are no failures and FAIL otherwise. A run that
    leaves no tally (an _exit(0) inside a test) must print none;
  * the control (one passing test) passes;
  * a failing assertion, each fatal signal the listener handles (SIGSEGV,
    SIGBUS, SIGFPE, SIGILL, and SIGABRT from an abort), an exit(0) inside a
    test, a skipped test, an uncaught exception, a disabled test, a disabled
    suite, a failure in a suite's set-up, one in a suite's tear-down and one
    in the global environment (outside every test) each fail: the run is
    refused, a [FAIL] line names the test, the suite or the program, and
    scripts/suite_tally.py --verdict, the sweep's own reader, exits 1 on the
    log;
  * an _exit(0) inside a test and a run that selects no test leave no tally,
    or a tally of nothing, and the sweep's tally refuses both as NOCOUNT;
  * a GoogleTest control in the environment (GTEST_ALSO_RUN_DISABLED_TESTS)
    does not reach the binary: fw_gtest.run drops GTEST_*, so the disabled
    test still runs nothing and still fails the tally.

The grading is fw_gtest.grade(), the one every firmware arm uses, so a
listener or a grader that lets any of these pass reddens this self-test.

--mutants then plants defects into copies of the listener (each seam must
match fw_gtest_main.cpp exactly once), builds the cases against each copy,
and requires every case a defect names to read otherwise than planted. A
defect whose named case still reads as planted, or a copy that does not
build, is an escape: the self-test cannot see that defect.

Usage:
    python3 sw/firmware/gtest/tally_selftest.py [--mutants]

Exit 0 = every case read as planted (and, with --mutants, every defect was
caught); 1 = a case did not, or a defect escaped; 2 = the cases could not be
built.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import fw_gtest  # noqa: E402
import suite_tally  # noqa: E402

TALLY = fw_gtest.ROOT / "scripts" / "suite_tally.py"
#: tally_cases.cpp's FW_TALLY_LABEL: the tally line must be the listener's.
LABEL = "firmware tally listener (planted cases)"


@dataclass(frozen=True)
class Case:
    """One planted run: its filter, whether it must pass, the test a [FAIL]
    line must name, whether the sweep's tally must call it NOCOUNT, and the
    (checks, failures) its tally line must carry, None for no tally."""

    what: str
    gtest_filter: str
    passes: bool
    tally: tuple[int, int] | None
    names: str = ""
    nocount: bool = False
    env: tuple[tuple[str, str], ...] = ()


CASES = (
    Case("a passing test (the control)", "Pass.*", True, (1, 0)),
    Case("a failing assertion", "Fail.*", False, (1, 1), "Fail.Expect"),
    Case("a crash on SIGSEGV", "Crash.Segv", False, (1, 1), "Crash.Segv"),
    Case("an abort", "Crash.Abort", False, (1, 1), "Crash.Abort"),
    Case("a crash on SIGBUS", "Crash.Bus", False, (1, 1), "Crash.Bus"),
    Case("a crash on SIGFPE", "Crash.Fpe", False, (1, 1), "Crash.Fpe"),
    Case("a crash on SIGILL", "Crash.Ill", False, (1, 1), "Crash.Ill"),
    Case("exit(0) inside a test", "Exit.Zero", False, (1, 1), "Exit.Zero"),
    Case("a skipped test", "Skip.*", False, (1, 1), "Skip.Silent"),
    Case("an uncaught exception", "Throw.*", False, (1, 1), "Throw.Uncaught"),
    Case("a disabled test", "Disabled.*", False, (0, 1), "Disabled.DISABLED_NeverRuns"),
    Case("a disabled suite", "DISABLED_Suite.*", False, (0, 1), "DISABLED_Suite.NeverRuns"),
    # GoogleTest fails the suite's test too, and the listener adds the set-up
    Case("a failure in a suite's set-up", "SetUpFails.*", False, (1, 2), "SetUpFails"),
    # the test passed, so the listener's count of the tear-down is the only failure
    Case("a failure in a suite's tear-down", "TearDownFails.*", False, (1, 1), "TearDownFails"),
    # likewise the program's: the global environment's set-up fails, its test passes
    Case("a failure in the global environment", "ProgramFails.*", False, (1, 1), "(program)"),
    Case("_exit(0) inside a test", "Exit.Immediate", False, None, nocount=True),
    Case("no test selected", "NoSuchSuite.*", False, (0, 0), nocount=True),
    Case("a disabled test, GTEST_ALSO_RUN_DISABLED_TESTS=1 in the environment", "Disabled.*", False, (0, 1),
         "Disabled.DISABLED_NeverRuns", env=(("GTEST_ALSO_RUN_DISABLED_TESTS", "1"),)),
)


@dataclass(frozen=True)
class Defect:
    """One defect planted into a copy of the listener: the exact text it
    replaces, what replaces it, and the cases that must stop reading as
    planted."""

    name: str
    old: str
    new: str
    cases: tuple[str, ...]


#: Every crash case, one per fatal signal the listener handles.
CRASHES = ("Crash.Segv", "Crash.Abort", "Crash.Bus", "Crash.Fpe", "Crash.Ill")
#: The signal list the listener installs its handler for.
SIGNALS = "{SIGSEGV, SIGBUS, SIGFPE, SIGILL, SIGABRT}"


def unhandled(sig: str, case: str) -> Defect:
    """One fatal signal dropped from the handler's list."""
    return Defect(f"{sig.lower()}-unhandled", SIGNALS, SIGNALS.replace(f"{sig}, ", "").replace(f", {sig}", ""),
                  (case,))


#: The listener's defects. The first three are R506-1-F2's: each falsified
#: the tally line while the [FAIL] marker alone kept the run refused. The
#: per-signal ones and the last two are R506-2-F3's; a program failure not
#: counted, like a suite tear-down's, leaves the tally line at RESULT: PASS.
DEFECTS = (
    Defect("skip-not-counted", "if (info.result()->Failed() || info.result()->Skipped()) {",
           "if (info.result()->Failed()) {", ("Skip.*",)),
    Defect("suite-failure-not-counted",
           '"  [FAIL] %s: a failure in its set-up or tear-down\\n", suite->name());\n                failures++;',
           '"  [FAIL] %s: a failure in its set-up or tear-down\\n", suite->name());',
           ("SetUpFails.*", "TearDownFails.*")),
    Defect("crash-tally-passes",
           '    put_number(static_cast<unsigned long>(sig));\n        put("\\n");\n'
           "        put_tally(state.checks + 1u, state.failures + 1u);",
           '    put_number(static_cast<unsigned long>(sig));\n        put("\\n");\n'
           "        put_tally(state.checks + 1u, state.failures);", CRASHES),
    Defect("crashed-test-not-counted",
           '    put_number(static_cast<unsigned long>(sig));\n        put("\\n");\n'
           "        put_tally(state.checks + 1u, state.failures + 1u);",
           '    put_number(static_cast<unsigned long>(sig));\n        put("\\n");\n'
           "        put_tally(state.checks, state.failures + 1u);", CRASHES),
    Defect("early-exit-tally-passes", "    put(how);\n    put_tally(state.checks + 1u, state.failures + 1u);",
           "    put(how);\n    put_tally(state.checks + 1u, state.failures);", ("Exit.Zero",)),
    Defect("disabled-not-counted", "failures += report_disabled(unit);",
           "static_cast<void>(report_disabled(unit));", ("Disabled.*", "DISABLED_Suite.*")),
    Defect("result-always-pass", 'put(failures == 0u ? "RESULT: PASS\\n" : "RESULT: FAIL\\n");',
           'put("RESULT: PASS\\n");', ("Fail.*", "Crash.Segv", "Exit.Zero", "Skip.*", "Disabled.*",
                                        "TearDownFails.*", "ProgramFails.*")),
    Defect("tests-not-counted", "        state.checks++;\n", "", ("Pass.*", "Fail.*")),
    Defect("fail-line-dropped", "if (part.passed()) {", "if (part.passed() || part.failed()) {", ("Fail.*",)),
    Defect("no-atexit", "    static_cast<void>(std::atexit(on_exit_early));\n", "", ("Exit.Zero",)),
    Defect("no-signal-handler", "static_cast<void>(std::signal(sig, on_fatal_signal));",
           "static_cast<void>(sig);", CRASHES),
    unhandled("SIGSEGV", "Crash.Segv"),
    unhandled("SIGBUS", "Crash.Bus"),
    unhandled("SIGFPE", "Crash.Fpe"),
    unhandled("SIGILL", "Crash.Ill"),
    unhandled("SIGABRT", "Crash.Abort"),
    Defect("program-failure-not-counted",
           '"  [FAIL] (program): a failure outside every test\\n");\n            failures++;',
           '"  [FAIL] (program): a failure outside every test\\n");', ("ProgramFails.*",)),
    Defect("disabled-suite-not-counted",
           'std::strncmp(suite->name(), "DISABLED_", 9) == 0 || std::strncmp(info->name(), "DISABLED_", 9) == 0',
           'std::strncmp(info->name(), "DISABLED_", 9) == 0', ("DISABLED_Suite.*",)),
)


def build(out: Path, b: fw_gtest.Build | None = None, main_source: Path = fw_gtest.MAIN_SOURCE) -> Path:
    """The planted cases, linked with the harness's main (or a copy of it)."""
    b = b or fw_gtest.Build()
    includes = [f"-I{HERE}"]
    objects = fw_gtest.compile_tests(b, includes, [HERE / "tally_cases.cpp", main_source], out)
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


def tally_wrong(case: Case, log_text: str) -> list[str]:
    """What the log's tally line and RESULT line say that the plant says
    they must not: read with suite_tally.scan, the sweep's own scanner."""
    _checks, _failures, matched, unparsed, _skipped = suite_tally.scan(log_text)
    results = re.findall(r"^RESULT: (\S+)$", log_text, re.M)
    if case.tally is None:
        return [f"a tally where none can be printed: {matched[0][3]}"] if matched or results else []
    want_result = "PASS" if case.tally[1] == 0 else "FAIL"
    wrong = []
    if len(matched) != 1 or unparsed or LABEL not in matched[0][3]:
        wrong.append(f"not one listener tally line: {[m[3] for m in matched] + unparsed}")
    elif (matched[0][1], matched[0][2]) != case.tally:
        wrong.append(f"tally checks {matched[0][1]} failures {matched[0][2]}, "
                     f"want checks {case.tally[0]} failures {case.tally[1]}")
    if results != [want_result]:
        wrong.append(f"RESULT lines {results}, want [{want_result!r}]")
    return wrong


def grade_case(case: Case, exe: Path, work: Path, quiet: bool = False) -> list[str]:
    """Run one case; what it did that the plant says it must not."""
    res = fw_gtest.run([str(exe), f"--gtest_filter={case.gtest_filter}"], timeout=fw_gtest.RUN_TIMEOUT_S,
                       env={**os.environ, **dict(case.env)})
    log_text = res.stdout + res.stderr
    log = work / f"{case.gtest_filter.replace('*', 'all').replace('.', '_')}{'_env' if case.env else ''}.log"
    log.write_text(log_text, encoding="utf-8")
    ok, why = fw_gtest.grade(res.returncode, log_text)
    wrong = tally_wrong(case, log_text)
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
    if not quiet:
        tally = "no tally" if case.tally is None else f"tally {case.tally[0]}/{case.tally[1]}"
        print(f"[{'ok' if not wrong else 'FAIL'}] {case.what}: exit {res.returncode}, {tally}, {why}")
    return wrong


def plant(defect: Defect, out: Path) -> Path:
    """A copy of the listener with the defect planted; the seam must match once."""
    text = fw_gtest.MAIN_SOURCE.read_text(encoding="utf-8")
    hits = text.count(defect.old)
    if hits != 1:
        raise fw_gtest.BuildError(f"the seam of {defect.name} matches {hits} times, not once")
    copy = out / f"main_{defect.name}.cpp"
    copy.write_text(text.replace(defect.old, defect.new), encoding="utf-8")
    return copy


def campaign(b: fw_gtest.Build, work: Path) -> int:
    """Every listener defect planted and graded; the number that escaped."""
    escaped = 0
    for defect in DEFECTS:
        out = work / "defects" / defect.name
        out.mkdir(parents=True)
        try:
            exe = build(out, b, plant(defect, out))
        except fw_gtest.BuildError as exc:
            print(f"[ESCAPE] {defect.name}: the planted copy does not build: {str(exc).splitlines()[0]}")
            escaped += 1
            continue
        red = {c.gtest_filter: grade_case(c, exe, out, quiet=True) for c in CASES if not c.env}
        missed = [f for f in defect.cases if not red[f]]
        also = sorted(f for f, w in red.items() if w and f not in defect.cases)
        first = next((w[0] for f in defect.cases for w in [red[f]] if w), "")
        if missed:
            print(f"[ESCAPE] {defect.name}: still read as planted: {', '.join(missed)}")
            escaped += 1
        else:
            print(f"[caught] {defect.name}: {', '.join(defect.cases)} ({first})"
                  + (f"; also {', '.join(also)}" if also else ""))
    print(f"listener defects: {len(DEFECTS) - escaped} of {len(DEFECTS)} caught")
    return escaped


def main() -> int:
    """Build the cases and grade each one; with --mutants, plant the listener's defects."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--mutants", action="store_true", help="also plant the listener's defects")
    args = ap.parse_args()
    print(f"toolchain: {fw_gtest.toolchain()}")
    b = fw_gtest.Build()
    with tempfile.TemporaryDirectory(prefix="fw-tally.") as tmp:
        work = Path(tmp)
        try:
            exe = build(work, b)
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
        escaped = campaign(b, work) if args.mutants and not failures else 0
    return 1 if failures or escaped else 0


if __name__ == "__main__":
    sys.exit(main())
