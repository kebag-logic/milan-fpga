#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer-owned planted controls for processor PR #172 (tb/name_state).

Each control is an exact edit, written by the reviewer and distinct from the
author's campaign, applied to an isolated copy of a processor export. The copy
is built with the suite's own harness and run on the synthetic population for
the requested shape. A control counts as KILLED only when the run completes
(tally line present), exits 1, and a FAIL line starts with the expected named
assertion. Build failure, crash or a missing tally is never a kill.

Usage: reviewer_controls.py --root <processor export> --output <new dir>
       [--verilator V] [--jobs N] [--only NAME ...]
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

W = "hdl/aecp/KL_aecp_nvm_writer.sv"

# name, shape (aaf), sim case, expected assertion prefix, edits
CONTROLS = [
    # every ordinal: names at and above the product default capacity (32)
    # lose their trigger; the old five-name proof never reached them
    ("R1_trigger_lost_above_31", 1, "inventory", "N3 saved ordinal 32", [(W,
        "    if (nchg_i && (32'(nchg_ord_i) < N_NAME_P)) begin\n",
        "    if (nchg_i && (32'(nchg_ord_i) < N_NAME_P) && (nchg_ord_i < 10'd32)) begin\n")]),
    # the 8x8 population really reaches its last ordinals (100..106)
    ("R1b_trigger_lost_above_99_8x8", 8, "inventory", "N3 saved ordinal 100", [(W,
        "    if (nchg_i && (32'(nchg_ord_i) < N_NAME_P)) begin\n",
        "    if (nchg_i && (32'(nchg_ord_i) < N_NAME_P) && (nchg_ord_i < 10'd100)) begin\n")]),
    # swap ordinal and record id for one adjacent pair (36 <-> 37) only
    ("R2_record_id_pair_swapped", 1, "inventory", "N3 saved ordinal 36", [(W,
        "  assign hrid_w  = sel_base_f(hsel_w) + 8'(hidx_w);\n",
        "  assign hrid_w  = sel_base_f(hsel_w) + 8'(((hsel_w == GRP_NAME_C) && (hidx_w[15:1] == 15'd18))\n"
        "                                            ? (hidx_w ^ 16'd1) : hidx_w);\n")]),
    # empty lanes treated as absent on replay: a zero lane is not written back
    ("R3_zero_lane_not_replayed", 1, "inventory", "N5 restored ordinal 2", [(W,
        "        rs_sb_req_w   = 1'b1;\n        rs_sb_name_w  = 1'b1;\n",
        "        rs_sb_req_w   = (nb_rlane_w != 64'd0);\n        rs_sb_name_w  = 1'b1;\n")]),
    # completing a name record also clears the next record's pending
    ("R4_done_clears_next_record", 1, "inventory", "N3 saved ordinal", [(W,
        "    if (done_ok_w || giveup_w) clr_w[hand_r] = 1'b1;\n",
        "    if (done_ok_w || giveup_w) clr_w[hand_r] = 1'b1;\n"
        "    if ((done_ok_w || giveup_w) && (hsel_w == GRP_NAME_C)\n"
        "        && (32'(hand_r) + 1 < N_REC_C)) clr_w[hand_r + RW_C'(1)] = 1'b1;\n")]),
    # a name's eight-lane latch no longer waits for the program to finish
    ("R5_name_latch_ignores_program", 1, "capture", "N7 capture:", [(W,
        "          if (!prog_busy_i) begin\n            ss_r    <= (hsel_w == GRP_NAME_C) ? S_NLATCH : S_LATCH;\n",
        "          if (!prog_busy_i || (hsel_w == GRP_NAME_C)) begin\n            ss_r    <= (hsel_w == GRP_NAME_C) ? S_NLATCH : S_LATCH;\n")]),
    # the late-image LOCATE is not awaited: replay starts before the walk ends
    # graded first on D3N7 (healing case): SURVIVED there (one seeded name);
    # the full-population inventory case is where its effect is visible
    ("R6_replay_before_locate_answer", 1, "inventory", "N4 every name reset", [(W,
        "        W_IMGLOC: begin\n          if (sb_rvalid_i) begin",
        "        W_IMGLOC: begin\n          if (1'b1) begin")]),
    # the roll-back strobe never reaches the stores
    ("R7_rollback_strobe_dropped", 1, "rollback", "D3N5: the roll-back left", [(W,
        "  assign rb_rst_o    = (ws_r == W_RB);\n",
        "  assign rb_rst_o    = 1'b0;\n")]),
    # README check: does the image-proof bypass also fail N4 in the inventory
    # case (the README lists it under N4; the campaign grades it on D3N7 only)
    ("R8_image_proof_bypassed_inventory", 1, "inventory", "N4 every name reset", [(W,
        "        W_IMG: begin\n          if (img_valid_i) begin\n            proven_r <= 1'b1;\n"
        "            ws_r     <= W_RQ;\n          end else begin\n            ws_r <= W_IMGLOC;\n"
        "          end\n        end\n",
        "        W_IMG: begin\n          proven_r <= 1'b1;\n          ws_r     <= W_RQ;\n        end\n")]),
    # N4 alone: the boot walk no longer reloads names at or above ordinal 8,
    # so the SET values survive the reset into the replay
    ("R9_reset_walk_keeps_names", 1, "inventory", "N4 every name reset", [(
        "hdl/aecp/KL_aecp_desc_store.sv",
        "      name_we_w    = 1'b1;\n      name_waddr_w = NAME_AW_C'(name_load_lane_r + {11'd0, beat_ix_r});\n",
        "      name_we_w    = (name_load_lane_r + {11'd0, beat_ix_r}) < 64 || name_r[NAME_AW_C'(name_load_lane_r + {11'd0, beat_ix_r})] == 64'd0;\n"
        "      name_waddr_w = NAME_AW_C'(name_load_lane_r + {11'd0, beat_ix_r});\n")]),
    # pending: names never raise the D3 writer's pending export (values are
    # still saved); probes whether any name check reads d3_unflushed_o high
    ("R10_names_not_pending", 1, "all", "N", [(W,
        "  assign unflushed_o = |dirty_r;\n",
        "  assign unflushed_o = |dirty_r[OFF_NAME_C-1:0];\n")]),
]


def replace_once(text, old, new):
    if text.count(old) != 1:
        raise RuntimeError(f"anchor count {text.count(old)}: {old!r}")
    return text.replace(old, new)


def judge(control, root, output, verilator):
    name, aaf, case, expect, edits = control
    work = output / name
    work.mkdir()
    tree = work / "source"
    skip = shutil.ignore_patterns("obj*", "*.hex", "__pycache__")
    for d in ("hdl", "tb/common", "tb/pp_top", "tb/name_state"):
        shutil.copytree(root / d, tree / d, ignore=skip)
    for filename, old, new in edits:
        path = tree / filename
        path.write_text(replace_once(path.read_text(), old, new))
    sys.path.insert(0, str(tree / "tb/name_state"))
    import run as harness  # the suite's own build (wrapper widening + gsi-build)
    import fixture as fx
    try:
        binary = harness.build(tree, work, verilator)
    except RuntimeError as error:
        rec = {"name": name, "verdict": "BUILD_FAILED", "reason": str(error)}
        print(f"{name}: BUILD_FAILED", flush=True)
        return rec
    image = work / f"names-{aaf}.bin"
    image.write_bytes(fx.packer(tree).build(fx.fixture(aaf), lint=False)[0])
    res = subprocess.run([str(binary), str(image), str(aaf), case], cwd=work,
                         text=True, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, check=False, timeout=3600)
    (work / "run.log").write_text(res.stdout)
    fails = [l[len("FAIL: "):] for l in res.stdout.splitlines() if l.startswith("FAIL: ")]
    tally = re.search(r"(\d+) checks: (\d+) PASS, (\d+) FAIL", res.stdout)
    golden = not edits
    if golden:
        verdict = "PASS" if res.returncode == 0 and tally and tally[3] == "0" else "BROKEN"
    else:
        verdict = "KILLED" if (res.returncode == 1 and tally and
                               any(f.startswith(expect) for f in fails)) else "SURVIVED"
    rec = {"name": name, "aaf": aaf, "case": case, "expect": expect,
           "run_rc": res.returncode, "tally": tally[0] if tally else None,
           "verdict": verdict, "failures": fails[:40], "n_failures": len(fails)}
    print(f"{name}: {verdict} ({rec['tally']})", flush=True)
    return rec


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--verilator", default="verilator")
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    root = a.root.resolve()
    out = a.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    sel = [c for c in CONTROLS if not a.only or c[0] in a.only]
    goldens = [("golden_1x1", 1, "all", "", []), ("golden_8x8", 8, "inventory", "", [])]
    with ThreadPoolExecutor(max_workers=a.jobs) as pool:
        recs = list(pool.map(lambda c: judge(c, root, out, a.verilator), goldens + sel))
    (out / "results.json").write_text(json.dumps(recs, indent=2) + "\n")
    ok = all(r["verdict"] in ("PASS", "KILLED") for r in recs)
    print(f"reviewer controls: {sum(r['verdict']=='KILLED' for r in recs)}/{len(sel)} KILLED; "
          f"goldens {[r['verdict'] for r in recs[:2]]}; rc {0 if ok else 1}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
