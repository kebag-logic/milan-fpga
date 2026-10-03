#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer probes for the D3KR cut oracle (R444-1). Plants one defect in a
scratch copy of the processor tree. Every edit's old text must occur exactly
once. Usage: plant.py TREE NAME   (NAME in PLANTS)."""
import sys
from pathlib import Path

W = "hdl/aecp/KL_aecp_nvm_writer.sv"
DYN = "hdl/aecp/KL_aecp_dyn_state.sv"

PLANTS = {
    # T1, torn-write acceptance with the crc compare KEPT: the frame's crc16
    # covers the header and only the FIRST payload byte, on the writer's
    # commit side and on its restore side alike. Whole records still frame;
    # a record torn after its first payload byte frames too, and is applied.
    "T1_torn_crc_truncated": [
        (W, "  assign crc_last_w    = 7'd5 + hplen_w;           // header 0..5, payload\n",
            "  assign crc_last_w    = 7'd6;                     // PLANT: header + 1 payload byte\n"),
        (W, "            if ((rbcnt_r != 17'd6) && (rbcnt_r != 17'd7))\n",
            "            if ((rbcnt_r != 17'd6) && (rbcnt_r != 17'd7) && (rbcnt_r <= 17'd8))\n"),
    ],
    # T2, torn-write acceptance with the crc compare KEPT and computed: the
    # restore's frame verdict is bypassed in control flow, so a framed read
    # whose frame fails (a torn payload's crc) goes on to the SET program's
    # value rule instead of keeping its default.
    "T2_refused_frame_goes_to_rule": [
        (W, "              n_ref_r <= n_ref_r + 8'd1;      // the frame refuses it\n"
            "              ws_r    <= W_NEXT;\n",
            "              framed_any_r <= 1'b1;            // PLANT: the frame verdict bypassed\n"
            "              ws_r    <= W_RULE;\n"),
    ],
    # S1, stale-record acceptance: an erased/unframed (blank) name record in
    # pass 1 is taken to the name rule and written back from the name buffer,
    # a LUT RAM with no reset that still holds the name latched before the cut.
    "S1_blank_name_applies_stale_buffer": [
        (W, "              n_blank_r <= n_blank_r + 8'd1;  // erased or unframed: the default\n"
            "              ws_r      <= W_NEXT;\n",
            "              n_blank_r <= n_blank_r + 8'd1;  // PLANT: a blank name applies the buffer\n"
            "              ws_r      <= (rsel_w == GRP_NAME_C) ? W_RULE : W_NEXT;\n"),
    ],
    # S2, stale-row acceptance: the presentation-offset rows' valid flags
    # survive rst_n, so the value set before the cut outlives an erased or
    # torn record.
    "S2_ptof_valid_survives_reset": [
        (DYN, "      ptoff_v_r  <= '0;\n", "      // PLANT: ptoff_v_r keeps its value across rst_n\n"),
    ],
}


def main() -> int:
    tree, name = Path(sys.argv[1]), sys.argv[2]
    for path, old, new in PLANTS[name]:
        p = tree / path
        text = p.read_text()
        n = text.count(old)
        if n != 1:
            print(f"REFUSED {name}: {path} old text occurs {n} times")
            return 2
        p.write_text(text.replace(old, new))
        print(f"planted {name}: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
