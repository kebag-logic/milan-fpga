#!/usr/bin/env python3
"""Write planted mutants of the two changed RTL files.

usage: make_mutants.py <head-tree> <outdir>
Each mutant is a whole-file copy with exactly one textual edit; the edit's
'old' text must occur exactly once in the head file, so a mutant can never be
a silent no-op. Writes <outdir>/<ID>/<relpath> and <outdir>/index.tsv.
"""
import pathlib
import sys

EVR = "hdl/packet_engine/KL_pp_event_router.sv"
NTF = "hdl/aecp/KL_aecp_notify.sv"

MUTANTS = [
    # router: each changes a port-visible behaviour unless marked EQUIV
    ("R1", EVR, "base always ptr_r",
     "assign base_w = valid_r ? rr_next(sel_r) : ptr_r;",
     "assign base_w = ptr_r;"),
    ("R2", EVR, "presented event not removed from the scan",
     "if (valid_r) pend_after_w[sel_r] = 1'b0;",
     "if (1'b0) pend_after_w[sel_r] = 1'b0;"),
    ("R3", EVR, "load ignores the acknowledge",
     "if (deliver_w || !valid_r) begin",
     "if (1'b1) begin"),
    ("R4", EVR, "select reloads every cycle, outside the load enable",
     "        valid_r <= gnt_found_w;\n        sel_r   <= sel_next_w;\n      end",
     "        valid_r <= gnt_found_w;\n      end\n      sel_r <= sel_next_w;"),
    ("R5", EVR, "no grant clears the select instead of keeping it",
     "assign sel_next_w = gnt_found_w ? gnt_src_w : sel_r;",
     "assign sel_next_w = gnt_src_w;"),
    ("R6", EVR, "base keyed on valid_r, removal still keyed on deliver_w (EQUIV)",
     "if (valid_r) pend_after_w[sel_r] = 1'b0;",
     "if (deliver_w) pend_after_w[sel_r] = 1'b0;"),
    # notify: occupancy flop and its readers
    ("N1", NTF, "pop keeps the queue occupied",
     "cmdq_nempty_r <= (cmdq_count_r != 5'd1);",
     "cmdq_nempty_r <= 1'b1;"),
    ("N2", NTF, "push does not set the occupancy",
     "          cmdq_count_r <= cmdq_count_r + 5'd1;\n          cmdq_nempty_r <= 1'b1;\n",
     "          cmdq_count_r <= cmdq_count_r + 5'd1;\n"),
    ("N3", NTF, "pop off by one (empties one entry late)",
     "cmdq_nempty_r <= (cmdq_count_r != 5'd1);",
     "cmdq_nempty_r <= (cmdq_count_r != 5'd0);"),
    ("N4", NTF, "pop beside a push clears the occupancy",
     "                  if (cmd_push_w)\n                    cmdq_count_r <= cmdq_count_r;\n",
     "                  if (cmd_push_w) begin\n                    cmdq_count_r <= cmdq_count_r;\n"
     "                    cmdq_nempty_r <= 1'b0;\n                  end\n"),
    ("N5", NTF, "amap_busy_o drops the queue occupancy",
     "|| cmdq_nempty_r || (|ctr_pend_r) || id_own_w;",
     "|| (|ctr_pend_r) || id_own_w;"),
    ("N6", NTF, "reset sets the occupancy",
     "      cmdq_nempty_r <= 1'b0;",
     "      cmdq_nempty_r <= 1'b1;"),
    ("N7", NTF, "pop clears the occupancy at once (empties early)",
     "cmdq_nempty_r <= (cmdq_count_r != 5'd1);",
     "cmdq_nempty_r <= 1'b0;"),
]


def main() -> int:
    head = pathlib.Path(sys.argv[1])
    out = pathlib.Path(sys.argv[2])
    rows = []
    for mid, rel, what, old, new in MUTANTS:
        text = (head / rel).read_text()
        n = text.count(old)
        if n != 1:
            print(f"{mid}: anchor occurs {n} times in {rel}", file=sys.stderr)
            return 2
        dst = out / mid / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(text.replace(old, new))
        rows.append(f"{mid}\t{rel}\t{what}")
    (out / "index.tsv").write_text("\n".join(rows) + "\n")
    print("\n".join(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
