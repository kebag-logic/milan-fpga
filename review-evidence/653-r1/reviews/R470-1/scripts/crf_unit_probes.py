#!/usr/bin/env python3
"""Reviewer probes: plant defects in a copy of KL_crf_rx.sv and run the
crf_rx unit harness against each; report which checks fail.

usage: crf_unit_probes.py <tree at the head under review> <work dir>
Each probe runs `make unit RX_RTL=<mutant>` in its own copy of
tb/verilator/crf_rx (same depth, so the Makefile's relative paths hold).
The tree's own files are never edited.  Exit 0 when every probe made the
unit harness report at least one failure (a crash or build failure is not
counted as a catch)."""
import concurrent.futures as cf
import re
import shutil
import subprocess
import sys
from pathlib import Path

TREE = Path(sys.argv[1]).resolve()
WORK = Path(sys.argv[2]).resolve()
RTL = TREE / "hdl/ieee1722/crf/KL_crf_rx.sv"
FALL = "      if (w_bind_fall_w && locked_o) begin\n"
PROBES = {
    # the arm removed: the dev behaviour
    "p1_no_fall_arm": [(FALL, "      if (1'b0) begin\n")],
    # every unbind counts, locked or not
    "p2_count_unlocked_unbind": [(FALL, "      if (w_bind_fall_w) begin\n")],
    # the lock is kept, so the timeout counts again
    "p3_keep_lock": [(FALL + "        locked_o       <= 1'b0;\n", FALL)],
    # no Table 5.22 pulse
    "p4_no_dirty": [("        cnt_unlocked_o <= cnt_unlocked_o + 32'd1;\n        dirty_p_o      <= 1'b1;\n      end\n\n      //! not-bound -> bound",
                     "        cnt_unlocked_o <= cnt_unlocked_o + 32'd1;\n      end\n\n      //! not-bound -> bound")],
    # the unbind also counts a STREAM_INTERRUPTED
    "p5_count_intr": [(FALL, FALL + "        cnt_intr_o     <= cnt_intr_o + 32'd1;\n")],
    # a same-edge timeout and unbind count twice
    "p6_same_edge_double": [(FALL + "        locked_o       <= 1'b0;\n        cnt_unlocked_o <= cnt_unlocked_o + 32'd1;\n",
                             FALL + "        locked_o       <= 1'b0;\n        cnt_unlocked_o <= cnt_unlocked_o + ((!w_acc_run_w && tout_r == TOUT_CYC_C[$clog2(TOUT_CYC_C+1)-1:0]) ? 32'd2 : 32'd1);\n")],
    # the unlock is counted one cycle late (on the cycle after the fall)
    "p7_also_drops_lockcount": [(FALL + "        locked_o       <= 1'b0;\n",
                                 FALL + "        locked_o       <= 1'b0;\n        cnt_locked_o   <= cnt_locked_o - 32'd1;\n")],
}


def run(name, edits):
    text = RTL.read_text()
    for old, new in edits:
        n = text.count(old)
        if n != 1:
            return name, f"PATTERN-COUNT {n}", []
        text = text.replace(old, new)
    d = TREE / "tb/verilator" / f"crf_rx_probe_{name}"
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(TREE / "tb/verilator/crf_rx", d,
                    ignore=shutil.ignore_patterns("obj_*"))
    mut = WORK / f"KL_crf_rx_{name}.sv"
    mut.write_text(text)
    out = subprocess.run(["make", "unit", f"RX_RTL={mut}"], cwd=d,
                         capture_output=True, text=True, check=False)
    log = out.stdout + out.stderr
    (WORK / f"{name}.log").write_text(log)
    fails = [l.strip() for l in log.splitlines() if l.strip().startswith("[FAIL]")]
    m = re.search(r"KL_crf_rx: (\d+) checks, (\d+) failures", log)
    tally = m.group(0) if m else f"NO TALLY rc={out.returncode}"
    shutil.rmtree(d)
    return name, tally, fails


WORK.mkdir(parents=True, exist_ok=True)
ok = True
with cf.ThreadPoolExecutor(max_workers=4) as ex:
    for name, tally, fails in ex.map(lambda kv: run(*kv), PROBES.items()):
        caught = tally.startswith("KL_crf_rx") and not tally.endswith(" 0 failures") and fails
        ok &= bool(caught)
        print(f"== {name}: {tally} -> {'CAUGHT' if caught else 'NOT CAUGHT'}")
        for f in fails[:12]:
            print("   " + f[:200])
sys.exit(0 if ok else 1)
