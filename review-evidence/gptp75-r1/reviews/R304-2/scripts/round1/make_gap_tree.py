#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Build a disposable probe tree whose engine harness adds the two negative
lifecycle cases R304-1 finds untested: an idle Sync receipt timeout followed by
an in-band pair, and a return from mastership whose first pair is in-band.
Both must leave phc_slew_active_o low. Only the copied harness is edited.

usage: make_gap_tree.py HEAD_EXPORT OUT_TREE
"""
import shutil
import sys
from pathlib import Path

src, dst = Path(sys.argv[1]), Path(sys.argv[2])
if dst.exists():
    shutil.rmtree(dst)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns("obj_dir", "seedrun",
                                                         "syncseedrun"))
f = dst / "tb/verilator/engine/sim_main.cpp"
t = f.read_text(encoding="utf-8")

a_old = ('    expect("slew: tracking includes a nonzero frequency trim", '
         'phc_adj != 0, 1);\n')
a_new = a_old + (
    '    // R304 probe A: an idle Sync receipt timeout, then ordinary tracking.\n'
    '    run_svc(800000);\n'
    '    expect("probeA: idle timeout clears sync-ok", '
    'dut->pub_flags_o & FL_SYNCOK, 0);\n'
    '    expect("probeA: idle timeout leaves the level low", '
    'dut->phc_slew_active_o, 0);\n'
    '    slew_probe("probeA: in-band pair after idle timeout stays inactive", '
    '0, false);\n'
    '    slew_probe("probeA: second in-band pair stays inactive", 0, false);\n')
b_old = ('    slew_probe("slew: return from GM uses locked slew", 50000, true);\n')
b_new = (
    '    // R304 probe B: the first pair after mastership is in-band.\n'
    '    slew_probe("probeB: in-band return from GM stays inactive", 0, false);\n'
    ) + b_old
for old, new in ((a_old, a_new), (b_old, b_new)):
    assert t.count(old) == 1, old
    t = t.replace(old, new)
f.write_text(t, encoding="utf-8")
print(f"probe tree ready: {dst}")
