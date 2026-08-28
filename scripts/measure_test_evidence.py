#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Measure how much a passing suite actually proves.

Why this exists. Rule 8 of the maintainability guide
(docs/development/CODE_QUALITY.md) says a test's oracle comes from the
specification, its assertions are mutation-proven, and a pass publishes a
non-zero tally. A suite can be green and prove nothing: assertions that have
never been observed to fail are indistinguishable from assertions that cannot.

Two things are counted, and one is already clean.

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


def audit():
    armed, unarmed = [], []
    for name in suites():
        (armed if has_arm(suite_text(name)) else unarmed).append(name)

    unseeded = []
    for rel in tracked("tb/**/*.py", "sw/**/*.py", "scripts/*.py", "tests/**/*.py",
                       "tb/**/*.cpp"):
        if draws_without_seed((REPO / rel).read_text(errors="replace")):
            unseeded.append(rel)
    return armed, unarmed, unseeded


def read_budget():
    if not BUDGET.is_file():
        return None, None
    vals = [int(x) for x in re.findall(r"^\s*(\d+)\s*$", BUDGET.read_text(), re.M)]
    return (vals + [None, None])[:2]


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

    armed, unarmed, unseeded = audit()
    ck("the live scan sees the suites", len(armed) + len(unarmed) > 40,
       f"{len(armed) + len(unarmed)} suites")
    ck("both sides of the mutation split are non-empty",
       bool(armed) and bool(unarmed),
       "an inert classifier would put every suite on one side")

    n = 13
    print(f"\n{n} checks: {n - failures} PASS, {failures} FAIL")
    return 1 if failures else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="ratchet both counts")
    ap.add_argument("--selftest", action="store_true", help="run the fixture arms")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    armed, unarmed, unseeded = audit()
    print(f"RTL suites with an executable mutation or negative arm: "
          f"{len(armed)} of {len(armed) + len(unarmed)}")
    print(f"\nsuites with none ({len(unarmed)}):")
    for name in unarmed:
        print(f"   {name}")
    print(f"\nfiles that draw random values without recording a seed ({len(unseeded)}):")
    for rel in unseeded:
        print(f"   {rel}")

    if not args.check:
        return 0

    b_unarmed, b_unseeded = read_budget()
    if b_unarmed is None or b_unseeded is None:
        print(f"\nNO RATCHET: {BUDGET.relative_to(REPO)} must hold two counts")
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
    if bad:
        return 1
    print(f"\nTEST-EVIDENCE RATCHET: PASS ({len(unarmed)} <= {b_unarmed} suite(s) "
          f"without a mutation arm, {len(unseeded)} <= {b_unseeded} unseeded draw site(s))")
    if len(unarmed) < b_unarmed:
        print(f"  the mutation ratchet can be lowered to {len(unarmed)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
