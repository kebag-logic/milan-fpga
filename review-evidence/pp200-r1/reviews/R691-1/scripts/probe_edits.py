#!/usr/bin/env python3
"""Plant one of the reviewer's two disposable probe edits in a COPY of the
processor tree at 33d3010c (never in the reviewed clone).

usage: python3 -I probe_edits.py {order|noecho} TREE

order  : GET_AVB_INFO's A_PLD-exit arm judges the type before the length
         (expected: tb/aecp_cmds decode record diverges and tb/pp_top V4 fails)
noecho : the wrong-type NSUPPE arm without its explicit `echo_r <= 1'b1`
         (expected: behaviour unchanged; only the engine digest moves)

Then run, in TREE:
  make -C tb/aecp_cmds run VERILATOR=<pinned 5.050>
  make -C tb/pp_top aecp-dispatch VERILATOR=<pinned 5.050>
"""
import pathlib
import sys

ARM = """              if (cmd_r.cdl < 11'd16)                 upc_r <= UPC_BADARG_C;
              else if (cfg_ix_r != DT_AVB_INTERFACE_C) begin
                upc_r  <= UPC_NSUPPE_C;
                echo_r <= 1'b1;
              end else begin
                upc_r  <= UPC_GAVB_C;"""

EDITS = {
    "order": """              if (cfg_ix_r != DT_AVB_INTERFACE_C) begin
                upc_r  <= UPC_NSUPPE_C;
                echo_r <= 1'b1;
              end else if (cmd_r.cdl < 11'd16)        upc_r <= UPC_BADARG_C;
              else begin
                upc_r  <= UPC_GAVB_C;""",
    "noecho": """              if (cmd_r.cdl < 11'd16)                 upc_r <= UPC_BADARG_C;
              else if (cfg_ix_r != DT_AVB_INTERFACE_C) begin
                upc_r  <= UPC_NSUPPE_C;
              end else begin
                upc_r  <= UPC_GAVB_C;""",
}


def main() -> int:
    kind, tree = sys.argv[1], pathlib.Path(sys.argv[2])
    eng = tree / "hdl/aecp/KL_aecp_engine.sv"
    src = eng.read_text()
    if src.count(ARM) != 1:
        print("the GET_AVB_INFO arm is not the 33d3010c text", file=sys.stderr)
        return 2
    eng.write_text(src.replace(ARM, EDITS[kind]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
