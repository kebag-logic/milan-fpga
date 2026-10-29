"""Summarise an engine mutation-arm log: verdict counts, and for each control
whose named checks carry a strict prefix, the FAIL lines it printed.

usage: arm_summary.py <arm log> [<prefix> ...]
"""
import re
import sys
from pathlib import Path

lines = Path(sys.argv[1]).read_text(errors="replace").splitlines()
prefixes = tuple(sys.argv[2:]) or ("#94 ",)
caught = [l for l in lines if l.startswith("[PASS] mutant caught")]
failed = [l for l in lines if l.startswith("[FAIL]")]
control = [l for l in lines if l.startswith("[PASS] the unmutated")]
tally = [l for l in lines if re.match(r"^\d+ checks: \d+ PASS, \d+ FAIL", l)]
print(f"caught {len(caught)}, failed {len(failed)}, control {len(control)}, tally {tally[-1] if tally else None}")
pending = []
for l in lines:
    if l.startswith("FAIL "):
        pending.append(l)
    elif l.startswith("[PASS] mutant caught") or l.startswith("[FAIL]"):
        m = re.search(r'breaks "(.*)"$', l)
        breaks = m.group(1) if m else ""
        if breaks.startswith(prefixes):
            print(l)
            for f in pending:
                print("   ", f)
        pending = []
for l in failed:
    print("FAILED:", l)
