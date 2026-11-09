#!/usr/bin/env python3
"""self-probes.py <tree> <out>: one-edit probes of the round's new KL_srp_vlan lines, each planted in a scratch copy
of <tree> (hdl/, tb/common, tb/srp_encoder) and graded by the encoder suite; prints each probe's FAIL lines."""
import shutil, subprocess, sys, tempfile
from pathlib import Path
tree, out = Path(sys.argv[1]), Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
V = "hdl/srp/KL_srp_vlan.sv"
PROBES = {
    "valid-gate-only": [("  assign vlan_ev_valid_o = (st_r == W_PUSH) && !link_rise_w;\n",
                         "  assign vlan_ev_valid_o = (st_r == W_PUSH);\n")],
    "push-return-only": [("          if (link_rise_w) begin\n            st_r <= W_EVAL;\n          end else if (vlan_ev_ready_i) begin\n",
                          "          if (vlan_ev_ready_i) begin\n")],
    "registrar-rise-only": [("      if (link_ev_w)\n        reg_nx_w[i] = 1'b0;", "      if (link_rise_w)\n        reg_nx_w[i] = 1'b0;")],
    "registrar-fall-only": [("      if (link_ev_w)\n        reg_nx_w[i] = 1'b0;", "      if (link_ev_w && !link_rise_w)\n        reg_nx_w[i] = 1'b0;")],
    "begin-by-alloc": [("        app_ev_w[i] = active_r[i] ? SRP_AP_VN_C : SRP_AP_VO_C;\n",
                        "        app_ev_w[i] = alloc_r[i] ? SRP_AP_VN_C : SRP_AP_VO_C;\n")],
}
for name, edits in PROBES.items():
    with tempfile.TemporaryDirectory() as tmp:
        w = Path(tmp)
        shutil.copytree(tree / "hdl", w / "hdl")
        for n in ("common", "srp_encoder"):
            shutil.copytree(tree / "tb" / n, w / "tb" / n, ignore=shutil.ignore_patterns("obj_*"))
        p = w / V; t = p.read_text()
        for a, b in edits:
            assert t.count(a) == 1, (name, a)
            t = t.replace(a, b)
        p.write_text(t)
        r = subprocess.run(["make", "-C", str(w / "tb/srp_encoder")], capture_output=True, text=True)
        log = r.stdout + r.stderr
        (out / f"{name}.log").write_text(log)
        fails = [l for l in log.splitlines() if l.startswith("FAIL:")]
        tally = [l for l in log.splitlines() if "checks:" in l]
        print(f"{name}: rc={r.returncode} {tally[-1] if tally else 'no tally'}")
        for l in fails:
            print("   ", l[:150])
