#!/usr/bin/env python3
"""make_arm_patches.py <tree> [arm...]: write tb/srp_top/mutations/<arm>.patch for each arm below (all, or the
named ones), each a list of exact text replacements in the processor tree, as three-line-context unified diffs (one
per file, in the order the files first appear). Refuses an edit whose old text does not occur exactly once in the
file as the earlier edits of the arm left it.

Two kinds of arm: those re-expressed for issue #216 because the code they edit changed (same name, same intent, same
rows in tb/srp_top/mutants.py), and the new arms of issue #216.
"""
import difflib
import sys
from pathlib import Path

DOM = "hdl/srp/KL_srp_domain.sv"
VLAN = "hdl/srp/KL_srp_vlan.sv"
TOP = "hdl/srp/KL_srp_top.sv"
ENC = "hdl/srp/KL_srp_encoder.sv"
TALK = "hdl/srp/KL_srp_talker_fsm.sv"
LSTN = "hdl/srp/KL_srp_listener_fsm.sv"

ARMS = {
    # ---- re-expressed: the Domain Registrar (issue #184), unchanged code, moved lines
    "domain-adoption-drops-registrar": [
        (DOM, "        reg_in_r            <= pend_in_nx_w;  // the adopted value's Registrar\n",
              "        reg_in_r            <= 1'b0;  // the adopted value's Registrar\n")],
    "domain-capture-unregistered": [
        (DOM, "        pend_in_r      <= 1'b1;           // registered by this very event\n", "")],
    "domain-leaveall-after-receive": [
        (DOM, "    if (rxdom_lv_i && rx_is_pend_w)    pend_in_nx_w = 1'b0;\n",
              "    if (rxdom_lv_i && rx_is_pend_w)    pend_in_nx_w = 1'b0;\n"
              "    if (leaveall_tick_i && declared_r) reg_in_nx_w  = 1'b0;\n")],
    "domain-link-keeps-registrar": [
        (DOM, "        reg_in_r      <= 1'b0;             // Flush!: every Registrar to MT\n", ""),
        (DOM, "        reg_in_r   <= 1'b0;                // Begin!: nothing registered yet\n", "")],
    "domain-pending-lv-ignored": [
        (DOM, "    if (rxdom_lv_i && rx_is_pend_w)    pend_in_nx_w = 1'b0;\n", "")],
    # ---- re-expressed: the Domain re-join, now the Applicant's sJ at tx!
    "domain-rejoin-always-joinin": [
        (DOM, "    tx_msg_w  = srp_app_msg(app_per_w, tx_la_w, reg_in_nx_w);\n",
              "    tx_msg_w  = srp_app_msg(app_per_w, tx_la_w, 1'b1);\n")],
    "domain-rejoin-always-joinmt": [
        (DOM, "    tx_msg_w  = srp_app_msg(app_per_w, tx_la_w, reg_in_nx_w);\n",
              "    tx_msg_w  = srp_app_msg(app_per_w, tx_la_w, 1'b0);\n")],
    # a received LeaveAll's re-join sent at the request, not at the next tx!
    "domain-rejoin-at-request": [
        (DOM, "  assign tx_serve_w = (txp_r || tx_tick_i) && !q1_valid_r\n",
              "  assign tx_serve_w = (txp_r || tx_tick_i || leaveall_tick_i) && !q1_valid_r\n")],
    # a received LeaveAll's re-join dropped: rLA! never reaches the Applicant
    "domain-rx-leaveall-dropped": [
        (DOM, "    app_la_w  = (leaveall_tick_i && !leaveall_own_i && declared_r)\n",
              "    app_la_w  = (1'b0 && leaveall_tick_i && !leaveall_own_i && declared_r)\n")],
    # ---- re-expressed: the KL_srp_top wiring of the Domain (moved lines)
    "top-domain-lv-unwired": [
        (TOP, "      .rxdom_lv_i          (dom_rx_lv_w),\n", "      .rxdom_lv_i          (1'b0),\n")],
    "top-domain-tx-every-clock": [
        (TOP, "      .tx_tick_i           (join_fsm_w),\n", "      .tx_tick_i           (1'b1),\n")],
    "top-domain-tx-unwired": [
        (TOP, "      .tx_tick_i           (join_fsm_w),\n", "      .tx_tick_i           (1'b0),\n")],
    # ---- re-expressed: the VLAN declaration-on-the-wire state (issue #65), the walk's hand-over
    "join-sent-at-handover": [
        (VLAN, "            if (ev_decl_r) queued_r[widx_r] <= 1'b1;   // its declaration handed over\n",
               "            if (ev_decl_r) sent_r[widx_r] <= 1'b1;   // its declaration handed over\n")],
    "count-up-unsends": [
        (VLAN, "              // another user of a live VID: the count goes up (tbl_wmux), silent\n",
               "              // another user of a live VID: the count goes up (tbl_wmux), silent\n"
               "              sent_r[found_ix_r] <= 1'b0;\n")],
    # ---- re-expressed: the cadence plane (moved lines)
    "leaveall-expiry-lost": [
        (TOP, "  assign cad_hit_w       = exp_valid_i && (cad_exp_ix_w < N_CAD_C);\n",
              "  assign cad_hit_w       = exp_valid_i && (cad_exp_ix_w != CAD_LA_MSRP_C) && (cad_exp_ix_w < N_CAD_C);\n")],
    "reset-retains-intent": [
        (TOP, "      la_wait_r         <= 1'b0;\n", "      // pending preparation incorrectly retained at reset\n")],
    "my-expiry-pulse": [
        (TOP, "  logic       la_msrp_pend_r;  // timer intent, not a registrar event\n",
              "  logic       la_msrp_pend_r;  // timer intent, not a registrar event\n  logic       my_exp_r;\n"),
        (TOP, "      .leaveall_own_i      (p_la_msrp_w),\n      .txop_done_o         (tk_txop_done_w),\n",
              "      .leaveall_own_i      (p_la_msrp_w || my_exp_r),\n      .txop_done_o         (tk_txop_done_w),\n"),
        (TOP, "      .leaveall_own_i          (p_la_msrp_w),\n",
              "      .leaveall_own_i          (p_la_msrp_w || my_exp_r),\n"),
        (TOP, "      la_mvrp_pend_r    <= 1'b0;\n", "      la_mvrp_pend_r    <= 1'b0;\n      my_exp_r <= 1'b0;\n"),
        (TOP, "      p_tx_mvrp_r  <= 1'b0;\n", "      p_tx_mvrp_r  <= 1'b0;\n      my_exp_r <= 1'b0;\n"),
        (TOP, "              la_msrp_pend_r <= 1'b1;  // wait for a supported sLA opportunity\n",
              "              la_msrp_pend_r <= 1'b1;  // wait for a supported sLA opportunity\n"
              "              my_exp_r <= 1'b1;\n")],
    # the own MVRP LeaveAll sent at the expiry, not at the tx! (Table 10-5 Active)
    "mvrp-flag-at-expiry": [
        (TOP, "              la_mvrp_pend_r <= 1'b1;  // Active: sLA at the next MVRP tx!\n",
              "              enc_la_r[1]    <= 1'b1;\n")],
    "mvrp-stale-expiry-honoured": [
        (TOP, "            if (!la_rearm_w[1]) begin\n              la_mvrp_pend_r <= 1'b1;  // Active: sLA at the next MVRP tx!\n",
              "            if (1'b1) begin\n              la_mvrp_pend_r <= 1'b1;  // Active: sLA at the next MVRP tx!\n")],
    # a peer MVRP LeaveAll on the tx! edge does not win over the own sLA
    "r-flag-ignores-edge-peer": [
        (TOP, "        p_tx_mvrp_la_r   <= la_mvrp_pend_r && !dec_la_mvrp_w;\n        mla_r            <= la_mvrp_pend_r && !dec_la_mvrp_w;\n",
              "        p_tx_mvrp_la_r   <= la_mvrp_pend_r;\n        mla_r            <= la_mvrp_pend_r;\n")],
    # ---- re-expressed: the encoder's push face and MVRP start (moved lines)
    "push-taken-in-alloc": [
        (ENC, "  assign busy_app_w  = (st_r != E_IDLE) && (st_r != E_COLLECT)\n",
              "  assign busy_app_w  = (st_r != E_IDLE) && (st_r != E_COLLECT) && (st_r != E_ALLOC)\n")],
    "r-collect-blocks-pushes": [
        (ENC, "  assign busy_app_w  = (st_r != E_IDLE) && (st_r != E_COLLECT)\n",
              "  assign busy_app_w  = (st_r != E_IDLE)\n")],
    "r-mvrp-start-during-prepare": [
        (ENC, "  assign start1_w = (st_r == E_IDLE) && !la_prepare_i && !start0_w && go1_w\n",
              "  assign start1_w = (st_r == E_IDLE) && !start0_w && go1_w\n")],

    # ================= issue #216: the new arms =================
    # acceptance: one New (the Domain's declaration enters AN, as the base sent it)
    "domain-one-new": [
        (DOM, "        app_r      <= SRP_AP_VN_C;\n", "        app_r      <= SRP_AP_AN_C;\n")],
    # acceptance: one New (a VID's first user enters AN)
    "vlan-one-new": [
        (VLAN, "      2'd0:    one_nx_w = srp_app_next(one_st_w, SRP_AE_NEW_C, reg_nx_w[one_ix_w], p2p_i);\n",
               "      2'd0:    one_nx_w = SRP_AP_AN_C;\n")],
    # acceptance: JoinIn with the Registrar MT (the base's always-JoinIn re-join)
    "vlan-joinin-registrar-mt": [
        (VLAN, "    wmsg_w = srp_app_msg(app_ev_w[widx_r], wla_r, reg_nx_w[widx_r]);\n",
               "    wmsg_w = srp_app_msg(app_ev_w[widx_r], wla_r, 1'b1);\n")],
    # acceptance: LeaveAll stopped with the last declaration (an MVRP drain needs content)
    "mvrp-leaveall-needs-content": [
        (ENC, "                 && ((cnt_mvrp_r != '0) || la_pend_r[1] || leaveall_i[1]);\n",
              "                 && (cnt_mvrp_r != '0);\n")],
    # the MVRP round's LeaveAll dropped on its way to the drain
    "top-mvrp-la-flag-dropped": [
        (TOP, "        enc_la_r[1]   <= mla_r;\n", "        enc_la_r[1]   <= 1'b0;\n")],
    # the MVRP drain at the tick, not after the VID walk
    "top-mvrp-drain-at-tick": [
        (TOP, "      if (mrnd_act_r && vlan_tx_done_w) begin\n", "      if (mrnd_act_r) begin\n")],
    # the MSRP drain does not wait for the Domain's tx!
    "top-round-ignores-domain": [
        (TOP, "          && (td_dom_r || dom_tx_done_w)) begin\n", "          ) begin\n")],
    # the own LeaveAll's tx! takes the tx! row
    "domain-txla-row-ignored": [
        (DOM, "    tx_la_w   = txp_la_r || leaveall_own_i;\n", "    tx_la_w   = 1'b0;\n")],
    # the Domain's tx! done when served, before its message is in the encoder
    "domain-tx-done-at-serve": [
        (DOM, "      if (txw_r && !tx_serve_w && q_empty_w) begin\n", "      if (txw_r && !tx_serve_w) begin\n")],
    # a tx! that finds the queue full is dropped, not owed
    "domain-tx-owed-dropped": [
        (DOM, "      if (tx_tick_i && !tx_serve_w) begin\n        txp_r    <= 1'b1;\n",
              "      if (tx_tick_i && !tx_serve_w) begin\n        txp_r    <= 1'b0;\n")],
    # received messages of the declared value never reach the Applicant
    "domain-applicant-deaf": [
        (DOM, "    app_rx_w  = (rxdom_any_i && rx_is_decl_w)\n", "    app_rx_w  = (1'b0 && rx_is_decl_w)\n")],
    # received messages of any Class A Domain value move the Applicant
    "domain-applicant-any-value": [
        (DOM, "    app_rx_w  = (rxdom_any_i && rx_is_decl_w)\n",
              "    app_rx_w  = (rxdom_any_i && declared_r && covers6_w)\n")],
    # the talker and listener Applicants: tx! from VN goes to AA (one New)
    "talker-one-new": [
        (TALK, "          A_VN_C:  nx = A_AN_C;\n          A_AN_C:  nx = reg_in_i ? A_QA_C : A_AA_C;   // note 8\n",
               "          A_VN_C:  nx = A_AA_C;\n          A_AN_C:  nx = reg_in_i ? A_QA_C : A_AA_C;   // note 8\n")],
    "listener-one-new": [
        (LSTN, "          A_VN_C:  nx = A_AN_C;\n          A_AN_C:  nx = reg_in_i ? A_QA_C : A_AA_C;   // note 8\n",
               "          A_VN_C:  nx = A_AA_C;\n          A_AN_C:  nx = reg_in_i ? A_QA_C : A_AA_C;   // note 8\n")],
    # ---- the VID Registrar and Applicant (issue #216)
    "vlan-registrar-never-in": [
        (VLAN, "        reg_nx_w[i] = 1'b1;                               // rNew / rJoinIn / rJoinMt\n",
               "        reg_nx_w[i] = reg_nx_w[i];                        // rNew / rJoinIn / rJoinMt\n")],
    "vlan-rlv-ignored": [
        (VLAN, "      if (rx_hit_w[i] && (rx_ev_i == SRP_EV_LV))\n        reg_nx_w[i] = 1'b0;                               // rLv!: IN -> LV\n",
               "")],
    "vlan-rx-any-vid": [
        (VLAN, "      rx_hit_w[i] = rx_valid_i && alloc_r[i] && (rx_vid_i == {4'd0, vid_q_r[i]});\n",
               "      rx_hit_w[i] = rx_valid_i && alloc_r[i];\n")],
    "vlan-s-registers": [
        (VLAN, "                          || (rx_ev_i == SRP_EV_JOINMT)))\n",
               "                          || (rx_ev_i == SRP_EV_JOINMT) || (rx_ev_i == SRP_EV_IN)\n"
               "                          || (rx_ev_i == SRP_EV_MT)))\n")],
    "vlan-leaveall-keeps-in": [
        (VLAN, "      if (leaveall_tick_i || (walk_start_w && (txp_la_r || tx_la_i)))\n",
               "      if (walk_start_w && (txp_la_r || tx_la_i))\n")],
    "vlan-rx-loses-to-leaveall": [
        (VLAN, "      if (leaveall_tick_i || (walk_start_w && (txp_la_r || tx_la_i)))\n        reg_nx_w[i] = 1'b0;                               // rLA! / txLA!: IN -> LV\n", ""),
        (VLAN, "        reg_nx_w[i] = 1'b0;                               // rLv!: IN -> LV\n",
               "        reg_nx_w[i] = 1'b0;                               // rLv!: IN -> LV\n"
               "      if (leaveall_tick_i || (walk_start_w && (txp_la_r || tx_la_i)))\n"
               "        reg_nx_w[i] = 1'b0;                               // rLA! / txLA!: IN -> LV\n")],
    "vlan-txla-keeps-in": [
        (VLAN, "      if (leaveall_tick_i || (walk_start_w && (txp_la_r || tx_la_i)))\n",
               "      if (leaveall_tick_i)\n")],
    "vlan-applicant-deaf": [
        (VLAN, "      app_ev_w[i] = rx_hit_w[i] ? rx_nx_w : app_r[i];\n",
               "      app_ev_w[i] = app_r[i];\n")],
    "vlan-note8-ignores-registrar": [
        (VLAN, "      2'd2:    one_nx_w = srp_app_next(one_st_w, SRP_AE_TX_C, reg_nx_w[one_ix_w], p2p_i);\n",
               "      2'd2:    one_nx_w = srp_app_next(one_st_w, SRP_AE_TX_C, 1'b0, p2p_i);\n")],
    "vlan-registrar-kept-on-allocation": [
        (VLAN, "              reg_r[free_ix_r]    <= 1'b0;         // a new Registrar: MT (Begin!)\n", "")],
    "vlan-leave-abandoned": [
        (VLAN, "              if (app_idle_f(app_nx_w[found_ix_r])) alloc_r[found_ix_r] <= 1'b0;\n",
               "              alloc_r[found_ix_r] <= 1'b0;\n")],
    "vlan-rejoin-of-leaving-allocates": [
        (VLAN, "            if (alloc_r[chk_ix_r] && (vid_q_r[chk_ix_r] == op_vid_r)) begin\n",
               "            if (active_r[chk_ix_r] && (vid_q_r[chk_ix_r] == op_vid_r)) begin\n")],
    "vlan-walk-frees-lo": [
        (VLAN, "    return st inside {SRP_AP_VO_C, SRP_AP_AO_C, SRP_AP_QO_C};\n",
               "    return st inside {SRP_AP_VO_C, SRP_AP_AO_C, SRP_AP_QO_C, SRP_AP_LO_C};\n")],
}


def arm_patch(tree: Path, arm: str) -> str:
    texts: dict[str, str] = {}
    order: list[str] = []
    for path, old, new in ARMS[arm]:
        if path not in texts:
            texts[path] = (tree / path).read_text()
            order.append(path)
        n = texts[path].count(old)
        assert n == 1, (arm, path, n, old[:60])
        texts[path] = texts[path].replace(old, new)
    out = []
    for path in order:
        src = (tree / path).read_text()
        out += difflib.unified_diff(src.splitlines(keepends=True), texts[path].splitlines(keepends=True),
                                    fromfile="a/" + path, tofile="b/" + path, n=3)
    return "".join(out)


def main() -> int:
    tree = Path(sys.argv[1])
    for arm in sys.argv[2:] or list(ARMS):
        (tree / "tb/srp_top/mutations" / (arm + ".patch")).write_text(arm_patch(tree, arm))
        print(arm)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
