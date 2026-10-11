#!/usr/bin/env python3
"""Disposable probe (R570-4): repair the pre-existing dev gap in
tb/verilator/milan_dp/test_sim_pool.py (LEGACY_LEGS lacks the #658 dynmap leg)
in a SCRATCH clone, then run only the Makefile-inventory arm, so the remaining
verdict is attributable to the revision under test.

Usage: python3 -I probe_sim_pool_dynmap.py <scratch clone root>
"""
import subprocess, sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
test = root / "tb/verilator/milan_dp/test_sim_pool.py"
text = test.read_text()
anchor = ('     "./obj_crflic/Vmilan_dp_crflic"),\n')
add = ('    ("---- #658 the power-on audio maps, Milan 5.4.2.7 and a restored format ----",\n'
       '     "./obj_dynmap/Vmilan_dp_dynmap"),\n')
if add not in text:
    assert text.count(anchor) == 1, "anchor not unique"
    text = text.replace(anchor, anchor + add)
    test.write_text(text)
driver = ("import sys; sys.path.insert(0, %r); import test_sim_pool as t\n"
          "try:\n    t.arm_the_makefile_hands_the_runner_the_recipes_ordinary_legs(); print('[PASS] makefile arm')\n"
          "except Exception as e:\n    print('[FAIL] makefile arm:', type(e).__name__, str(e)[:300]); sys.exit(1)\n"
          % str(test.parent))
sys.exit(subprocess.run([sys.executable, "-c", driver], cwd=test.parent).returncode)
