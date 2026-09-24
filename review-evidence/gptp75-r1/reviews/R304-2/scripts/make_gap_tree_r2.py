#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R304-2 probe tree: add the inactive direction of the asCapable-loss edge.

While phc_slew_active_o is low (ordinary tracking), asCapable is lost through
bad Pdelay responses, held lost, then recovered; the first consumed pairs after
recovery are in-band and must leave the level low. Only the copied harness is
edited; the reviewed clone is never touched.

usage: make_gap_tree_r2.py HEAD_EXPORT OUT_TREE
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

old = ('    expect("slew: tracking includes a nonzero frequency trim", '
       'phc_adj != 0, 1);\n')
new = old + (
    '    // R304-2 probe C: lose asCapable while inactive, recover, track.\n'
    '    {\n'
    '      const size_t c_edges = slew_edges.size();\n'
    '      pd_mode = PD_FAR;\n'
    '      expect("probeC: bad delay drops asCapable while inactive", '
    'wait_flags(FL_ASCAP, 0, 2500000), 1);\n'
    '      run_svc(200000);\n'
    '      expect("probeC: incapable and inactive", '
    'dut->phc_slew_active_o, 0);\n'
    '      pd_mode = PD_NORMAL;\n'
    '      expect("probeC: capability recovers", '
    'wait_flags(FL_ASCAP, FL_ASCAP, 5000000), 1);\n'
    '      expect("probeC: recovery has no level edge", '
    'slew_edges.size(), c_edges);\n'
    '      announce(0x75C0, 100, GMID, 0, PEER_CID);\n'
    '      slew_probe("probeC: in-band pair after asCapable recovery stays '
    'inactive", 0, false, false, true);\n'
    '      slew_probe("probeC: second in-band pair after recovery stays '
    'inactive", 0, false);\n'
    '    }\n')
assert t.count(old) == 1, old
t = t.replace(old, new)
f.write_text(t, encoding="utf-8")
print(f"probe tree ready: {dst}")
