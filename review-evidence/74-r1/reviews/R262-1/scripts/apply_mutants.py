#!/usr/bin/env python3
"""Reviewer mutation recipe (R262-1, issue #74 item 2).

Applies one exact-string substitution per mutant to a disposable copy of the
head tree at <scratch>/mut/<name>/ and refuses unless the pattern matches
exactly once. usage: apply_mutants.py <scratch_dir>
"""
import pathlib
import sys

ALIGN = "hdl/ieee1722/crf/KL_media_grid_align.sv"
CAPT = "hdl/ieee1722/aaf/KL_chan_map_capture.sv"

MUTANTS = {
    # the keep-off clamps only the low side (captures just after the tick)
    "MA1_no_hi_clamp": (ALIGN,
        ": (tst_next_w > KEEP_HI_C) ? KEEP_HI_C",
        ": (1'b0) ? KEEP_HI_C"),
    # the keep-off clamps only the high side (captures just before the tick)
    "MA2_no_lo_clamp": (ALIGN,
        "(tst_next_w < KEEP_LO_C) ? KEEP_LO_C",
        "(1'b0) ? KEEP_LO_C"),
    # a keep-off of 1/512 sample (4 cycles) instead of 1/128 (16 cycles)
    "MA3_keepoff4": (ALIGN,
        "= (CLK_FREQ_HZ_P / FS_HZ_P) / 128",
        "= (CLK_FREQ_HZ_P / FS_HZ_P) / 512"),
    # coincidence always leaves the coincident marker pending, uncounted
    "MC1_coin_pend1": (CAPT,
        "tdm_frame_pend_r <= tdm_frame_pend_r;",
        "tdm_frame_pend_r <= 1'b1;"),
    # coincidence as a consistent tick-then-marker order (dup when nothing
    # was pending, the coincident marker pends) - a net-exact alternative
    "MC2_coin_tickfirst": (CAPT,
        "tdm_frame_pend_r <= tdm_frame_pend_r;",
        "tdm_frame_pend_r <= 1'b1;\n"
        "          if (tdm_fed_r && !tdm_frame_pend_r && tdm_dup_cnt_o != 16'hFFFF)\n"
        "            tdm_dup_cnt_o <= tdm_dup_cnt_o + 16'd1;"),
    # coincidence as a consistent marker-then-tick order (skip when one was
    # pending, the tick consumes the coincident marker) - net-exact too
    "MC3_coin_markfirst": (CAPT,
        "tdm_frame_pend_r <= tdm_frame_pend_r;",
        "tdm_frame_pend_r <= 1'b0;\n"
        "          if (tdm_frame_pend_r && tdm_skip_cnt_o != 16'hFFFF)\n"
        "            tdm_skip_cnt_o <= tdm_skip_cnt_o + 16'd1;"),
}


def main() -> int:
    scratch = pathlib.Path(sys.argv[1])
    for name, (rel, old, new) in MUTANTS.items():
        path = scratch / "mut" / name / rel
        text = path.read_text()
        count = text.count(old)
        if count != 1:
            print(f"REFUSED {name}: pattern matched {count} times in {rel}")
            return 1
        path.write_text(text.replace(old, new))
        print(f"applied {name}: {rel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
