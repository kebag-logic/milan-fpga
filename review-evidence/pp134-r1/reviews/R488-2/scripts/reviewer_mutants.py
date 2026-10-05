#!/usr/bin/env python3
"""Reviewer fault probes: plant one fault in a scratch export and print the tree.

usage: reviewer_mutants.py <repo> <tree> <fault>
faults:
  listener-only-restore  pre-fix order on the listener plane only (head talker kept)
  talker-only-restore    pre-fix order on the talker plane only (head listener kept)
  expiry-over-renewal    expiry branch moved ABOVE the registering branch, both planes
                         (a same-clock New/Join is lost and the registrar ends MT)
  lv-never-ends          the checked-in patch, run against the complete default suite
The tree is a `git archive HEAD` export; nothing in <repo> is written.
"""
import subprocess
import sys
from pathlib import Path

repo, tree, fault = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
srp = tree / "hdl" / "srp"
pre = "21c6f7096ac80007f723de59c6f717f55bd34cfc"   # merged main, pre-fix RTL


def blob(rev: str, path: str) -> str:
    return subprocess.run(["git", "-C", str(repo), "show", f"{rev}:{path}"],
                          check=True, capture_output=True, text=True).stdout


if fault == "listener-only-restore":
    (srp / "KL_srp_listener_fsm.sv").write_text(blob(pre, "hdl/srp/KL_srp_listener_fsm.sv"))
elif fault == "talker-only-restore":
    (srp / "KL_srp_talker_fsm.sv").write_text(blob(pre, "hdl/srp/KL_srp_talker_fsm.sv"))
elif fault == "expiry-over-renewal":
    for name, reg_head in (("KL_srp_talker_fsm.sv",
                            "        if (reg_rx_hit_w[s] && ((evt_mrp_event_i == 3'(SRP_EV_NEW))\n"),
                           ("KL_srp_listener_fsm.sv",
                            "        if (reg_rx_hit_w[s] && rx_registering_w) begin\n")):
        p = srp / name
        t = p.read_text()
        start = t.index("        end else if (exp_hit_w && (exp_idx_w == s)\n")
        end = t.index("        end else if (reg_rx_hit_w[s]", start)
        body = t[start:end]                       # "end else if (exp...) begin ... "
        t = t[:start] + t[end:]
        head_at = t.index(reg_head)
        cond = body.replace("        end else if ", "        if ", 1)
        t = t[:head_at] + cond + t[head_at:].replace("        if (reg_rx_hit_w[s]", "        end else if (reg_rx_hit_w[s]", 1)
        p.write_text(t)
elif fault == "lv-never-ends":
    subprocess.run(["git", "apply", str(repo / "tb/srp_top/mutations/lv-never-ends.patch")],
                   cwd=tree, check=True)
else:
    sys.exit(f"unknown fault {fault}")
subprocess.run(["diff", "-ru", "--label", "head", "--label", fault,
                str(repo / "hdl" / "srp"), str(srp)], check=False)
