#!/usr/bin/env python3
"""Reviewer-owned mutants (R307-1, PR #560) run through the lane's own
gsi_mutants.py machinery: plant in a COPY of the processor hdl/ tree, rebuild
the timed obj_notify leg through `make notify-build`, run it.

Run from a DISPOSABLE copy of tb/verilator/milan_dp (never a tracked checkout):
    python3 reviewer_mutants.py <milan_dp dir>
Each row states the expected outcome: "caught" (the named check must fail) or
"survives" (the parent leg is expected NOT to see it; this documents coverage,
it is not a defect claim by itself).
"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
import gsi_mutants as g  # noqa: E402

ROWS = [
    ("R1 status read from the other sink only",
     [("pp", "      gsi_status_w = lstn_gsi_status_r[gsi_sink_w];",
       "      gsi_status_w = lstn_gsi_status_r[gsi_sink_w ^ 1'b1];")],
     "[GSI] G2 sink 0 beside sink 1's refusal: acmp_status", "caught"),
    ("R2 listener-status notification raised on the other sink",
     [("pp", "          || lstn_gsi_changed_r[k]\n",
       "          || lstn_gsi_changed_r[k ^ 1]\n")],
     "[GSI] G1 sink 0 bound: unsolicited GET_STREAM_INFO(sink 0) to A", "caught"),
    ("R3 latency-only notification term dropped (processor #113)",
     [("pp", "          || srp_evt_tk_fail_chg_w[k] || srp_evt_tk_latency_chg_w[k];",
       "          || srp_evt_tk_fail_chg_w[k];")],
     None, "survives"),
]

ok = True
with tempfile.TemporaryDirectory(prefix="r307-mut-") as td:
    work = Path(td)
    for name, edits, check, expect in ROWS:
        tag = "".join(c if c.isalnum() else "_" for c in name)
        planted = g.plant(name, edits, work, tag)
        if planted is None:
            print(f"[FAIL] {name}: pattern did not match once"); ok = False; continue
        exe = g.build(planted[0], planted[1], work / f"obj_{tag}")
        if exe is None:
            print(f"[FAIL] {name}: did not build"); ok = False; continue
        rc, out = g.run_leg(exe)
        got = g.verdict(rc, out, check)
        fails = [ln.strip() for ln in out.splitlines() if ln.strip().startswith("[FAIL]")]
        tally = [ln for ln in out.splitlines() if ln.startswith("checks:")]
        print(f"[{ 'PASS' if (got == 'caught') == (expect == 'caught') and got in ('caught','pass') else 'FAIL'}] "
              f"{name}: expected {expect}, verdict {got}; {tally[-1] if tally else 'no tally'}")
        for ln in fails[:6]:
            print(f"      {ln}")
        if not ((got == "caught") == (expect == "caught") and got in ("caught", "pass")):
            ok = False
sys.exit(0 if ok else 1)
