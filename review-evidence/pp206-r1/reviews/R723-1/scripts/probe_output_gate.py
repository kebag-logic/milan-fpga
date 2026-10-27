#!/usr/bin/env python3
"""Reviewer probe: apply issue #206's settled gate to STREAM_OUTPUT words too.

Plants, in a disposable copy of hdl/top/protocol_processor_top.sv, a gate on
kind-0 STREAM_OUTPUT selectors 0, 2 and 4 keyed on the same gsi_settled_w.
The suite must fail (STREAM_OUTPUT answers are required to be unchanged).
Usage: probe_output_gate.py <path to protocol_processor_top.sv>
"""
import sys

ANCHOR = "  always_comb begin : gsi_answer\n    aecp_gsi_data_w = gsi_data_i;\n"
PLANT = (
    "    if (!gsi_input_w && (gsi_kind_o == 2'd0)\n"
    "        && (gsi_desc_type_o == 16'h0006) && !gsi_settled_w) begin\n"
    "      case (gsi_sel_o)\n"
    "        4'd0: aecp_gsi_data_w = gsi_data_i & ~64'h0000_0000_5200_0000;\n"
    "        4'd2: aecp_gsi_data_w = 64'd0;\n"
    "        4'd4: aecp_gsi_data_w[63:16] = 48'd0;\n"
    "        default: begin end\n"
    "      endcase\n"
    "    end\n"
)


def main() -> int:
    path = sys.argv[1]
    text = open(path, encoding="utf-8").read()
    if text.count(ANCHOR) != 1:
        print("anchor not found exactly once", file=sys.stderr)
        return 2
    open(path, "w", encoding="utf-8").write(text.replace(ANCHOR, ANCHOR + PLANT))
    print("planted output gate in", path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
