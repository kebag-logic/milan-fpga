#!/usr/bin/env python3
"""Reviewer mutants R391-3 (disposable). Each entry is a list of exact edits
(path, old, new); every old text must occur exactly once in the tree.

The R391-2 set is re-planted at the round-3 head (anchors refreshed where the
round-3 RTL moved them), plus the reviewer's own mutants against the pre-proof
path of the clarified aggregate (issue #131, 5876655419).
"""

W = "hdl/aecp/KL_aecp_nvm_writer.sv"
T = "hdl/top/protocol_processor_top.sv"
V = "hdl/packet_engine/KL_pp_rx_validator.sv"
SH = "hdl/acmp/KL_acmp_nvm_shadow.sv"
HOLD = "  assign aecp_rx_hold_w = !d3_done_w && ((aecp_rx_res_r != '0) || aecp_rx_in_w);"
LIVE = "assign agg_live_w   = (agg_run_r || rs_go_i) && !agg_fired_r && !done_r && !closed_r;"
TMO = ("  assign rs_tmo_w   = (rs_stall_w && ((rs_wd_r >= 32'(RS_TMO_CYC_P - 1)) || rs_agg_i))\n"
       "                    || ((hs_r == H_RS_REQ) && rs_agg_i);\n")

MUTANTS = {
    # ---- R391-1 / R391-2 set, re-run ----
    "rate_walk_stuck_on_first_lane": [(W,
        "lane_off_r <= SSR_LIST_OFF_C + (16'(walk_next_w) << 2);",
        "lane_off_r <= SSR_LIST_OFF_C;")],
    "rate_walk_unbounded": [(W,
        "lane_refuse_w = (walk_next_w == SSR_WALK_MAX_C)\n                      || (rcount_r == 16'(walk_next_w));",
        "lane_refuse_w = (rcount_r == 16'(walk_next_w));")],
    "pass1_read_not_drained": [(W,
        "assign m_abort_o  = expire_w && (ws_r == W_RD);",
        "assign m_abort_o  = expire_w && (ws_r == W_RD) && !pass_r;")],
    "judge_wait_unwatched": [(W, "W_JUDGE: stall_w = jd_wait_i;", "W_JUDGE: stall_w = 1'b0;")],
    "backoff_holds_dispatch": [(W,
        "assign own_o = !done_r || (ss_r == S_ACQ) || latch_w;",
        "assign own_o = !done_r || (ss_r == S_ACQ) || latch_w || (ss_r == S_BACKOFF);")],
    "disagree_whole_then_blank_only": [(W,
        "&& (rd_whole_w != whole0_r[rec_r]);",
        "&& (!rd_whole_w && whole0_r[rec_r]);")],
    "rollback_strobe_one_cycle": [(W,
        "if (rb_min_r && !desc_debt_i) ws_r <= W_RELOC;",
        "if (!desc_debt_i) ws_r <= W_RELOC;")],
    "agg_fires_with_event_in_hand": [(W,
        "  assign agg_expire_w = agg_live_w && (agg_r >= 32'(RS_AGG_CYC_P - 1))\n                        && (stall_w || !wait_w);",
        "  assign agg_expire_w = agg_live_w && (agg_r >= 32'(RS_AGG_CYC_P - 1));")],
    "agg_not_stopped_at_terminal": [(W, LIVE,
        "assign agg_live_w   = (agg_run_r || rs_go_i) && !agg_fired_r;")],
    "agg_not_one_shot": [(W, LIVE,
        "assign agg_live_w   = (agg_run_r || rs_go_i) && !done_r && !closed_r;")],
    "hold_admits_two": [(T, HOLD,
        "  assign aecp_rx_hold_w = !d3_done_w && ((aecp_rx_res_r > 'd1) || (aecp_rx_res_r != '0 && aecp_rx_in_w));")],
    "hold_released_in_closed": [(T, HOLD,
        "  assign aecp_rx_hold_w = !d3_done_w && !d3_closed_w && ((aecp_rx_res_r != '0) || aecp_rx_in_w);")],
    "held_gate_drops_every_subtype": [(V,
        "                       && (rx_data_i == SUB_AECP_C) && (da_own_r | da_mcast_r);",
        "                       && (da_own_r | da_mcast_r);")],
    "resident_counts_acmp": [(T, "                         && (v_hdr_protocol_w != 3'(PP_PROTO_ACMP))\n", "")],
    "resident_never_returned": [(T,
        "  assign aecp_rx_out_w = {1'b0, aecp_rxs_free_w} + {1'b0, aecp_rxs_free_i};",
        "  assign aecp_rx_out_w = 2'd0;")],
    # ---- R391-3: the reviewer's own mutants against the pre-proof path ----
    # agg_o a one-clock pulse on the expiry instead of a level held until
    # reset: a binding walk whose byte is in hand on that clock never sees it
    "agg_o_pulse": [(W, "  assign agg_o        = agg_fired_r;\n",
                        "  assign agg_o        = agg_expire_w;\n")],
    # the binding walk honours the aggregate only between records (H_RS_REQ),
    # never inside a record's stream
    "bind_agg_only_between_records": [(SH, TMO,
        "  assign rs_tmo_w   = (rs_stall_w && (rs_wd_r >= 32'(RS_TMO_CYC_P - 1)))\n"
        "                    || ((hs_r == H_RS_REQ) && rs_agg_i);\n")],
    # the binding walk takes the aggregate at once, byte in hand or not (the
    # stall qualifier dropped in H_RS_STREAM): the byte in hand is orphaned
    "bind_agg_ignores_byte_in_hand": [(SH, TMO,
        "  assign rs_tmo_w   = (rs_stall_w && (rs_wd_r >= 32'(RS_TMO_CYC_P - 1)))\n"
        "                    || (((hs_r == H_RS_REQ) || (hs_r == H_RS_STREAM)) && rs_agg_i);\n")],
    # the proof past the bound tests the fired level, not the count: a proof
    # landing on the bound's own clock (its answer in hand, so unfired) reads on
    "proof_past_bound_needs_fired": [(W,
        "  assign agg_past_w   = agg_run_r && (agg_r >= 32'(RS_AGG_CYC_P - 1));\n",
        "  assign agg_past_w   = agg_fired_r;\n")],
    # a pre-proof expiry closes the image walk even when the LOCATE then hits
    # (the proof's DEFAULTS path taken only from W_IMG)
    "proof_default_only_from_img": [(W,
        "      if (proof_w && agg_past_w) begin\n",
        "      if (proof_w && agg_past_w && (ws_r == W_IMG)) begin\n")],
}
