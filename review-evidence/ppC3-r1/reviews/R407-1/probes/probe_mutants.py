#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer probes (disposable): plant one RTL edit in a scratch copy and run a suite.

  domain-fresh  : TK_DISCOVERED's fresh-index branch additionally requires the
                  domain to match (the domain analogue of the campaign's
                  disc-fresh-checks-gm arm); run tb/adp_engine.
  gate-full     : the campaign's gate-enable-dropped patch, run on the FULL
                  default tb/pp_top (the README's "3 of 7,766" claim).
Usage: probe_mutants.py <clone> <scratch-root> <probe>
"""
import shutil
import subprocess
import sys
from pathlib import Path

clone, root, probe = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
tree = root / probe
if tree.exists():
    shutil.rmtree(tree)
for sub in ("hdl", "tb/common", "tb/adp_engine", "tb/pp_top"):
    shutil.copytree(clone / sub, tree / sub,
                    ignore=shutil.ignore_patterns("obj_*", "__pycache__"))
if probe == "domain-fresh":
    f = tree / "hdl/adp/KL_adp_engine.sv"
    old = "          if (rx_aidx_r > rec_aidx_w) begin\n"
    new = ("          if ((rx_aidx_r > rec_aidx_w)\n"
           "              && (rx_dom_r == dom_slice_f(rxq_if_r))) begin\n")
    text = f.read_text()
    assert text.count(old) == 1, "anchor drifted"
    f.write_text(text.replace(old, new))
    target = ["make", "-C", str(tree / "tb/adp_engine")]
elif probe == "gate-full":
    subprocess.run(["git", "apply", str(clone / "tb/adp_engine/mutations/gate-enable-dropped.patch")],
                   cwd=tree, check=True)
    target = ["make", "-C", str(tree / "tb/pp_top")]
else:
    sys.exit(f"unknown probe {probe}")
print("planted", probe, "in", tree, flush=True)
rc = subprocess.run(target).returncode
print(f"probe {probe}: suite rc={rc}")
