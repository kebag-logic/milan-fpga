#!/usr/bin/env python3
"""Write each mutation patch as one exact textual edit of the head RTL.

usage: make_patches.py <processor tree>   (writes tb/srp_top/mutations/<label>.patch)
"""
import difflib, sys
from pathlib import Path

tree = Path(sys.argv[1])
rel = "hdl/srp/KL_srp_listener_fsm.sv"
src = (tree / rel).read_text()

EDITS = {
  # re-anchored issue #188 arms, the same edits on the new context
  "listener-declaration-not-held": (
    "      decl_grant_w[s] = (decl_pend_r[s] != D_NOP_C) && !lvp_r[s]\n",
    "      decl_grant_w[s] = (decl_pend_r[s] != D_NOP_C)\n"),
  "listener-lo-not-owed": (
    "    set_owes_w = (set_lv_w inside {A_LA_C, A_LO_C}) && !hand_w;\n",
    "    set_owes_w = (set_lv_w == A_LA_C) && !hand_w;\n"),
  "listener-lost-txla": (
    "            wtxla_r      <= laown_pend_r || leaveall_own_i;\n",
    "            wtxla_r      <= laown_pend_r;\n"),
  "listener-park-never-retires": (
    "              && !(wnext_w inside {A_LA_C, A_LO_C})) begin\n"
    "            lvp_r[wsrc_r]      <= 1'b0;\n",
    "              && !(wnext_w inside {A_LA_C, A_LO_C})) begin\n"),
  "listener-park-retires-on-txla": (
    "          if (walk_tx_w && lvp_r[wsrc_r]\n"
    "              && !(wnext_w inside {A_LA_C, A_LO_C})) begin\n",
    "          if (walk_tx_w && lvp_r[wsrc_r]) begin\n"),
  "listener-rebind-abandons-leave": (
    "    set_app_w  = set_owes_w ? set_lv_w : A_VO_C;\n",
    "    set_app_w  = (set_owes_w && set_same_w) ? set_lv_w : A_VO_C;\n"),
  "listener-reprobe-abandons-leave": (
    "    set_app_w  = set_owes_w ? set_lv_w : A_VO_C;\n",
    "    set_app_w  = (set_owes_w && !set_same_w) ? set_lv_w : A_VO_C;\n"),
  "listener-reprobe-parks-own-stream": (
    "    set_same_w = rec_valid_r[ctl_sink_i] && (csid_w == ctl_stream_id_i);\n",
    "    set_same_w = 1'b0;\n"),
  "listener-unrecorded-applicant-owes": (
    "    set_lv_w   = rec_valid_r[ctl_sink_i]\n"
    "               ? app_next_f(app_r[ctl_sink_i], AE_LV_C, 1'b0, p2p_i) : A_VO_C;\n",
    "    set_lv_w   = app_next_f(app_r[ctl_sink_i], AE_LV_C, 1'b0, p2p_i);\n"),
  # issue #193: one declaring applicant per stream_id
  "listener-settle-compare-dropped": (
    "      cset_w[s] = (ctl_stream_id_i == sid_r[s]);\n",
    "      cset_w[s] = 1'b0;\n"),
  "listener-teardown-applies-lv": (
    "        // nothing here: the group's Lv! or handover follows (owner_map)\n",
    "        // nothing here: the group's Lv! or handover follows (owner_map)\n"
    "        app_ev_v_w[s] = !ctl_settle_i;\n"
    "        app_ev_w[s]   = AE_LV_C;\n"),
  "listener-withdraw-ignores-riders": (
    "          anyo_w[s] = anyo_w[s] | dcl_w[t];\n",
    "          anyo_w[s] = dcl_w[s];\n"),
  "listener-teardown-keeps-declaring": (
    "        // over, from the next cycle (owner_map)\n"
    "        dcl_r[ctl_sink_i] <= 2'd0;\n",
    "        // over, from the next cycle (owner_map)\n"),
  "listener-group-order-reversed": (
    "          if (t < s) begin\n"
    "            lo_dcl_w[s] = lo_dcl_w[s] | dcl_w[t];\n",
    "          if (t > s) begin\n"
    "            lo_dcl_w[s] = lo_dcl_w[s] | dcl_w[t];\n"),
  "listener-rider-settle-hands-over": (
    "    hand_w = ctl_acc_w && ctl_settle_i && nvo_w[ctl_sink_i] && (hoth_w != '0);\n",
    "    hand_w = ctl_acc_w && ctl_settle_i && (hoth_w != '0);\n"),
  "listener-settle-parks-shared-stream": (
    "    hand_w = ctl_acc_w && ctl_settle_i && nvo_w[ctl_sink_i] && (hoth_w != '0);\n",
    "    hand_w = 1'b0;\n"),
  "listener-group-op-during-settle": (
    "      end else if (op_w[s] && !ctl_acc_w) begin\n",
    "      end else if (op_w[s]) begin\n"),
  "listener-type-not-combined": (
    "          cfp_w[s] = cfp_w[s] | dcl_r[t];\n",
    "          cfp_w[s] = (dcl_r[t] != 2'd0) ? dcl_r[t] : cfp_w[s];\n"),
  "listener-handover-drops-state": (
    "                         : app_r[take_src_w[t]];\n",
    "                         : A_VO_C;\n"),
  "listener-rider-not-quiet": (
    "      quiet_w[s] = mbr_w[s] && !act_w[s];\n",
    "      quiet_w[s] = 1'b0;\n"),
  "listener-handover-forgets-walk-mark": (
    "          wdone_r[t]    <= (walk_r != W_IDLE) && wdone_r[take_src_w[t]];\n",
    "          wdone_r[t]    <= 1'b0;\n"),
}

out = tree / "tb" / "srp_top" / "mutations"
for label, (old, new) in EDITS.items():
    if src.count(old) != 1:
        sys.exit(f"{label}: the edit's anchor occurs {src.count(old)} times")
    mutated = src.replace(old, new)
    diff = difflib.unified_diff(src.splitlines(keepends=True),
                                mutated.splitlines(keepends=True),
                                fromfile="a/" + rel, tofile="b/" + rel, n=3)
    (out / f"{label}.patch").write_text("".join(diff))
    print("wrote", label)
