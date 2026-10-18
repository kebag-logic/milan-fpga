#!/usr/bin/env python3
"""Round-2 planted mutants for the out-of-tree proofs (issue #181 evidence).

Each is one exact edit (the old text must occur exactly once) in a copy of the
head module (src/head_*.sv, from c5afc0a4). R1-R5 must fail the router
equivalence; N1-N4, N6, N7 must fail the occupancy induction; N5 (amap_busy_o
drops the occupancy term) only reads the flop, so the invariant still holds and
the in-tree checks CQ1b and CQ2b fail it instead. usage: make_mutants.py <dir>
"""
import sys
from pathlib import Path

ROUTER = {
    "R1-base-always-ptr": ("  assign base_w = valid_r ? rr_next(sel_r) : ptr_r;\n",
                           "  assign base_w = ptr_r;\n"),
    "R2-presented-not-removed": ("    if (valid_r) pend_after_w[sel_r] = 1'b0;\n",
                                 "    if (1'b0) pend_after_w[sel_r] = 1'b0;\n"),
    "R3-load-ignores-ack": ("      if (deliver_w || !valid_r) begin\n",
                            "      if (1'b1) begin\n"),
    "R4-select-reloads-always": ("        valid_r <= gnt_found_w;\n        sel_r   <= sel_next_w;\n      end\n",
                                 "        valid_r <= gnt_found_w;\n      end\n      sel_r <= sel_next_w;\n"),
    "R5-no-grant-clears": ("  assign sel_next_w = gnt_found_w ? gnt_src_w : sel_r;\n",
                           "  assign sel_next_w = gnt_src_w;\n"),
}
POP = "                    cmdq_nempty_r <= (cmdq_count_r != 5'd1);\n"
NOTIFY = {
    "N1-pop-keeps-set": (POP, POP.replace("(cmdq_count_r != 5'd1)", "1'b1")),
    "N2-push-unseen": ("          cmdq_nempty_r <= 1'b1;\n", ""),
    "N3-pop-one-late": (POP, POP.replace("5'd1", "5'd0")),
    "N4-cleared-beside-push": ("                  if (cmd_push_w)\n                    cmdq_count_r <= cmdq_count_r;\n",
                               "                  if (cmd_push_w) begin\n                    cmdq_count_r <= cmdq_count_r;\n"
                               "                    cmdq_nempty_r <= 1'b0;\n                  end\n"),
    "N5-not-busy": ("                       || cmdq_nempty_r || (|ctr_pend_r) || id_own_w;\n",
                    "                       || (|ctr_pend_r) || id_own_w;\n"),
    "N6-reset-set": ("      cmdq_nempty_r <= 1'b0;\n", "      cmdq_nempty_r <= 1'b1;\n"),
    "N7-pop-clears": (POP, POP.replace("(cmdq_count_r != 5'd1)", "1'b0")),
}


def main() -> int:
    here = Path(sys.argv[1])
    ok = True
    for src, muts in (("head_KL_pp_event_router.sv", ROUTER), ("head_KL_aecp_notify.sv", NOTIFY)):
        text = (here / "src" / src).read_text()
        for name, (old, new) in muts.items():
            if text.count(old) != 1:
                print(f"{name}: REFUSED, the edit text occurs {text.count(old)} times")
                ok = False
                continue
            (here / "mutants" / f"{name}.sv").write_text(text.replace(old, new, 1))
            print(f"{name}: planted")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
