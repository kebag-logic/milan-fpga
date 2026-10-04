#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Write the reviewer's planted controls: copies of the candidate KL_aecp_notify.sv,
each with exact edits (every old text must occur exactly once).

Usage: make_controls.py CANDIDATE.sv OUTDIR
"""
import sys
from pathlib import Path

MATCH = ("((ix_busy_w && (wr_ix_r == CIX_W_C'(i))) ? ix_own_w\n"
         "                                                                     : ix_hit_w[i]);")
WRITE = "        if (ix_busy_w && (wr_ix_r == CIX_W_C'(i)))\n"

CONTROLS = {
    # the rewrite comparator dropped: the index alone in both cycles
    "no_override": [(MATCH, "ix_hit_w[i];")],
    # the comparator only in the clear cycle (the set cycle reads the index)
    "override_clr_only": [(MATCH, MATCH.replace("(ix_busy_w &&", "(ix_clr_r &&"))],
    # the comparator only in the set cycle (the clear cycle reads the index)
    "override_set_only": [(MATCH, MATCH.replace("(ix_busy_w &&", "(ix_set_r &&"))],
    # the comparator against the row being written, not what rows_r holds
    "own_vs_new_row": [("  assign ix_own_w    = (ix_wr_row_w[127:16] == {rx_cmd_eid_i, rx_cmd_mac_i});",
                        "  assign ix_own_w    = (wr_row_r[127:16] == {rx_cmd_eid_i, rx_cmd_mac_i});")],
    # the old identity never cleared
    "no_clear": [(WRITE, WRITE.replace("ix_busy_w", "ix_set_r"))],
    # the new identity never set
    "no_set": [("      ix_set_r        <= ix_clr_r;\n", "      ix_set_r        <= 1'b0;\n")],
    # the last (4-bit) chunk ignored
    "last_chunk_ignored": [("    assign ix_hit_w[i] = &ch_w;\n",
                            "    assign ix_hit_w[i] = &ch_w[N_IXC_C-2:0];\n")],
    # the first chunk ignored
    "first_chunk_ignored": [("    assign ix_hit_w[i] = &ch_w;\n",
                             "    assign ix_hit_w[i] = &ch_w[N_IXC_C-1:1];\n")],
    # the key's eid and mac swapped against the row's
    "key_swapped": [("  assign ix_key_w    = (N_IXC_C*IXC_W_C)'({rx_cmd_eid_i, rx_cmd_mac_i});",
                     "  assign ix_key_w    = (N_IXC_C*IXC_W_C)'({rx_cmd_mac_i, rx_cmd_eid_i});")],
    # the write lands in the walk's row, not the written one
    "index_wrong_row": [(WRITE, WRITE.replace("(wr_ix_r == CIX_W_C'(i))", "(rd_ix_w == CIX_W_C'(i))"))],
    # the re-index starts a cycle late (clear in the set cycle, set after it)
    "reindex_late": [("      ix_set_r        <= ix_clr_r;\n",
                      "      ix_set_r        <= ix_late_r;\n      ix_late_r       <= ix_clr_r;\n"),
                     ("  logic                ix_clr_r, ix_set_r, ix_busy_w, ix_own_w;",
                      "  logic                ix_clr_r, ix_set_r, ix_busy_w, ix_own_w, ix_late_r;")],
    # a counter stamp read without its valid bit (the dropped reset then shows)
    "stamp_read_without_valid": [("            && (!ctr_sent_r[c]\n", "            && (1'b0\n")],
}


def main() -> int:
    src = Path(sys.argv[1]).read_text()
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    for name, edits in CONTROLS.items():
        text = src
        for old, new in edits:
            n = text.count(old)
            if n != 1:
                print(f"REFUSED {name}: old text occurs {n} times")
                return 1
            text = text.replace(old, new)
        (out / f"{name}.sv").write_text(text)
        print(f"planted {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
