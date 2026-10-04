#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer-owned disposable fault probes for processor PR #155 (milan-fpga #639).

Each probe copies a pristine extract of the reviewed head (ROOT), plants one exact
textual edit (the old text must occur exactly once) or swaps in a file from another
extract, builds the named suite with the given Verilator, runs it, and records the
exit code and the section tallies. Nothing outside OUTPUT is written.

Usage: python3 probes.py --root HEAD_EXTRACT --main MAIN_EXTRACT --output DIR
                         --verilator V [--jobs N] [--only NAME ...]
"""

import argparse
import concurrent.futures
import json
from pathlib import Path
import re
import shutil
import subprocess

TOP = "hdl/top/protocol_processor_top.sv"
LISTENER = "hdl/acmp/KL_pp_acmp_listener.sv"
STORE = "      if (armq_push_ok_w[g]) mem_r[wr_ix_w] <= armq_in_w[g];\n"
DROP = "          if (arm_drop_r != 16'hFFFF) arm_drop_r <= arm_drop_r + 16'd1;\n"
PICK = "      if ((armq_pop_w == '0) && (armq_cnt_r[i] != 3'd0)) begin\n"
HD_RST = "      armq_hd_r  <= '0;\n"
REC_WRITE = "      rec_ram_r[recwr_addr_w] <= recwr_data_w;\n"

AQ_RUN = (("make", "gsi-build"), ("./obj_dir/Vpp_top_sim", "--arm-queue-only"), "tb/pp_top")
LSN_RUN = ((), ("make", "run"), "tb/acmp_listener")


def store_without(bit: int) -> str:
    """The ring write with one arm bit never stored (bit 0 = deadline LSB)."""
    return (f"      if (armq_push_ok_w[g]) mem_r[wr_ix_w] <= armq_in_w[g]"
            f" & ~(ARM_W_C'(1) << {bit});\n")


# name, run, edits (path, old, new) or ("swap", path) from --main, expectation, why.
# Expectations: PASS / FAIL as for a golden or a control; GAP = a real fault the committed
# checks cannot see (the finding's evidence); EQUIV = no behaviour change at any shape.
PROBES = [
    ("aq_golden_head", AQ_RUN, [], "PASS", "the head as published"),
    ("aq_main_rtl", AQ_RUN, [("swap", TOP)], "PASS",
     "head bench on main b0a7419's top (the shift queue): AQ grades kept behaviour"),
    ("aq_hd_not_reset", AQ_RUN, [(TOP, HD_RST, "")], "PASS",
     "equivalent: with the count reset, any head index is a valid empty ring"),
    ("aq_drop_per_face", AQ_RUN,
     [(TOP, DROP, "          if (arm_drop_r != 16'hFFFF) arm_drop_r <= arm_drop_r + 16'd1;\n"
                  "          if (i == 7 && armq_in_vld_w[0] && !armq_push_ok_w[0]"
                  " && armq_in_vld_w[7] && !armq_push_ok_w[7]"
                  " && arm_drop_r < 16'hFFFE) arm_drop_r <= arm_drop_r + 16'd2;\n")],
     "PASS", "EQUIVALENT by construction: face 0 drains first every clock, so it never"
             " holds more than one arm and can never drop; kept as the record of a probe"
             " that could not fire"),
    ("aq_drop_two_faces_count_two", AQ_RUN,
     [(TOP, DROP, "          if (arm_drop_r != 16'hFFFF) arm_drop_r <= arm_drop_r + 16'd1;\n"
                  "          if (i == 7 && armq_in_vld_w[6] && !armq_push_ok_w[6]"
                  " && arm_drop_r < 16'hFFFE) arm_drop_r <= arm_drop_r + 16'd2;\n")],
     "FAIL", "faces 6 and 7 (notify, notify monitor) dropping in one clock count two"),
    ("aq_priority_reversed", AQ_RUN,
     [(TOP, PICK, "      if (((armq_pop_w == '0) || (i > 0)) && (armq_cnt_r[i] != 3'd0)) begin\n"
                  "        armq_pop_w = '0;\n")],
     "FAIL", "the last non-empty face drains first"),
    ("aq_cancel_unstored", AQ_RUN, [(TOP, STORE, "      if (armq_push_ok_w[g]) mem_r[wr_ix_w] <="
                                                 " {1'b0, armq_in_w[g][ARM_W_C-2:0]};\n")],
     "FAIL", "the cancel bit (MSB) is never stored in the ring"),
    ("aq_deadline_bit0_unstored", AQ_RUN, [(TOP, STORE, store_without(0))], "FAIL",
     "deadline bit 0 never stored"),
    ("aq_deadline_bit21_unstored", AQ_RUN, [(TOP, STORE, store_without(21))], "GAP",
     "deadline bit 21 never stored"),
    ("aq_deadline_bit22_unstored", AQ_RUN, [(TOP, STORE, store_without(22))], "GAP",
     "deadline bit 22 never stored"),
    ("aq_deadline_bit31_unstored", AQ_RUN, [(TOP, STORE, store_without(31))], "GAP",
     "deadline bit 31 never stored"),
    ("lsn_golden_head", LSN_RUN, [], "PASS", "the head as published"),
    ("lsn_main_rtl", LSN_RUN, [("swap", LISTENER)], "PASS",
     "head bench on main b0a7419's listener (the read register): RS grades kept behaviour"),
    ("lsn_rec_bit367_unstored", LSN_RUN,
     [(LISTENER, REC_WRITE, "      rec_ram_r[recwr_addr_w] <= recwr_data_w"
                            " & ~(ACMP_REC_W_C'(1) << 367);\n")],
     "EQUIV", "sm_tmr_handle MSB (record bit 367) never stored; informational only:"
              " the handle holds a timer slot index, and the top's TMR_AW_C is 7 at 8x8,"
              " so bit 7 is never set at the shipped shapes"),
]

TALLY = re.compile(r"^(AQ[^\n]*|RS[^\n]*FAIL[^\n]*|\d+ checks[^\n]*|FAIL[^\n]*|"
                   r"\[build[^\n]*)$", re.M)


def plant(tree: Path, main: Path, edits) -> None:
    for edit in edits:
        if edit[0] == "swap":
            shutil.copyfile(main / edit[1], tree / edit[1])
            continue
        path, old, new = edit
        text = (tree / path).read_text()
        if text.count(old) != 1:
            raise SystemExit(f"{path}: anchor occurs {text.count(old)} times: {old!r}")
        (tree / path).write_text(text.replace(old, new))


def run_probe(probe, args) -> dict:
    name, (build, run, suite), edits, expect, why = probe
    work = Path(args.output) / name
    if work.exists():
        shutil.rmtree(work)
    shutil.copytree(args.root, work / "tree", symlinks=True,
                    ignore=shutil.ignore_patterns("obj*", "*.hex", "__pycache__"))
    plant(work / "tree", Path(args.main), edits)
    env_v = f"VERILATOR={args.verilator}"
    log = work / "log.txt"
    rc_build = 0
    with log.open("w") as out:
        cwd = work / "tree" / suite
        if build:
            rc_build = subprocess.run(list(build) + [env_v], cwd=cwd, stdout=out,
                                      stderr=subprocess.STDOUT).returncode
        if rc_build == 0:
            cmd = list(run) + ([env_v] if run[0] == "make" else [])
            rc = subprocess.run(cmd, cwd=cwd, stdout=out, stderr=subprocess.STDOUT).returncode
        else:
            rc = -1
    text = log.read_text(errors="replace")
    lines = [m.group(0) for m in TALLY.finditer(text)]
    shutil.rmtree(work / "tree")
    verdict = "BUILD-FAIL" if rc_build else ("PASS" if rc == 0 else "FAIL")
    rec = {"probe": name, "expect": expect, "verdict": verdict, "rc": rc,
           "why": why, "lines": lines[-12:]}
    (work / "result.json").write_text(json.dumps(rec, indent=1) + "\n")
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--main", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--verilator", required=True)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--only", nargs="*")
    args = ap.parse_args()
    chosen = [p for p in PROBES if not args.only or p[0] in args.only]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(lambda p: run_probe(p, args), chosen))
    for r in results:
        print(json.dumps({k: r[k] for k in ("probe", "expect", "verdict", "rc")}), flush=True)
    (Path(args.output) / "results.json").write_text(json.dumps(results, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
