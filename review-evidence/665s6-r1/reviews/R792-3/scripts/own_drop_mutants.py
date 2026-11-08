#!/usr/bin/env python3
"""Plant one disposable defect into a COPY of the tree's split datapath drop-count binding
(hdl/milan/milan_datapath.sv, the CTRL_SPLIT_P = 1 KL_ctrl_split instance), so the split leg
can be rebuilt on that copy and must fail. Usage: own_drop_mutants.py <copy-root> <halved|stuck1>
Never run it on a checkout you want to keep: it rewrites the file in place."""
import pathlib
import sys

OLD = ("      .rx_drops_o       (pp_rx_drops_w),\n      .tx_frames_o      (pp_tx_frames_w)\n"
       "    );\n")
INST = "    KL_ctrl_split #(.TDATA_WIDTH_P(TDATA_WIDTH)) ctrl_split ("
EXPR = {"halved": "{1'b0, own_drops_w[7:1]}", "stuck1": "own_drops_w | 8'h01"}


def main() -> int:
    root, kind = pathlib.Path(sys.argv[1]), sys.argv[2]
    p = root / "hdl/milan/milan_datapath.sv"
    t = p.read_text()
    if t.count(OLD) != 1 or t.count(INST) != 1:
        print("anchor not unique; refusing")
        return 2
    t = t.replace(OLD, OLD.replace("(pp_rx_drops_w)", "(own_drops_w)")
                  + f"    assign pp_rx_drops_w = {EXPR[kind]};\n")
    t = t.replace(INST, "    logic [7:0] own_drops_w;\n" + INST)
    p.write_text(t)
    print(f"planted {kind}: pp_rx_drops_w = {EXPR[kind]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
