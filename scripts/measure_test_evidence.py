#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Measure how much a passing suite actually proves.

Why this exists. Rule 8 of the maintainability guide
(docs/development/CODE_QUALITY.md) says a test's oracle comes from the
specification, its assertions are mutation-proven, and a pass publishes a
non-zero tally. A suite can be green and prove nothing: assertions that have
never been observed to fail are indistinguishable from assertions that cannot.

Four things are counted or refused, and one is already clean.

  1. MUTATION COVERAGE. A suite carries an executable arm that deliberately breaks
     something and requires the suite to notice - a mutated DUT, an illegal
     parameter, a broken fixture. The inventory includes the superproject's
     Verilator suites and the processor submodules' own RTL suites.
     This is a RATCHET: the number without one may only fall.

  2. REPLAYABLE RANDOMNESS. A test that draws random values without recording
     a seed cannot be replayed from its own failure. Every first-party file
     that draws already seeds - this is measured and reported as ZERO, and it
     must stay zero, because the cost of finding out otherwise is a flaky
     failure nobody can reproduce.

  3. DUT-SOURCE ORACLES. A high-signal inventory finds test programs that read
     production HDL text. The current readers are structural contract or
     mutation tools, each explicitly classified; an unexplained reader is
     refused because copying expected values out of the implementation would
     make a test agree with the same defect.

  4. WALL-CLOCK DEPENDENCE. Suite files that use host time or process/socket
     deadlines are ratcheted. Cycle-bounded protocol timeouts are deterministic
     and do not enter this population. The common runner must classify a suite
     killed by its wall-clock guard as UNKNOWN, never pass or fail, and must run
     the tally self-test before starting the sweep.

Not counted here, because another gate already owns it: a missing or malformed
tally is `NOCOUNT` in `scripts/suite_tally.py`, which refuses to let an unknown
look like agreement. This script does not re-implement that judgement.

Usage:
    python3 scripts/measure_test_evidence.py            # both inventories
    python3 scripts/measure_test_evidence.py --check    # the ratchets
    python3 scripts/measure_test_evidence.py --selftest # fixture arms

Exit 0 = at or under the ratchets in scripts/test_evidence.budget.
"""

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BUDGET = Path(__file__).resolve().parent / "test_evidence.budget"
SUITE_ROOT = REPO / "tb/verilator"

#: Executable evidence, not prose claiming that a mutation once ran. A suite
#: must expose a runnable target/command, a mutation table, an illegal-case
#: table, or compile-time mutation defines that the driver actually exercises.
ARM = re.compile(
    r"(?m)^\s*(?:mutants?|negative|self-?test)\s*:"
    r"|\bmutants?\.py\b|--self-?test\b|\bMUTATIONS?\s*="
    r"|\bNEG_CASES\s*=|\bmutation_checks\s*\("
    r"|-D[A-Za-z0-9_]*MUT[A-Za-z0-9_]*"
    r"|\+define\+[A-Za-z0-9_]*MUT[A-Za-z0-9_]*", re.I)

#: a random draw, and the seed that makes it replayable
DRAW = re.compile(r"(?<![\w.])random\.(?:random|randint|choice|shuffle|randrange"
                  r"|uniform|sample|getrandbits)\s*\(|(?<![\w:])rand\s*\(\s*\)")
SEED = re.compile(r"random\.Random\s*\(\s*\d|random\.seed\s*\(\s*\d|srand\s*\(\s*\d")

# Reading the DUT is not automatically wrong: mutation arms must rewrite the
# DUT and structural contract checks must inspect it. It is, however, the
# smallest useful static population for an implementation-derived-oracle
# review. Every present reader has a narrow recorded reason; a new one is debt
# until it is classified.
DUT_READ = re.compile(r"\bread_text\s*\(")
DUT_PATH = re.compile(r"\b(?:RTL|FILTER)\s*=|[\"'][^\"'\n]*hdl/")
DUT_READER_DISPOSITIONS = {
    "gptp-processor/tb/check_phc_contract.py":
        "structural boundary check; it asserts required/forbidden tokens, not behavior",
    "protocol-processor/tb/nvm_port/measure_figures.py":
        "mutation campaign; it rewrites one RTL arm and requires the suite to fail",
    "tb/verilator/rx_filter/binding_mutant.py":
        "mutation campaign; it ties a real named binding low and requires failure",
    "tb/verilator/tcam/mutants.py":
        "mutation campaign; it injects three RTL defects and requires failure",
}

# Host time can vary with machine load. This deliberately ignores identifiers
# such as `timeout_cycles`: protocol time advanced by explicit DUT ticks is a
# deterministic oracle. It catches actual host clocks, sleeps, socket deadlines
# and subprocess deadlines.
WALL_CLOCK = re.compile(
    r"\btime\.(?:time|monotonic|sleep)\s*\(|\.settimeout\s*\("
    r"|\b(?:subprocess\.)?(?:run|wait)\s*\([^)]*\btimeout\s*=", re.S)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from code_quality_scope import tracked, tracked_exact


def suite_text(name):
    """Everything a suite is made of: its makefile, harnesses and wrappers."""
    parts = []
    for rel in tracked_exact(f"{name}/*"):
        try:
            parts.append((REPO / rel).read_text(errors="replace"))
        except OSError:
            pass
    return "\n".join(parts)


def suites():
    makefiles = tracked("tb/verilator/*/Makefile", "tb/*/Makefile")
    return sorted({str(Path(rel).parent) for rel in makefiles
                   if "/tb/" in rel or rel.startswith("tb/")})


def has_arm(text):
    return bool(ARM.search(text))


def draws_without_seed(text):
    return bool(DRAW.search(text)) and not SEED.search(text)


def test_sources():
    suffixes = {".py", ".cpp", ".cc", ".c", ".sv", ".v", ".sh"}
    return sorted(rel for rel in tracked("tb/*", "tb/**/*")
                  if Path(rel).suffix in suffixes or Path(rel).name == "Makefile")


def suite_sources():
    """Executable files owned by a directory that the suite inventory names."""
    suffixes = {".py", ".cpp", ".cc", ".c", ".sv", ".v", ".sh"}
    paths = {rel for name in suites() for rel in tracked_exact(f"{name}/*")}
    return sorted(rel for rel in paths
                  if Path(rel).suffix in suffixes or Path(rel).name == "Makefile")


def reads_dut_source(text):
    return bool(DUT_READ.search(text) and DUT_PATH.search(text))


def uses_wall_clock(text):
    return bool(WALL_CLOCK.search(text))


def runner_contract(text):
    """Problems in the common sweep's timeout and tally evidence contract."""
    problems = []
    launch = text.find('timeout "$TMO" make')
    tally_selftest = text.find('suite_tally.py" --selftest')
    tally_run = text.find('suite_tally.py" "$OUT" --quiet')
    if launch < 0:
        problems.append("the per-suite wall-clock guard is missing")
    if tally_selftest < 0 or (launch >= 0 and tally_selftest > launch):
        problems.append("the tally self-test does not run before the first suite")
    if tally_run < 0 or (launch >= 0 and tally_run < launch):
        problems.append("the final log tally does not run after the suites")
    if "124|137)" not in text or "tmo=$((tmo + 1))" not in text:
        problems.append("timeout/OOM exits are not classified separately")
    if '[ "$tmo"  -gt 0 ] && exit 92' not in text:
        problems.append("an unknown timeout result does not return exit 92")
    if '[ "$tally_rc" -ne 0 ] && exit 90' not in text:
        problems.append("a malformed or missing tally does not return exit 90")
    return problems


def audit():
    armed, unarmed = [], []
    for name in suites():
        (armed if has_arm(suite_text(name)) else unarmed).append(name)

    unseeded = []
    for rel in tracked("tb/**/*.py", "sw/**/*.py", "scripts/*.py", "tests/**/*.py",
                       "tb/**/*.cpp"):
        if draws_without_seed((REPO / rel).read_text(errors="replace")):
            unseeded.append(rel)

    readers = []
    for rel in test_sources():
        text = (REPO / rel).read_text(errors="replace")
        if reads_dut_source(text):
            readers.append(rel)
    wallclock = []
    for rel in suite_sources():
        text = (REPO / rel).read_text(errors="replace")
        if uses_wall_clock(text):
            wallclock.append(rel)
    unexplained = sorted(set(readers) - set(DUT_READER_DISPOSITIONS))
    stale = sorted(set(DUT_READER_DISPOSITIONS) - set(readers))
    return armed, unarmed, unseeded, readers, unexplained, stale, wallclock


def read_budget():
    if not BUDGET.is_file():
        return None, None, None, None
    vals = [int(x) for x in re.findall(r"^\s*(\d+)\s*$", BUDGET.read_text(), re.M)]
    return (vals + [None, None, None, None])[:4]


def selftest():
    failures = 0

    def ck(name, ok, detail=""):
        nonlocal failures
        if ok:
            print(f"[PASS] {name}")
        else:
            failures += 1
            print(f"[FAIL] {name}{': ' + detail if detail else ''}")

    ck("a runnable mutant command is armed", has_arm("python3 mutants.py"))
    ck("an executable negative target is armed", has_arm("negative:\n\t./broken-case"))
    ck("a suite with a self-test is armed", has_arm("python3 x.py --selftest"))
    ck("an ordinary suite is not armed", not has_arm("build and run the harness"))
    ck("mutation prose alone is not an executable arm",
       not has_arm("the mutation was run by hand and failed"))

    ck("an unseeded draw is caught", draws_without_seed("x = random.choice([1,2])"))
    ck("a seeded draw is not", not draws_without_seed("random.seed(11)\nx = random.choice([1,2])"))
    ck("a Random(seed) instance counts as seeded",
       not draws_without_seed("rng = random.Random(13)\nx = random.choice([1,2])"))
    ck("a file that never draws is not counted", not draws_without_seed("x = 1"))
    ck("a C rand() with no srand is caught", draws_without_seed("int x = rand();"))
    ck("a C rand() with srand is not", not draws_without_seed("srand(7); int x = rand();"))

    ck("a test reading an HDL source is an oracle-review candidate",
       reads_dut_source('RTL = ROOT / "hdl/block.sv"\nsrc = RTL.read_text()'))
    ck("an ordinary behavioral harness is not a source-reader candidate",
       not reads_dut_source("expect(got, 7);"))
    ck("host sleep is wall-clock dependent", uses_wall_clock("time.sleep(0.02)"))
    ck("a cycle timeout is deterministic",
       not uses_wall_clock("for (int timeout_cycles = 0; timeout_cycles < 32; ++timeout_cycles) tick();"))

    runner = (REPO / "scripts/run_all_suites.sh").read_text()
    ck("the live runner preserves timeout and tally verdicts",
       not runner_contract(runner), "; ".join(runner_contract(runner)))
    ck("a timeout reported as failure is rejected",
       bool(runner_contract(runner.replace("exit 92", "exit 1"))))

    armed, unarmed, unseeded, readers, unexplained, stale, wallclock = audit()
    ck("the live scan sees the suites", len(armed) + len(unarmed) > 40,
       f"{len(armed) + len(unarmed)} suites")
    ck("both sides of the mutation split are non-empty",
       bool(armed) and bool(unarmed),
       "an inert classifier would put every suite on one side")
    ck("every DUT-source reader has a current disposition",
       not unexplained and not stale, f"unexplained={unexplained}, stale={stale}")

    n = 20
    print(f"\n{n} checks: {n - failures} PASS, {failures} FAIL")
    return 1 if failures else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="ratchet both counts")
    ap.add_argument("--selftest", action="store_true", help="run the fixture arms")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    armed, unarmed, unseeded, readers, unexplained, stale, wallclock = audit()
    print(f"RTL suites with an executable mutation or negative arm: "
          f"{len(armed)} of {len(armed) + len(unarmed)}")
    print(f"\nsuites with none ({len(unarmed)}):")
    for name in unarmed:
        print(f"   {name}")
    print(f"\nfiles that draw random values without recording a seed ({len(unseeded)}):")
    for rel in unseeded:
        print(f"   {rel}")
    print(f"\ntest programs that read production HDL ({len(readers)}):")
    for rel in readers:
        print(f"   {rel}: {DUT_READER_DISPOSITIONS.get(rel, 'UNEXPLAINED')}")
    print(f"\nsuite files using host wall-clock/process deadlines ({len(wallclock)}):")
    for rel in wallclock:
        print(f"   {rel}")

    runner_problems = runner_contract((REPO / "scripts/run_all_suites.sh").read_text())
    print("\nrunner evidence contract: " + ("OK" if not runner_problems else "FAIL"))
    for problem in runner_problems:
        print(f"   {problem}")

    if not args.check:
        return 0

    b_unarmed, b_unseeded, b_unexplained, b_wallclock = read_budget()
    if any(value is None for value in
           (b_unarmed, b_unseeded, b_unexplained, b_wallclock)):
        print(f"\nNO RATCHET: {BUDGET.relative_to(REPO)} must hold four counts")
        return 1
    bad = False
    if len(unarmed) > b_unarmed:
        print(f"\nFAIL: {len(unarmed)} suite(s) with no mutation arm > ratchet "
              f"{b_unarmed}. A new suite proves its own assertions can fail.")
        bad = True
    if len(unseeded) > b_unseeded:
        print(f"\nFAIL: {len(unseeded)} unseeded random draw site(s) > ratchet "
              f"{b_unseeded}. A random test records the seed it can be replayed from.")
        bad = True
    if len(unexplained) > b_unexplained or stale:
        print(f"\nFAIL: {len(unexplained)} unexplained DUT-source reader(s) > "
              f"ratchet {b_unexplained}; stale dispositions: {stale}")
        bad = True
    if len(wallclock) > b_wallclock:
        print(f"\nFAIL: {len(wallclock)} wall-clock-dependent suite file(s) > "
              f"ratchet {b_wallclock}. New behavioral tests use DUT cycles, not host time.")
        bad = True
    if runner_problems:
        bad = True
    if bad:
        return 1
    print(f"\nTEST-EVIDENCE RATCHET: PASS ({len(unarmed)} <= {b_unarmed} suite(s) "
          f"without a mutation arm, {len(unseeded)} <= {b_unseeded} unseeded "
          f"draw site(s), {len(unexplained)} <= {b_unexplained} unexplained "
          f"DUT-source reader(s), {len(wallclock)} <= {b_wallclock} "
          "wall-clock-dependent suite file(s))")
    if len(unarmed) < b_unarmed:
        print(f"  the mutation ratchet can be lowered to {len(unarmed)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
