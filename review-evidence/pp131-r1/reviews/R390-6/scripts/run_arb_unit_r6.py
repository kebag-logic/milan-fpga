#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R390-6: the reviewer's arbiter unit probe (carried from R390-4/R390-5) at the
head, against the R390-5 edits, the tree's two new N11d controls, and the three
manager-0 WRITE/stale-intent halves the tb/acmp_nvm README lists as ungraded
(reviewer's own texts, one per README row), each in its own scratch copy.
The point is to check the README's "out-of-tree probe" column: which of the
five manager-0 halves the unit probe kills, and with which case.
Usage: run_arb_unit_r6.py <tree> <scratch-dir> <verilator>"""
import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

tree, scratch, vl = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
here = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("d3", tree / "tb/pp_top/d3_mutants.py")
d3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d3)
spec = importlib.util.spec_from_file_location("r5x", here / "r5_extra_mutants.py")
r5x = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r5x)
ARB = "hdl/packet_engine/KL_pp_nvm_mgr_arb.sv"


def raw(a0_iss, a0_own):
    """Replace manager 0's two drain terms whole; manager 1's stay the head's."""
    return ((ARB, d3.ARMS,
             f"  assign arm0_w = ({a0_iss})\n"
             f"                  || ({a0_own});\n"
             "  assign arm1_w = (iss1_w && !m1_we_i && m1_abort_i)\n"
             "                  || ((own_r == O_M1) && !we_r && m1_abort_i);\n"),)


ISS0 = "iss0_w && !m0_we_i && m0_abort_i"
OWN0 = "(own_r == O_M0) && !we_r && m0_abort_i"
runs = {"head": ()}
runs.update(r5x.edits(d3))
for name in ("issue_arm_cross_intent", "owned_arm_cross_intent", "cross_own_m1_drains_m0"):
    runs[name] = next(m.edits for m in d3.MUTANTS if m.name == name)
# the README's manager-0 rows 3-5 (rows 1-2 are r5_issue_cross_m1_only and
# r5_owned_cross_m1_only above)
runs["r6_write_iss_m0_only"] = raw("iss0_w && m0_abort_i", OWN0)
runs["r6_write_own_m0_only"] = raw(ISS0, "(own_r == O_M0) && m0_abort_i")
runs["r6_stale_we_m0_only"] = raw("iss0_w && !we_r && m0_abort_i", OWN0)
for name, edits in runs.items():
    copy = scratch / name
    shutil.rmtree(copy, ignore_errors=True)
    (copy / "hdl/packet_engine").mkdir(parents=True)
    shutil.copy(tree / ARB, copy / "hdl/packet_engine/")
    assert d3.plant(copy, edits) == "", name
    out = subprocess.run(["sh", str(here / "arb_unit/run_arb_unit.sh"), str(copy),
                          str(copy / "build"), vl], capture_output=True, text=True).stdout
    tally = [l for l in out.splitlines() if "checks" in l.lower() or l.startswith("rc=")]
    fails = [l for l in out.splitlines() if l.startswith("FAIL")]
    print(f"== {name}: {' | '.join(tally)}")
    for f in fails:
        print("   " + f[:180])
