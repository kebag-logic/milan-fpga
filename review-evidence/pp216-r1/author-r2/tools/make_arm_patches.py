#!/usr/bin/env python3
"""make_arm_patches.py <tree> [arm...]: write tb/srp_top/mutations/<arm>.patch for each arm below (all, or the
named ones), each a list of exact text replacements in the processor tree, as three-line-context unified diffs (one
per file, in the order the files first appear). Refuses an edit whose old text does not occur exactly once in the
file as the earlier edits of the arm left it.

Round 2 of issue #216: the arms re-expressed because the lines around the code they edit changed (same name, same
intent, same rows in tb/srp_top/mutants.py), the arms of the VID link change, and the three Table 10-3 VP rows.
"""
import difflib
import sys
from pathlib import Path

PKG = "hdl/srp/srp_pkg.sv"
VLAN = "hdl/srp/KL_srp_vlan.sv"
TOP = "hdl/srp/KL_srp_top.sv"

RLA = ("      if (leaveall_tick_i || (walk_start_w && (txp_la_r || tx_la_i)))\n"
       "        reg_nx_w[i] = 1'b0;                               // rLA! / txLA!: IN -> LV\n")
RLV = ("      if (rx_hit_w[i] && (rx_ev_i == SRP_EV_LV))\n"
       "        reg_nx_w[i] = 1'b0;                               // rLv!: IN -> LV\n")
LINK = ("      if (link_ev_w)\n"
        "        reg_nx_w[i] = 1'b0;                               // Flush! / Begin!: MT\n")
BEGIN = ("      if (link_rise_w)                                    // Begin! (VO), then New! (VN)\n"
         "        app_ev_w[i] = active_r[i] ? SRP_AP_VN_C : SRP_AP_VO_C;\n")
ONE = "      app_nx_w[i] = (one_v_w && (one_ix_w == IDX_W_C'(i))) ? one_nx_w : app_ev_w[i];\n"
PUSH = ("          if (link_rise_w) begin\n"
        "            st_r <= W_EVAL;\n"
        "          end else if (vlan_ev_ready_i) begin\n")

ARMS = {
    # ---- re-expressed: the lines around the edit moved (the VID link change)
    "join-sent-at-handover": [
        (VLAN, "            if (ev_decl_r) queued_r[widx_r] <= 1'b1;   // its declaration handed over\n",
               "            if (ev_decl_r) sent_r[widx_r] <= 1'b1;   // its declaration handed over\n")],
    "vlan-registrar-never-in": [
        (VLAN, "        reg_nx_w[i] = 1'b1;                               // rNew / rJoinIn / rJoinMt\n",
               "        reg_nx_w[i] = reg_nx_w[i];                        // rNew / rJoinIn / rJoinMt\n")],
    "vlan-rlv-ignored": [(VLAN, RLV, "")],
    # the LeaveAll of a clock wins over its received value: the aging after the receive rows
    "vlan-rx-loses-to-leaveall": [(VLAN, RLA, ""), (VLAN, RLV, RLV + RLA)],
    # ---- the VID link change (issue #216 round 2)
    # the VID Registrar keeps its state across LINK_DOWN and LINK_UP
    "vlan-link-keeps-registrar": [(VLAN, LINK, "")],
    # LINK_UP is no Begin! on the VID Applicants: they keep their state
    "vlan-link-no-begin": [(VLAN, BEGIN, "")],
    # a received value on the link change's clock registers: the link change before the receive rows
    "vlan-link-rx-wins": [(VLAN, LINK, ""), (VLAN, RLA, LINK + RLA)],
    # a VID with no user keeps its state at LINK_UP: its owed Lv still goes out
    "vlan-link-keeps-leaving": [
        (VLAN, "        app_ev_w[i] = active_r[i] ? SRP_AP_VN_C : SRP_AP_VO_C;\n",
               "        app_ev_w[i] = active_r[i] ? SRP_AP_VN_C : app_ev_w[i];\n")],
    # the walk pushes the message it held across LINK_UP
    "vlan-link-push-kept": [
        (VLAN, PUSH, "          if (vlan_ev_ready_i) begin\n"),
        (VLAN, "  assign vlan_ev_valid_o = (st_r == W_PUSH) && !link_rise_w;\n",
               "  assign vlan_ev_valid_o = (st_r == W_PUSH);\n")],
    # Begin! after the clock's tx!: the walk's message on the LINK_UP clock is the old state's
    "vlan-link-after-tx": [
        (VLAN, BEGIN, ""),
        (VLAN, ONE, "      app_nx_w[i] = link_rise_w ? (active_r[i] ? SRP_AP_VN_C : SRP_AP_VO_C)\n"
                    "                  : (one_v_w && (one_ix_w == IDX_W_C'(i))) ? one_nx_w : app_ev_w[i];\n")],
    # KL_srp_top leaves the VID participant's link input tied up
    "top-vlan-link-unwired": [
        (TOP, "      .link_up_i       (link_up_i),\n", "      .link_up_i       (1'b1),\n")],
    # ---- Table 10-3 VP against AP (the shared Applicant rows)
    # note 4 inverted: rJoinIn! in VP goes AP with operPointToPointMAC TRUE
    "vp-rjoinin-ignores-note4": [
        (PKG, "          SRP_AP_VP_C: nx = p2p ? st : SRP_AP_AP_C;   // note 4\n",
              "          SRP_AP_VP_C: nx = p2p ? SRP_AP_AP_C : st;   // note 4\n")],
    # txLA! from VP stays VP instead of AA
    "vp-txla-stays-vp": [
        (PKG, "          SRP_AP_VO_C, SRP_AP_LA_C, SRP_AP_AO_C, SRP_AP_QO_C: nx = SRP_AP_LO_C;\n"
              "          SRP_AP_VP_C: nx = SRP_AP_AA_C;\n",
              "          SRP_AP_VO_C, SRP_AP_LA_C, SRP_AP_AO_C, SRP_AP_QO_C: nx = SRP_AP_LO_C;\n"
              "          SRP_AP_VP_C: nx = SRP_AP_VP_C;\n")],
    # txLA! from VP sends sJ instead of s
    "vp-txla-sends-sj": [
        (PKG, "        SRP_AP_VP_C:                          m = {1'b1, s};\n",
              "        SRP_AP_VP_C:                          m = {1'b1, sj};\n")],
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
