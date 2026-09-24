#!/usr/bin/env python3
"""R269-3: generate disposable RTL / harness mutants for the criterion-3 probes.

usage: gen_mutants.py <exact-head tree> <out dir>

Every edit is an exact textual replacement that must apply exactly once, so a
mutant cannot silently degrade into the unmutated head. Writes
<out>/<name>/milan_datapath.sv (RTL) or <out>/<name>/sim_nxn.cpp (harness) and
<out>/MUTANTS.tsv (name, kind, legs, expectation, description).
"""
import pathlib
import sys

A_SIN_DIRTY = "    assign pp_ctr_sin_dirty_w = {crf_dirty_p_w, avtprx_dirty_p_w};\n"
A_SIN_NEXT = "    pp_ctr_sin_pend_n  = pp_ctr_sin_pend_r  | pp_ctr_sin_dirty_w;\n"
A_SOUT_NEXT = "    pp_ctr_sout_pend_n = pp_ctr_sout_pend_r | tkd_dirty_p_w;\n"
A_AVB_NEXT = "    pp_ctr_avb_pend_n  = pp_ctr_avb_pend_r  | ctr_avb_dirty_w;\n"
A_CKD_NEXT = "    pp_ctr_ckd_pend_n  = pp_ctr_ckd_pend_r  | ctr_ckd_dirty_w;\n"
A_SIN_IDX = "          pp_ctr_evt_index_w = 16'(pick);\n"
A_AVB_TYPE = "          pp_ctr_evt_type_w  = DESC_AVB_INTERFACE_C;\n"
A_ARB_ANCHOR = "  always_comb begin : pp_ctr_event_next\n"
CRF_ROW = "(pick == N_STREAMS && PP_CTR_SIN_N_C > N_STREAMS)"

# name -> (legs, expectation, description, [(anchor, replacement), ...])
RTL = {
    "X01_also_sin0": ("nxn nxn8", "RED: STREAM_INPUT N only",
        "CRF pulse also raises AAF STREAM_INPUT 0",
        [(A_SIN_NEXT, "    pp_ctr_sin_pend_n  = pp_ctr_sin_pend_r  | pp_ctr_sin_dirty_w"
                      " | PP_CTR_SIN_N_C'(crf_dirty_p_w);\n")]),
    "X02_also_sin_last_aaf": ("nxn nxn8", "RED: STREAM_INPUT N only",
        "CRF pulse also raises AAF STREAM_INPUT N-1 (the CRF row's neighbour)",
        [(A_SIN_NEXT, "    pp_ctr_sin_pend_n  = pp_ctr_sin_pend_r  | pp_ctr_sin_dirty_w"
                      " | (PP_CTR_SIN_N_C'(crf_dirty_p_w) << (N_STREAMS - 1));\n")]),
    "X03_misroute_to_n_minus_1": ("nxn nxn8", "RED: STREAM_INPUT N only",
        "CRF pulse delivered at STREAM_INPUT N-1 INSTEAD of N",
        [(A_SIN_DIRTY, "    assign pp_ctr_sin_dirty_w = {1'b0, avtprx_dirty_p_w"
                       " | (N_STREAMS'(crf_dirty_p_w) << (N_STREAMS - 1))};\n")]),
    "X04_also_sout_n": ("nxn nxn8", "RED: no STREAM_OUTPUT row",
        "CRF pulse also raises STREAM_OUTPUT N (the CRF Media Clock Output)",
        [(A_SOUT_NEXT, "    pp_ctr_sout_pend_n = pp_ctr_sout_pend_r | tkd_dirty_p_w"
                       " | (ACMP_SRC_C'(crf_dirty_p_w) << N_STREAMS);\n")]),
    "X05_also_sout0": ("nxn nxn8", "RED: no STREAM_OUTPUT row",
        "CRF pulse also raises STREAM_OUTPUT 0",
        [(A_SOUT_NEXT, "    pp_ctr_sout_pend_n = pp_ctr_sout_pend_r | tkd_dirty_p_w"
                       " | ACMP_SRC_C'(crf_dirty_p_w);\n")]),
    "X06_also_avb": ("nxn nxn8", "RED: nor AVB_INTERFACE 0 or CLOCK_DOMAIN 0",
        "CRF pulse also raises AVB_INTERFACE 0",
        [(A_AVB_NEXT, "    pp_ctr_avb_pend_n  = pp_ctr_avb_pend_r  | ctr_avb_dirty_w | crf_dirty_p_w;\n")]),
    "X07_also_ckd": ("nxn nxn8", "RED: nor AVB_INTERFACE 0 or CLOCK_DOMAIN 0",
        "CRF pulse also raises CLOCK_DOMAIN 0",
        [(A_CKD_NEXT, "    pp_ctr_ckd_pend_n  = pp_ctr_ckd_pend_r  | ctr_ckd_dirty_w | crf_dirty_p_w;\n")]),
    "X08_also_avb_as_ix1": ("nxn nxn8", "RED: nor any tuple of another type or index",
        "CRF pulse also raises AVB, and the arbiter hands AVB out as {AVB_INTERFACE, 1}",
        [(A_AVB_NEXT, "    pp_ctr_avb_pend_n  = pp_ctr_avb_pend_r  | ctr_avb_dirty_w | crf_dirty_p_w;\n"),
         (A_AVB_TYPE, "          pp_ctr_evt_type_w  = DESC_AVB_INTERFACE_C;\n"
                      "          pp_ctr_evt_index_w = 16'd1;\n")]),
    "X09_crf_as_foreign_type": ("nxn nxn8", "RED: STREAM_INPUT N only / another type",
        "the CRF row handed out as type 0x000E (not STREAM_INPUT) at index N",
        [(A_SIN_IDX, "          pp_ctr_evt_index_w = 16'(pick);\n"
                     "          if " + CRF_ROW + " pp_ctr_evt_type_w = 16'h000E;\n")]),
    "X10_crf_at_undeclared_n_plus_1": ("nxn nxn8", "RED: STREAM_INPUT N only",
        "the CRF row handed out as STREAM_INPUT N+1 (undeclared)",
        [(A_SIN_IDX, "          pp_ctr_evt_index_w = " + CRF_ROW + " ? 16'(pick + 1) : 16'(pick);\n")]),
    "X11_crf_at_index_plus_64": ("nxn nxn8", "RED: STREAM_INPUT N only / another index",
        "the CRF row handed out as STREAM_INPUT N+64 (past the harness bitmap)",
        [(A_SIN_IDX, "          pp_ctr_evt_index_w = " + CRF_ROW + " ? 16'(pick + 64) : 16'(pick);\n")]),
    "X13_dirty_source_removed": ("nxn notify", "RED: bind edge on nxn; every [NOTIFY-CRF] incl. A's copy",
        "the CRF row's Table 5.22 source tied off",
        [(A_SIN_DIRTY, "    assign pp_ctr_sin_dirty_w = {1'b0, avtprx_dirty_p_w};\n")]),
    "X14_pending_clear_below_crf": ("notify", "RED: the two quiet checks",
        "the pending-clear loop stops below the CRF row",
        [("    for (int unsigned s = 0; s < PP_CTR_SIN_N_C; s++) begin\n",
          "    for (int unsigned s = 0; s < N_STREAMS; s++) begin\n")]),
    "X12_also_sout_n_late200": ("nxn", "CHARACTERISATION (window bound): expected GREEN",
        "CRF pulse also raises STREAM_OUTPUT N, but 200 cycles later (outside the 64-step window)",
        [(A_ARB_ANCHOR,
          "  logic [7:0] r269_dly_r = 8'd0;\n"
          "  logic       r269_arm_r = 1'b0;\n"
          "  always_ff @(posedge axis_clk) begin : r269_late\n"
          "    if (crf_dirty_p_w) begin r269_arm_r <= 1'b1; r269_dly_r <= 8'd0; end\n"
          "    else if (r269_arm_r) begin\n"
          "      r269_dly_r <= r269_dly_r + 8'd1;\n"
          "      if (r269_dly_r == 8'd200) r269_arm_r <= 1'b0;\n"
          "    end\n"
          "  end : r269_late\n"
          "  wire r269_late_p = r269_arm_r && (r269_dly_r == 8'd200);\n" + A_ARB_ANCHOR),
         (A_SOUT_NEXT, "    pp_ctr_sout_pend_n = pp_ctr_sout_pend_r | tkd_dirty_p_w"
                       " | (ACMP_SRC_C'(r269_late_p) << N_STREAMS);\n")]),
}

H_OTHER_ELSE = ("            else\n"
                "                pp_ctr_evt_other_n++;\n")
H_WINDOW_ANCHOR = ("        pp_ctr_evt_other_n = 0;\n"
                   "        crf_lever(true);\n")
H_STEP_ANCHOR = "        if (dut->rootp->milan_datapath__DOT__pp_ctr_evt_valid_w) {\n"
H_G_ANCHOR = ("        const std::vector<uint8_t> g = aecp_xact_from(CTL_B, 0x0029, notify_sq++, key);\n")

H_ACOPY_ANCHOR = "        ck(\"[NOTIFY-CRF] ...and so is A's copy\""

HARNESS = {
    # one counters-block bit of A's logged push flipped: only the A-copy check
    # may turn red, so it is shown to read A's copy and nothing else
    "H3_flip_a_copy": ("notify", "RED: only [NOTIFY-CRF] ...and so is A's copy",
        "flip one counters-block bit of controller A's logged CRF push before the A-copy check",
        [(H_ACOPY_ANCHOR,
          "        for (size_t r269_i = uns_log.size(); r269_i-- > 0;) {\n"
          "            std::vector<uint8_t>& r269_f = uns_log[r269_i];\n"
          "            if (aecp_is_unsolicited(r269_f) && notify_cmd(r269_f) == 0x0029\n"
          "                && notify_to(r269_f, CTL_A) && r269_f.size() > 60) {\n"
          "                r269_f[60] ^= 0x01; break; }\n"
          "        }\n" + H_ACOPY_ANCHOR)]),
    # the fifth record removed: a tuple the four cannot hold is dropped again
    "H1_no_other_record": ("nxn", "with X08: expected GREEN (shows the fifth record is load-bearing)",
        "observer drops a tuple none of the four records can hold (round-1 behaviour)",
        [(H_OTHER_ELSE, "")]),
    # instrumentation only, no check changed: when each delivery lands in the
    # bind-edge window, and whether the solicited exchange appends to uns_log
    "H2_instrument": ("nxn nxn8 notify", "instrumentation: all checks unchanged",
        "print each arbiter delivery inside the bind-edge window with its step number, "
        "and uns_log size/capacity around the [NOTIFY-CRF] solicited exchange",
        [(H_STEP_ANCHOR, "        if (r269_win_on) r269_win_step++;\n" + H_STEP_ANCHOR
                         + "            if (r269_win_on) printf(\"  [r269] window step %ld: type 0x%04x index %u\\n\","
                           " r269_win_step, (unsigned)dut->rootp->milan_datapath__DOT__pp_ctr_evt_type_w,"
                           " (unsigned)dut->rootp->milan_datapath__DOT__pp_ctr_evt_index_w);\n"),
         ("    void step() {\n", "    bool r269_win_on = false; long r269_win_step = 0;\n    void step() {\n"),
         (H_WINDOW_ANCHOR, "        pp_ctr_evt_other_n = 0;\n        r269_win_on = true; r269_win_step = 0;\n"
                           "        crf_lever(true);\n        r269_win_on = false;\n"
                           "        printf(\"  [r269] bind-edge window: %ld steps\\n\", r269_win_step);\n"),
         (H_G_ANCHOR, "        const size_t r269_n0 = uns_log.size(), r269_c0 = uns_log.capacity();\n"
                      + H_G_ANCHOR
                      + "        printf(\"  [r269] uns_log across the solicited exchange: size %zu -> %zu, capacity %zu -> %zu\\n\","
                        " r269_n0, uns_log.size(), r269_c0, uns_log.capacity());\n")]),
}


def apply(text, edits, name):
    for anchor, repl in edits:
        n = text.count(anchor)
        if n != 1:
            sys.exit(f"{name}: anchor occurs {n} times, need exactly 1:\n{anchor}")
        text = text.replace(anchor, repl)
    return text


def main():
    tree, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    rtl = (tree / "hdl/milan/milan_datapath.sv").read_text()
    cpp = (tree / "tb/verilator/milan_dp/sim_nxn.cpp").read_text()
    rows = []
    for name, (legs, exp, desc, edits) in RTL.items():
        d = out / name
        d.mkdir(parents=True, exist_ok=True)
        (d / "milan_datapath.sv").write_text(apply(rtl, edits, name))
        rows.append((name, "rtl", legs, exp, desc))
    for name, (legs, exp, desc, edits) in HARNESS.items():
        d = out / name
        d.mkdir(parents=True, exist_ok=True)
        (d / "sim_nxn.cpp").write_text(apply(cpp, edits, name))
        rows.append((name, "harness", legs, exp, desc))
    with open(out / "MUTANTS.tsv", "w") as f:
        f.write("name\tkind\tlegs\texpectation\tdescription\n")
        for r in rows:
            f.write("\t".join(r) + "\n")
    print(f"{len(rows)} mutants written to {out}")


if __name__ == "__main__":
    main()
