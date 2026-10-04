#!/usr/bin/env python3
"""R462-2's own arm-queue controls, in the MUTANTS format of R462-1's lockstep_armq/gen.py
(name -> (old, new), each old text occurring exactly once in protocol_processor_top.sv).
Pass this file as GEN_PY to aq_gen_mutant.sh. None of them is in acmp_mutants.py; they test
how far AQ3 reaches past the required list (resets with arms queued, the saturation edge,
the full-queue write index, the drop rule on a full face that pops)."""

MUTANTS = {
    # a reset leaves each face's count as it was (arms queued survive a reset)
    "cnt_not_reset": ("      armq_cnt_r <= '0;\n", ""),
    # a reset leaves the drop counter as it was
    "drop_not_reset": ("      arm_drop_r <= 16'd0;\n", ""),
    # the counter stops one short of 0xFFFF
    "sat_at_fffe": ("if (arm_drop_r != 16'hFFFF) arm_drop_r <= arm_drop_r + 16'd1;",
                    "if (arm_drop_r != 16'hFFFE) arm_drop_r <= arm_drop_r + 16'd1;"),
    # a full face that pops writes one past its leaving head (onto the oldest survivor)
    "full_pop_writes_next": ("assign wr_ix_w = armq_hd_r[g] + armq_cnt_r[g][1:0];",
                             "assign wr_ix_w = armq_hd_r[g] + armq_cnt_r[g][1:0]"
                             " + {1'b0, armq_cnt_r[g][2]};"),
    # write-first read: a full face that pops and pushes issues the arriving arm, not its head
    # (the second of R463-1 S1's three ring defects)
    "write_first_read": ("assign armq_hd_w[g] = mem_r[armq_hd_r[g]];",
                         "assign armq_hd_w[g] = (armq_push_ok_w[g] && (wr_ix_w == armq_hd_r[g]))"
                         " ? armq_in_w[g] : mem_r[armq_hd_r[g]];"),
    # an offer to a face full before the clock counts a drop even when its pop admits it
    "drop_on_full_popped": ("if (armq_in_vld_w[i] && !armq_push_ok_w[i]) begin",
                            "if (armq_in_vld_w[i] && (armq_cnt_r[i] == 3'd4)) begin"),
}
