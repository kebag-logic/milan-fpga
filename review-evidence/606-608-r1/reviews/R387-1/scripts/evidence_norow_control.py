#!/usr/bin/env python3
"""Negative control: run scripts/measure_test_evidence.py --check from the
repository root with the retry_mutants.py disposition row removed IN MEMORY
(the tracked file is never written). Expected: rc 1 and one unexplained
DUT-source reader."""
import sys
from pathlib import Path

p = Path("scripts/measure_test_evidence.py").resolve()
src = p.read_text()
row = ('    "protocol-processor/tb/acmp_talker/retry_mutants.py":\n'
       '        "mutation campaign; plants named defects in a scratch copy and requires named assertion "\n'
       '        "failures from completed cycle-bounded simulations; reads no expected behavior from RTL",\n')
assert src.count(row) == 1
sys.argv = [str(p), "--check"]
exec(compile(src.replace(row, ""), str(p), "exec"), {"__name__": "__main__", "__file__": str(p)})
