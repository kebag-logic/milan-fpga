#!/usr/bin/env python3
"""Scratch unit-suite mutant runner (not part of the repo)."""
import json, shutil, subprocess, sys
from pathlib import Path
LANE = Path(sys.argv[1]); OUT = Path(sys.argv[2]); V = sys.argv[3]
only = sys.argv[4].split(",") if len(sys.argv) > 4 else None
SRP = "hdl/srp/KL_srp_listener_fsm.sv"
LST = "hdl/acmp/KL_pp_acmp_listener.sv"
M = [
 ("srp-fchg-redeclares", "srp_stream_fsms", SRP,
  "&& ((reg_r[s] == R_MT_C) || (rtype_r[s] != rx_is_failed_w));",
  "&& ((reg_r[s] == R_MT_C) || (rtype_r[s] != rx_is_failed_w) || ind_fchg_w[s]);"),
 ("srp-fchg-strobe-removed", "srp_stream_fsms", SRP,
  "if (ind_fchg_w[s]) evt_tk_fail_chg_o[s]   <= 1'b1;",
  "if (1'b0) evt_tk_fail_chg_o[s]   <= 1'b1;"),
 ("srp-fchg-compare-sink0", "srp_stream_fsms", SRP,
  "fchg_ix_w  = SNK_W_C'(s);", "fchg_ix_w  = '0;"),
 ("srp-fchg-any-hit", "srp_stream_fsms", SRP,
  "fchg_cand_w[s] = reg_rx_hit_w[s] && (reg_r[s] != R_MT_C) && rtype_r[s];",
  "fchg_cand_w[s] = reg_rx_hit_w[s];"),
 ("srptop-fchg-redeclares", "srp_top", SRP,
  "&& ((reg_r[s] == R_MT_C) || (rtype_r[s] != rx_is_failed_w));",
  "&& ((reg_r[s] == R_MT_C) || (rtype_r[s] != rx_is_failed_w) || ind_fchg_w[s]);"),
 ("lstn-rebind-excluded", "acmp_listener", LST,
  "act_strt_chg_o <= cellmut_r && bnd_was_r && rec_r.f_bound\n",
  "act_strt_chg_o <= cellmut_r && bnd_was_r && rec_r.f_bound\n                            && !apend_r[ACT_A2_C]\n"),
]
res = []
for name, suite, rel, old, new in M:
    if only and name not in only: continue
    t = OUT / name
    shutil.rmtree(t, ignore_errors=True)
    for d in ("hdl", "tb/common", "tb/" + suite):
        shutil.copytree(LANE / d, t / d, ignore=shutil.ignore_patterns("obj*"))
    f = t / rel; s = f.read_text()
    assert s.count(old) == 1, (name, s.count(old))
    f.write_text(s.replace(old, new))
    log = OUT / (name + ".log")
    with log.open("w") as o:
        rc = subprocess.run(["make", "VERILATOR=" + V], cwd=t / "tb" / suite,
                            stdout=o, stderr=subprocess.STDOUT, timeout=1800).returncode
    txt = log.read_text()
    fails = [l for l in txt.splitlines() if l.startswith("FAIL")]
    tally = [l for l in txt.splitlines() if "checks:" in l]
    r = {"mutant": name, "suite": suite, "rc": rc, "tally": tally, "fails": fails}
    print(json.dumps(r), flush=True); res.append(r)
    shutil.rmtree(t, ignore_errors=True)
(OUT / "results.json").write_text(json.dumps(res, indent=2) + "\n")
