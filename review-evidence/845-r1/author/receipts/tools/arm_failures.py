#!/usr/bin/env python3
"""Run one unb_mutants.py arm through the driver's own plant, build, run and verdict, and print every line the
mutated leg marked [FAIL], so a catch is read by name rather than from a count.

usage: arm_failures.py <milan_dp dir> <1-based arm> <log>
"""
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
milan, arm, log = Path(sys.argv[1]).resolve(), int(sys.argv[2]), Path(sys.argv[3])
sys.path.insert(0, str(milan))
import unb_mutants as unb  # noqa: E402

mutation = unb.MUTATIONS[arm - 1]
original = unb.run_leg
seen = {}


def recording_run_leg(exe):
    """The driver's run_leg, keeping what it returned."""
    rc, out = original(exe)
    seen.update(rc=rc, out=out)
    return rc, out


unb.run_leg = recording_run_leg
with tempfile.TemporaryDirectory(prefix="unb-arm-") as td:
    caught = unb.run_mutant(mutation, Path(td))
log.write_text(seen.get("out", ""))
lines = seen.get("out", "").splitlines()
fails = [line.strip() for line in lines if line.strip().startswith("[FAIL]")]
print(f"arm {arm}: {mutation.name}")
print(f"driver verdict: {'caught' if caught else 'NOT caught'}; leg rc {seen.get('rc')}")
print(f"[FAIL] lines in the mutated leg: {len(fails)}")
print(*fails, sep="\n")
for hold in mutation.holds:
    print(f"hold {'[ok]' if unb.marked(seen.get('out', ''), '[ok]', hold) else 'MISSING'}: {hold}")
for line in lines:
    if line.strip().startswith("checks:"):
        print(line.strip())
sys.exit(0 if caught else 1)
