#!/usr/bin/env python3
"""mkpatch.py <repo> [label ...]: cut the issue #212 arms of tb/srp_top/mutations from one exact edit each.

Each arm replaces unique texts of one RTL file; the patch is `diff -u` of the file before and after,
with the a/ b/ prefixes git apply takes. With labels, only those arms are cut.
"""
import difflib
import sys
from pathlib import Path

LS = "hdl/srp/KL_srp_listener_fsm.sv"
TOP = "hdl/srp/KL_srp_top.sv"

ARMS = {
    # ---- round 1 (issue #212), cut again where the settle block moved: the same edits
    "pt-seed-dropped": (LS, [(
        "    seed_v_w = ctl_valid_i && !evt_valid_i && ctl_settle_i\n",
        "    seed_v_w = 1'b0 && ctl_valid_i && !evt_valid_i && ctl_settle_i\n")]),
    # the whole pre-settle path removed (the behaviour before the issue):
    # no seed, no kept registration, no declaration in the parked Leave's walk
    "presettle-removed": (LS, [(
        "    seed_v_w = ctl_valid_i && !evt_valid_i && ctl_settle_i\n",
        "    seed_v_w = 1'b0 && ctl_valid_i && !evt_valid_i && ctl_settle_i\n"), (
        "    keep_v_w = ctl_acc_w && ctl_settle_i && kset_w[ctl_sink_i]\n",
        "    keep_v_w = 1'b0 && ctl_acc_w && ctl_settle_i && kset_w[ctl_sink_i]\n"), (
        "          if (pk_decl_w) begin\n",
        "          if (1'b0 && pk_decl_w) begin\n")]),
    "pt-never-holds": (LS, [(
        "      pt_alloc_w[e] = pt_rx_w && rx_registering_w && (pt_hit_w == '0)\n",
        "      pt_alloc_w[e] = 1'b0 && pt_rx_w && rx_registering_w && (pt_hit_w == '0)\n")]),
    "seed-type-advertise": (LS, [(
        "        seed_type_w  = seed_type_w  | pt_type_r[e];\n",
        "        seed_type_w  = seed_type_w;\n")]),
    "seed-drops-failure-information": (LS, [(
        "        seed_fcode_w = seed_fcode_w | pt_fcode_r[e];\n        seed_fsys_w  = seed_fsys_w  | pt_fsys_r[e];\n",
        "        seed_fcode_w = seed_fcode_w;\n        seed_fsys_w  = seed_fsys_w;\n")]),
    "seed-no-registered-strobe": (LS, [(
        "            evt_tk_registered_o[s]   <= 1'b1;\n",
        "            evt_tk_registered_o[s]   <= 1'b0;\n")]),
    "park-retire-declares-next-walk": (LS, [(
        "          if (pk_decl_w) begin\n",
        "          if (1'b0 && pk_decl_w) begin\n")]),
    "pt-rlv-ignored": (LS, [(
        "        if (pt_reg_r[e] == R_IN_C) pt_nreg_w[e] = R_MT_C;   // Δ13; LV: -x-\n",
        "        if (1'b0) pt_nreg_w[e] = R_MT_C;   // Δ13; LV: -x-\n")]),
    "pt-leavetimer-never-expires": (LS, [(
        "      pt_exp_w[e] = (pt_reg_r[e] == R_LV_C) && (pt_age_w[e] <= PT_SLACK_C);\n",
        "      pt_exp_w[e] = 1'b0;\n")]),
    "pt-leaveall-ignored": (LS, [(
        "      pt_la_w[e]  = leaveall_own_i\n"
        "                 || (pt_type_r[e] ? leaveall_rx_i[SRP_LA_TALKER_FAILED_C]\n"
        "                                  : leaveall_rx_i[SRP_LA_TALKER_ADV_C]);\n",
        "      pt_la_w[e]  = 1'b0;\n")]),
    "pt-leaveall-any-lane": (LS, [(
        "                 || (pt_type_r[e] ? leaveall_rx_i[SRP_LA_TALKER_FAILED_C]\n"
        "                                  : leaveall_rx_i[SRP_LA_TALKER_ADV_C]);\n",
        "                 || (|leaveall_rx_i);\n")]),
    "seed-lv-fresh-deadline": (LS, [(
        "        sdl_ms_r <= now_ms_i + 32'(seed_rem_w);   // the entry's deadline, absolute\n",
        "        sdl_ms_r <= now_ms_i + LEAVE_MS_P;\n")]),
    "seed-from-current-state": (LS, [(
        "        seed_reg_w   = seed_reg_w   | pt_nreg_w[e];\n",
        "        seed_reg_w   = seed_reg_w   | pt_reg_r[e];\n"), (
        "        seed_dl_w    = seed_dl_w    | pt_ndl_w[e];\n",
        "        seed_dl_w    = seed_dl_w    | pt_dl_r[e];\n")]),
    "pt-match-ignores-da": (LS, [(
        "                 && (pt_sid_r[e] == pt_qsid_w) && (pt_da_r[e] == pt_qda_w)\n",
        "                 && (pt_sid_r[e] == pt_qsid_w)\n")]),
    "pt-vid-high-bits-ignored": (LS, [(
        "    pt_rx_w = evt_valid_i && evt_msrp_i && (evt_vid_i[15:12] == 4'd0)\n",
        "    pt_rx_w = evt_valid_i && evt_msrp_i\n")]),
    "pt-allocation-overwrites-entry-0": (LS, [(
        "                   && (pt_reg_r[e] == R_MT_C) && !pt_taken_w;\n",
        "                   && ((pt_reg_r[e] == R_MT_C) || (e == 0)) && !pt_taken_w;\n")]),
    "park-retire-ignores-group": (LS, [(
        "        pk_alone_w = 1'b0;\n",
        "        pk_alone_w = 1'b1;\n")]),
    "park-retire-without-hold": (LS, [(
        "      pk_hold_w[s] = lvp_r[s] && (decl_pend_r[s] == D_DECLARE_C)\n",
        "      pk_hold_w[s] = 1'b0 && lvp_r[s] && (decl_pend_r[s] == D_DECLARE_C)\n")]),
    "seed-keeps-expiry-strobe": (LS, [(
        "            evt_tk_unregistered_o[s] <= 1'b0;\n",
        "")]),
    "listener-retire-skips-group-mark": (LS, [(
        "              if (same_w[wsrc_r][t]) wdone_r[t] <= 1'b1;\n",
        "              if (t == 32'(wsrc_r)) wdone_r[t] <= 1'b1;\n")]),
    "seed-lv-unguarded": (LS, [(
        "              if (seed_reg_w == R_LV_C) tpend_r[s] <= T_ARM_C;\n",
        "")]),
    # ---- round 2 (issue #212)
    # R770-1 F1: an unheld value is allocated IN on any Talker event (rLv, rIn, rMt too)
    "pt-alloc-any-event": (LS, [(
        "      pt_alloc_w[e] = pt_rx_w && rx_registering_w && (pt_hit_w == '0)\n",
        "      pt_alloc_w[e] = pt_rx_w && (pt_hit_w == '0)\n")]),
    # R770-1 F2: the port registrar keeps its first FailureInformation / its allocation's latency
    "pt-fcode-first-only": (LS, [(
        "        if (rx_is_failed_w) begin\n          pt_fcode_r[e] <= evt_failure_code_i;\n",
        "        if (rx_is_failed_w && (pt_alloc_w[e] || !pt_type_r[e])) begin\n"
        "          pt_fcode_r[e] <= evt_failure_code_i;\n")]),
    "pt-lat-on-alloc-only": (LS, [(
        "        pt_lat_r[e]  <= evt_acc_latency_i;\n",
        "        if (pt_alloc_w[e]) pt_lat_r[e]  <= evt_acc_latency_i;\n")]),
    "pt-type-on-alloc-only": (LS, [(
        "        pt_type_r[e] <= rx_is_failed_w;\n",
        "        if (pt_alloc_w[e]) pt_type_r[e] <= rx_is_failed_w;\n")]),
    # R770-1 F3: an A8 seeds as a settle does; rLv on an LV port registrar ends it (Table 10-4: -x-)
    "seed-on-teardown": (LS, [(
        "    seed_v_w = ctl_valid_i && !evt_valid_i && ctl_settle_i\n",
        "    seed_v_w = ctl_valid_i && !evt_valid_i\n")]),
    "pt-rlv-on-lv-ends": (LS, [(
        "        if (pt_reg_r[e] == R_IN_C) pt_nreg_w[e] = R_MT_C;   // Δ13; LV: -x-\n",
        "        pt_nreg_w[e] = R_MT_C;\n")]),
    # R769-1 F1: the A15 on the same triple keeps the sink's registration
    "rebind-same-not-kept": (LS, [(
        "    keep_v_w = ctl_acc_w && ctl_settle_i && kset_w[ctl_sink_i]\n",
        "    keep_v_w = 1'b0 && ctl_acc_w && ctl_settle_i && kset_w[ctl_sink_i]\n")]),
    "keep-ignores-da": (LS, [(
        "      kset_w[s] = rec_valid_r[s] && cset_w[s] && (da_r[s] == ctl_da_i)\n",
        "      kset_w[s] = rec_valid_r[s] && cset_w[s] && 1'b1\n")]),
    "keep-ignores-vlan": (LS, [(
        "               && (vid_r[s] == ctl_vid_i);\n",
        "               && 1'b1;\n")]),
    "keep-declares-seed-type": (LS, [(
        "            decl_fp_r[ctl_sink_i]   <= (keep_v_w ? rtype_r[ctl_sink_i] : seed_type_w)\n",
        "            decl_fp_r[ctl_sink_i]   <= seed_type_w\n")]),
    "keep-latency-strobe-dropped": (LS, [(
        "              evt_tk_latency_chg_o[s] <= (lat_r[s] != 32'd0);\n",
        "              evt_tk_latency_chg_o[s] <= 1'b0;\n")]),
    "unarmed-registrar-deaf": (LS, [(
        "      reg_rx_hit_w[s] = evt_valid_i && evt_msrp_i && rec_valid_r[s]\n",
        "      reg_rx_hit_w[s] = evt_valid_i && evt_msrp_i && armed_r[s]\n")]),
    "keep-ignores-expiry": (LS, [(
        "            && (reg_r[ctl_sink_i] != R_MT_C) && !kexp_w && !link_ev_w;\n",
        "            && (reg_r[ctl_sink_i] != R_MT_C) && !link_ev_w;\n")]),
    "keep-on-link-clock": (LS, [(
        "            && (reg_r[ctl_sink_i] != R_MT_C) && !kexp_w && !link_ev_w;\n",
        "            && (reg_r[ctl_sink_i] != R_MT_C) && !kexp_w;\n")]),
    # a sink not settled raises and publishes nothing
    "unarmed-indicates": (LS, [(
        "      ind_reg_w[s] = armed_r[s] && reg_rx_hit_w[s] && rx_registering_w\n",
        "      ind_reg_w[s] = reg_rx_hit_w[s] && rx_registering_w\n")]),
    "unarmed-fail-chg": (LS, [(
        "      ind_fchg_w[s] = armed_r[s] && fchg_cand_w[s] && rx_registering_w\n",
        "      ind_fchg_w[s] = fchg_cand_w[s] && rx_registering_w\n")]),
    "unarmed-unregistered": (LS, [(
        "        if (!armed_r[s]) begin\n          evt_tk_unregistered_o[s] <= 1'b0;\n",
        "        if (!armed_r[s]) begin\n")]),
    "unarmed-latency-strobe": (LS, [(
        "          evt_tk_latency_chg_o[s]  <= 1'b0;\n        end\n",
        "        end\n")]),
    "unarmed-publishes-latency": (LS, [(
        "      acc_latency_o[s] = armed_r[s] ? lat_r[s] : 32'd0;\n",
        "      acc_latency_o[s] = lat_r[s];\n")]),
    "unarmed-dbg-registrar": (LS, [(
        "      dbg_reg_state_o[s] = armed_r[s] ? reg_r[s] : R_MT_C;   // as tk_reg_state\n",
        "      dbg_reg_state_o[s] = reg_r[s];\n")]),
    # R770-1 F4: LINK_DOWN (Flush!) and LINK_UP (Begin!)
    "pt-link-flush-dropped": (LS, [(
        "      if (link_ev_w) begin\n        pt_nreg_w[e] = R_MT_C;                  // Flush! / Begin!: MT\n",
        "      if (1'b0) begin\n        pt_nreg_w[e] = R_MT_C;                  // Flush! / Begin!: MT\n")]),
    "link-begin-dropped": (LS, [(
        "  assign link_ev_w = (link_up_i != link_q_r);\n",
        "  assign link_ev_w = link_q_r && !link_up_i;\n")]),
    # round 3: the link branch now serves every sink; the arm keeps it from the unbound ones
    "unarmed-link-flush-dropped": (LS, [(
        "        if (link_ev_w) begin\n          // issue #212: LINK_DOWN (Flush!) and LINK_UP (Begin!) take the\n",
        "        if (link_ev_w && armed_r[s]) begin\n          // issue #212: LINK_DOWN (Flush!) and LINK_UP (Begin!) take the\n")]),
    # ---- round 3 (issue #212): R769-2 F1 = R770-2 F1, option (a): a settled sink's
    # registrar takes LINK_DOWN (Flush!) and LINK_UP (Begin!) too
    # round 2's exception back: no link input for a settled sink's registrar
    "settled-link-flush-dropped": (LS, [(
        "        if (link_ev_w) begin\n          // issue #212: LINK_DOWN (Flush!) and LINK_UP (Begin!) take the\n",
        "        if (link_ev_w && !armed_r[s]) begin\n          // issue #212: LINK_DOWN (Flush!) and LINK_UP (Begin!) take the\n"), (
        "                    || (link_ev_w && (reg_r[s] != R_MT_C));\n",
        "                    || (link_ev_w && !armed_r[s] && (reg_r[s] != R_MT_C));\n"), (
        "                  && !link_ev_w\n",
        "                  && !(link_ev_w && !armed_r[s])\n")]),
    # the withdrawal at the link change not published (no EVT_TK_UNREGISTERED)
    "settled-link-unpublished": (LS, [(
        "          evt_tk_unregistered_o[s] <= (reg_r[s] != R_MT_C);\n",
        "          evt_tk_unregistered_o[s] <= 1'b0;\n")]),
    # the declaration not withdrawn at the link change
    "link-withdraw-dropped": (LS, [(
        "                        && !(reg_rx_hit_w[s] && rx_registering_w))\n"
        "                    || (link_ev_w && (reg_r[s] != R_MT_C));\n",
        "                        && !(reg_rx_hit_w[s] && rx_registering_w));\n")]),
    # a decoder value on the link's own clock requests a declaration
    "link-clock-indicates": (LS, [(
        "                  && !link_ev_w\n",
        "")]),
    # the leave slot of an LV registrar left armed at the link change
    "settled-link-keeps-lv-slot": (LS, [(
        "          if (reg_r[s] == R_LV_C) tpend_r[s] <= T_CANCEL_C;\n"
        "          reg_r[s] <= R_MT_C;\n"
        "          evt_tk_unregistered_o[s] <= (reg_r[s] != R_MT_C);\n",
        "          reg_r[s] <= R_MT_C;\n"
        "          evt_tk_unregistered_o[s] <= (reg_r[s] != R_MT_C);\n")]),
    # ---- arms before issue #212 whose listener context the link branch moved: the same
    # mutation; r-sink-receive-priority-lost's first branch is now the link change's else
    "r-sink-receive-priority-lost": (LS, [(
        "        end else if (reg_rx_hit_w[s] && rx_registering_w) begin\n",
        "        end else if (leaveall_any_w[s] && (reg_r[s] == R_IN_C)) begin\n"
        "          reg_r[s] <= R_LV_C; tpend_r[s] <= T_ARM_C;\n"
        "        end else if (reg_rx_hit_w[s] && rx_registering_w) begin\n")]),
    # the 13-bit leave deadline: a sign-bit compare on 13 bits, and an
    # absolute deadline rebuilt without now_ms_i's upper bits
    "pt-expiry-sign-bit": (LS, [(
        "      pt_exp_w[e] = (pt_reg_r[e] == R_LV_C) && (pt_age_w[e] <= PT_SLACK_C);\n",
        "      pt_exp_w[e] = (pt_reg_r[e] == R_LV_C) && !pt_age_w[e][PT_DW_C-1];\n")]),
    "seed-deadline-rebuild-drops-now": (LS, [(
        "        sdl_ms_r <= now_ms_i + 32'(seed_rem_w);   // the entry's deadline, absolute\n",
        "        sdl_ms_r <= 32'(seed_dl_w);   // the entry's deadline, absolute\n")]),
    "top-listener-link-unwired": (TOP, [(
        "      .link_up_i               (link_up_i),\n",
        "      .link_up_i               (1'b1),\n")]),
}


def main() -> int:
    repo = Path(sys.argv[1])
    labels = sys.argv[2:] or list(ARMS)
    out = repo / "tb" / "srp_top" / "mutations"
    for label in labels:
        rel, edits = ARMS[label]
        src = (repo / rel).read_text()
        text = src
        for old, new in edits:
            assert text.count(old) == 1, (label, old, text.count(old))
            text = text.replace(old, new)
        diff = difflib.unified_diff(src.splitlines(True), text.splitlines(True),
                                    fromfile="a/" + rel, tofile="b/" + rel, n=3)
        (out / (label + ".patch")).write_text("".join(diff))
        print("wrote", label)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
