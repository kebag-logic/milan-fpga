#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer-planted name controls for processor PR #172 (issue #170).

Each control is written by the reviewer from the RTL, independently of the
author's mutation tables. It copies the four source directories the name bench
builds from into an isolated tree, plants one exact edit, and runs the bench's
normal entry point (both synthetic populations, every check). A control is
KILLED only if the run completed (final tally printed), returned 1, and at
least one FAIL line starts with one of its expected name-value assertions.

usage: reviewer_controls.py --root CLONE --output NEWDIR --verilator PATH [--jobs N]
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

CONTROLS = (
    # name trigger kept only for even ordinals: half the names never persist
    ("R_trigger_odd_dropped", WRITER,
     "    if (nchg_i && (32'(nchg_ord_i) < N_NAME_P)) begin\n",
     "    if (nchg_i && (32'(nchg_ord_i) < N_NAME_P) && !nchg_ord_i[0]) begin\n",
     ("N3 saved ordinal 1", "N5 restored ordinal 1")),
    # record ID of a name written to the neighbouring ordinal's record
    ("R_record_id_neighbour", WRITER,
     "  assign hrid_w  = sel_base_f(hsel_w) + 8'(hidx_w);\n",
     "  assign hrid_w  = sel_base_f(hsel_w) + 8'((hsel_w == GRP_NAME_C) ? (hidx_w ^ 16'd1) : hidx_w);\n",
     ("N3 saved ordinal",)),
    # replay drops an all-zero lane: an empty saved name is treated as absent
    ("R_empty_replay_skipped", WRITER,
     "  assign sb_we_o    = !done_r && ((ws_r == W_APPLY) || (ws_r == W_NAPPLY));\n",
     "  assign sb_we_o    = !done_r && ((ws_r == W_APPLY)\n"
     "                                  || ((ws_r == W_NAPPLY) && (nb_rlane_w != 64'd0)));\n",
     ("N5 restored ordinal 2", "N5 restored ordinal 9", "N5 restored ordinal 16")),
    # a completed record also clears every higher-numbered pending record
    ("R_pending_clears_higher", WRITER,
     "    if (done_ok_w || giveup_w) clr_w[hand_r] = 1'b1;\n",
     "    if (done_ok_w || giveup_w)\n"
     "      for (int unsigned i = 0; i < N_REC_C; i++) if (i >= 32'(hand_r)) clr_w[i] = 1'b1;\n",
     ("N6 pending:",)),
    # replay proceeds without waiting for the store's LOCATE (image walk) answer
    ("R_replay_skips_locate_wait", WRITER,
     "        W_IMGLOC: begin\n          if (sb_rvalid_i) begin",
     "        W_IMGLOC: begin\n          if (1'b1) begin",
     ("D3N7:",)),
    # the service latch writes odd lanes over even lanes (lane aliasing)
    ("R_latch_lane_alias", WRITER,
     "  assign nb_waddr_w = done_r ? slane_r : rpj_w[5:3];\n",
     "  assign nb_waddr_w = done_r ? (slane_r & 3'd6) : rpj_w[5:3];\n",
     ("N3 saved ordinal",)),
)


def judge(control, root: Path, output: Path, verilator: str) -> dict:
    name, filename, old, new, expected = control
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
        [sys.executable, str(tree / "tb/name_state/run.py"), "--root", str(tree),
         "--work", str(work / "run"), "--verilator", verilator],
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    (work / "run.log").write_text(result.stdout)
    fails = [l[6:] for l in result.stdout.splitlines() if l.startswith("FAIL: ")]
    tallies = re.findall(r"(\d+) checks: (\d+) PASS, (\d+) FAIL", result.stdout)
    completed = len(tallies) == 3  # 1x1, 8x8 and the combined line
    hit = [f for f in fails if any(f == e or f.startswith(e + " ") or f.startswith(e)
                                   and not e[-1].isdigit() for e in expected)]
    if not old:
        verdict = "PASS" if result.returncode == 0 and completed and not fails else "BROKEN"
    else:
        verdict = "KILLED" if (result.returncode == 1 and completed and hit) else "SURVIVED"
    record = {"name": name, "rc": result.returncode, "completed": completed,
              "tallies": tallies, "expected": list(expected), "matching": hit[:8],
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
    golden = judge(("R_golden", None, "", "", ()), root, args.output.resolve(), args.verilator)
    records = [golden]
    if golden["verdict"] == "PASS":
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            records += list(pool.map(lambda c: judge(c, root, args.output.resolve(),
                                                     args.verilator), CONTROLS))
    (args.output / "results.json").write_text(json.dumps(records, indent=2) + "\n")
    ok = len(records) == len(CONTROLS) + 1 and all(
        r["verdict"] in ("PASS", "KILLED") for r in records)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
