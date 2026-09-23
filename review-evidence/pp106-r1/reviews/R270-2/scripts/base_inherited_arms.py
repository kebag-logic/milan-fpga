#!/usr/bin/env python3
"""Plant the three surviving head arms (B3, C1, C2) in their base-fbc1f715
spelling, to show the gap is inherited. usage: <base-export> <out-dir>"""
import os, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mutation_probes as mp

ARMS = [
    ("B3-base", [("hdl/srp/KL_srp_top.sv",
      ".leaveall_tick_i (dec_la_mvrp_w || p_la_mvrp_r),",
      ".leaveall_tick_i (dec_la_mvrp_w || dec_la_msrp_w || p_la_mvrp_r),")]),
    ("C1-base", [("hdl/srp/KL_srp_talker_fsm.sv",
      "  assign leaveall_any_w = leaveall_rx_i || leaveall_own_i;\n",
      "  assign leaveall_any_w = leaveall_rx_i;\n")]),
    ("C2-base", [("hdl/srp/KL_srp_listener_fsm.sv",
      "  assign leaveall_any_w = leaveall_rx_i || leaveall_own_i;\n",
      "  assign leaveall_any_w = leaveall_rx_i;\n")]),
]
src, out = sys.argv[1], sys.argv[2]
for aid, subs in ARMS:
    work = os.path.join(out, aid)
    shutil.rmtree(work, ignore_errors=True)
    shutil.copytree(src, work, symlinks=True)
    for rel, old, new in subs:
        p = os.path.join(work, rel)
        t = open(p).read()
        assert t.count(old) == 1, (aid, rel, t.count(old))
        open(p, "w").write(t.replace(old, new))
    parts = []
    for s in mp.ALL:
        rc, n, nf, fails, tail = mp.run_suite(work, s)
        parts.append(f"{s}={nf}/{n}" if n is not None else f"{s}=NO-TALLY(rc={rc})")
    print(f"fbc1f715 {aid}: {' '.join(parts)}")
    sys.stdout.flush()
    shutil.rmtree(work, ignore_errors=True)
