#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R276-5 reviewer probe: write the head engine and planted engines.

Each planted engine replaces exactly one anchor of the head
KL_media_clock_restart.sv; an anchor that is not found exactly once is a
hard error, so a moved line cannot turn a planted engine into a copy of the
head. Usage: plant.py <head KL_media_clock_restart.sv> <outdir>
"""
import sys
from pathlib import Path

MERGE = "      if (restart_p_i | src_change_w) tgt_r <= ~mr_o;"
WIRE = ("        if ((restart_p_i | src_change_w) && streaming_i[t]"
        " && (hold_r[t] == '0))")
ADOPT = ("        else if ((mr_o[t] != tgt_r[t]) && (hold_r[t] == "
         "HOLDW_C'(HOLD_PDU_P))) begin : g_adopt")
HOLDQ = "      if (frame_p_i && idx_ok_w && (frame_mr_i == mr_o[fidx_w])"

PLANTS = {
    # the pre-#387 rule: every request flips the target (cancels a pending one)
    "m1_flip_per_request": (MERGE, "      if (restart_p_i | src_change_w) tgt_r <= ~tgt_r;"),
    # the a9636e0f rule: the window ends at the adoption, not at the wire
    "m2_window_ends_at_adoption": (WIRE, "        if (1'b0)"),
    # the window stays open for the whole hold
    "m3_window_whole_hold": (WIRE,
        "        if ((restart_p_i | src_change_w) && streaming_i[t] && (mr_o[t] == tgt_r[t])\n"
        "            && (hold_r[t] != HOLDW_C'(HOLD_PDU_P)))"),
    # the window ends one PDU late (at the second PDU at the adopted level)
    "m4_window_one_pdu_late": (WIRE,
        "        if ((restart_p_i | src_change_w) && streaming_i[t] && (hold_r[t] < 2))"),
    # adoption one PDU early: a 7-PDU hold
    "m5_hold_seven": (ADOPT,
        "        else if ((mr_o[t] != tgt_r[t]) && (hold_r[t] >= "
        "HOLDW_C'(HOLD_PDU_P - 1))) begin : g_adopt"),
    # the hold counts every PDU, not only those at the current level
    "m6_hold_counts_any_level": (HOLDQ, "      if (frame_p_i && idx_ok_w"),
}


def main() -> int:
    src = Path(sys.argv[1]).read_text()
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    (out / "head.sv").write_text(src)
    for name, (anchor, repl) in PLANTS.items():
        n = src.count(anchor)
        if n != 1:
            print(f"anchor for {name} found {n} times, expected 1", file=sys.stderr)
            return 2
        (out / f"{name}.sv").write_text(src.replace(anchor, repl))
    return 0


if __name__ == "__main__":
    sys.exit(main())
