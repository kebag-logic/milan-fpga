#!/usr/bin/env python3
"""Write the reviewer's planted control copies of the candidate KL_aecp_notify.sv.

Usage: plant.py CANDIDATE_SV OUTDIR
Each control replaces exactly one snippet (asserted) and is written to
OUTDIR/<name>.sv. A control the lockstep bench does not catch is a hole in it.
"""
import sys
from pathlib import Path

HIT_MUX = ("                        && ((ix_busy_w && (wr_ix_r == CIX_W_C'(i))) ? ix_own_w\n"
           "                                                                     : ix_hit_w[i]);\n")
IX_WRITE = "        if (ix_busy_w && (wr_ix_r == CIX_W_C'(i)))\n"

CONTROLS = {
    # the two rewrite cycles read the index instead of the comparator
    "no_override": (HIT_MUX, "                        && ix_hit_w[i];\n"),
    # the comparator covers only the set cycle (the clear cycle reads the index)
    "override_set_only": (HIT_MUX, HIT_MUX.replace("(ix_busy_w &&", "(ix_set_r &&")),
    # the comparator covers only the clear cycle
    "override_clr_only": (HIT_MUX, HIT_MUX.replace("(ix_busy_w &&", "(ix_clr_r &&")),
    # the old identity's bits are never cleared
    "no_clear": (IX_WRITE, IX_WRITE.replace("ix_busy_w", "ix_set_r")),
    # the new identity's bits are never set
    "no_set": ("      ix_set_r        <= ix_clr_r;\n", "      ix_set_r        <= 1'b0;\n"),
    # the match ignores the last (4-bit) chunk
    "last_chunk_ignored": ("    assign ix_hit_w[i] = &ch_w;\n",
                           "    assign ix_hit_w[i] = &ch_w[N_IXC_C-2:0];\n"),
    # the clear addresses the NEW identity (wr_row_r), so the old one stays
    "clear_new_identity": ("  assign ix_row_w    = (N_IXC_C*IXC_W_C)'(ix_wr_row_w[127:16]);\n",
                           "  assign ix_row_w    = (N_IXC_C*IXC_W_C)'(wr_row_r[127:16]);\n"),
    # the window comparator reads the incoming row, not what rows_r holds
    "own_compare_new_row": ("  assign ix_own_w    = (ix_wr_row_w[127:16] == {rx_cmd_eid_i, rx_cmd_mac_i});\n",
                            "  assign ix_own_w    = (wr_row_r[127:16] == {rx_cmd_eid_i, rx_cmd_mac_i});\n"),
    # REGISTER does not start the re-index
    "register_not_reindexed": ("            ix_clr_r <= 1'b1;             // re-index the row (above)\n", ""),
    # a stamp is read without its valid bit (the dropped reset then shows)
    "stamp_without_valid": ("            && (!ctr_sent_r[c]\n                || ((now_ms_i - ctr_last_r[c]) >= 32'd1000))) begin\n",
                            "            && (((now_ms_i - ctr_last_r[c]) >= 32'd1000))) begin\n"),
}


def main() -> int:
    src = Path(sys.argv[1]).read_text()
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    for name, (old, new) in CONTROLS.items():
        n = src.count(old)
        if n != 1:
            print(f"control {name}: snippet found {n} times, expected 1", file=sys.stderr)
            return 1
        (out / f"{name}.sv").write_text(src.replace(old, new))
        print(f"planted {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
