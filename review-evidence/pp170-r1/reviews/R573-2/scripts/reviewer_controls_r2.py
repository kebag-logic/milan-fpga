#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer-planted name controls for processor PR #172 (issue #170), round 2.

Each control is written by the reviewer from the RTL or the bench, independently
of the author's mutation tables. It copies the four source directories the name
bench builds from into an isolated tree, plants one exact edit, and runs the
bench's normal entry point (both synthetic populations at their bound name
capacity, 39 and 107, then both again at 128). A control is KILLED only if the
run completed (four per-run tallies plus the combined tally), returned 1, and
EVERY required pattern matches at least one FAIL line (a pattern ending in an
ordinal matches that ordinal alone). INFO controls are reported, not graded.

usage: reviewer_controls_r2.py --root CLONE --output NEWDIR --verilator PATH [--jobs N]
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

WRITER = "hdl/aecp/KL_aecp_nvm_writer.sv"
TOP = "hdl/top/protocol_processor_top.sv"
GUARD = "hdl/aecp/KL_aecp_desc_mem_guard.sv"
BENCH = "tb/name_state/sim_main.cpp"

# (name, file, old, new, required patterns, graded)
CONTROLS = (
    # round-1 controls, rerun at the new geometry
    ("R_trigger_odd_dropped", WRITER,
     "    if (nchg_i && (32'(nchg_ord_i) < N_NAME_P)) begin\n",
     "    if (nchg_i && (32'(nchg_ord_i) < N_NAME_P) && !nchg_ord_i[0]) begin\n",
     (r"N3 saved ordinal 1(?!\d)",), True),
    ("R_record_id_neighbour", WRITER,
     "  assign hrid_w  = sel_base_f(hsel_w) + 8'(hidx_w);\n",
     "  assign hrid_w  = sel_base_f(hsel_w) + 8'((hsel_w == GRP_NAME_C) ? (hidx_w ^ 16'd1) : hidx_w);\n",
     (r"N3 saved ordinal \d+",), True),
    ("R_empty_replay_skipped", WRITER,
     "  assign sb_we_o    = !done_r && ((ws_r == W_APPLY) || (ws_r == W_NAPPLY));\n",
     "  assign sb_we_o    = !done_r && ((ws_r == W_APPLY)\n"
     "                                  || ((ws_r == W_NAPPLY) && (nb_rlane_w != 64'd0)));\n",
     (r"N5 restored ordinal 2(?!\d)",), True),
    ("R_pending_clears_higher", WRITER,
     "    if (done_ok_w || giveup_w) clr_w[hand_r] = 1'b1;\n",
     "    if (done_ok_w || giveup_w)\n"
     "      for (int unsigned i = 0; i < N_REC_C; i++) if (i >= 32'(hand_r)) clr_w[i] = 1'b1;\n",
     (r"N6 pending:",), True),
    ("R_replay_skips_locate_wait", WRITER,
     "        W_IMGLOC: begin\n          if (sb_rvalid_i) begin",
     "        W_IMGLOC: begin\n          if (1'b1) begin",
     (r"D3N7:",), True),
    ("R_latch_lane_alias", WRITER,
     "  assign nb_waddr_w = done_r ? slane_r : rpj_w[5:3];\n",
     "  assign nb_waddr_w = done_r ? (slane_r & 3'd6) : rpj_w[5:3];\n",
     (r"N3 saved ordinal \d+",), True),
    # round 2: capacity boundary on the record walk (not the author's trigger edit):
    # the writer counts one name record fewer, so the table's last entry is
    # neither walked nor replayed; invisible at 128, fatal at the bound capacity
    ("R_name_walk_one_short", WRITER,
     "      default:    return 32'(N_NAME_P);\n",
     "      default:    return 32'(N_NAME_P - 1);\n",
     (r"N[35] \w+ ordinal 38(?!\d)", r"N[35] \w+ ordinal 106(?!\d)"), True),
    # round 2: the guard's debt never reaches the writer (top-level wiring)
    ("R_debt_unwired", TOP,
     "      .d3_desc_debt_i     (desc_mem_debt_w),\n",
     "      .d3_desc_debt_i     (1'b0),\n",
     (r"N9 debt names:",), True),
    # round 2: the guard forgives the debt at the burst's first beat, not its last
    ("R_guard_first_beat", GUARD,
     "                 && (m_rsp_last_i || m_rsp_err_i)) begin\n",
     "                 ) begin\n",
     (r"N9 debt names:",), False),
    # round 2: N9's premise is load-bearing: without the late burst there is no
    # debt and no cause-6 abort, and the premise check must fail
    ("R_n9_no_late_burst", BENCH,
     "    x.dram_late_cycles = 16000;\n",
     "    x.dram_late_cycles = 0;\n",
     (r"N9 debt: the late AUDIO_UNIT burst",), True),
)


def judge(control, root: Path, output: Path, verilator: str) -> dict:
    name, filename, old, new, required, graded = control
    work = output / name
    tree = work / "source"
    skip = shutil.ignore_patterns("obj*", "*.hex", "__pycache__")
    for directory in ("hdl", "tb/common", "tb/pp_top", "tb/name_state"):
        shutil.copytree(root / directory, tree / directory, ignore=skip)
    if old:
        path = tree / filename
        text = path.read_text()
        if text.count(old) != 1:
            return {"name": name, "verdict": "ANCHOR_MISSING"}
        path.write_text(text.replace(old, new))
    (work / "run").mkdir()
    result = subprocess.run(
        [sys.executable, "-B", str(tree / "tb/name_state/run.py"), "--root", str(tree),
         "--work", str(work / "run"), "--verilator", verilator],
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    (work / "run.log").write_text(result.stdout)
    fails = [l[6:] for l in result.stdout.splitlines() if l.startswith("FAIL: ")]
    tallies = re.findall(r"(\d+) checks: (\d+) PASS, (\d+) FAIL", result.stdout)
    completed = len(tallies) == 5  # 1x1@39, 8x8@107, 1x1@128, 8x8@128, combined
    hits = {p: [f for f in fails if re.match(p, f)][:4] for p in required}
    if not old:
        verdict = "PASS" if result.returncode == 0 and completed and not fails else "BROKEN"
    else:
        killed = result.returncode == 1 and completed and all(hits.values())
        verdict = ("KILLED" if killed else "SURVIVED") if graded else (
            "INFO_KILLED" if killed else "INFO_SURVIVED")
    record = {"name": name, "rc": result.returncode, "completed": completed,
              "tallies": tallies, "required": list(required), "matching": hits,
              "n_fail": len(fails), "first_fails": fails[:8], "verdict": verdict}
    print(f"{name}: {verdict} rc={result.returncode} fails={len(fails)}", flush=True)
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--verilator", required=True)
    parser.add_argument("--jobs", type=int, default=6)
    args = parser.parse_args()
    args.output.mkdir(parents=True)  # must be new
    root = args.root.resolve()
    out = args.output.resolve()
    golden = judge(("R_golden", None, "", "", (), True), root, out, args.verilator)
    records = [golden]
    if golden["verdict"] == "PASS":
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            records += list(pool.map(lambda c: judge(c, root, out, args.verilator), CONTROLS))
    (args.output / "results.json").write_text(json.dumps(records, indent=2) + "\n")
    ok = len(records) == len(CONTROLS) + 1 and all(
        r["verdict"] in ("PASS", "KILLED", "INFO_KILLED", "INFO_SURVIVED") for r in records)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
