#!/usr/bin/env python3
"""Reviewer probe: dev 46c971fa's #851 arm alone (the encoder's value search
tied to a miss, no doubled intake) at the head's processor pin; the PR says it
now survives the crflic leg. Exit 0 when it SURVIVES (the leg passes).
usage: <repo> [work-dir]"""
import sys, tempfile
from pathlib import Path
repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / "tb/verilator/milan_dp"))
import crflic_mutants as cm  # noqa: E402
mut = ("reviewer probe: dev's #851 arm alone, the encoder never merges",
       [("srp/KL_srp_encoder.sv",
         "  assign sr_hit_w    = sr_cont_w && (q_key_w == sr_key_r);",
         "  assign sr_hit_w    = 1'b0;")],
       "no DUT MRPDU carries one attribute value in two VectorAttributes")
with tempfile.TemporaryDirectory(prefix="r831-851enc-", dir=sys.argv[2] if len(sys.argv) > 2 else None) as td:
    caught = cm.run_pp_mutant(mut, Path(td))
print("RESULT:", "CAUGHT" if caught else "NOT CAUGHT (survives or not evidence; see above)", flush=True)
sys.exit(1 if caught else 0)
