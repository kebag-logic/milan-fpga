#!/usr/bin/env python3
"""mkpatch.py <repo>: cut the issue #212 arms of tb/srp_top/mutations from one exact edit each.

Each arm replaces one unique text of hdl/srp/KL_srp_listener_fsm.sv; the patch is
`diff -u` of the file before and after, with the a/ b/ prefixes git apply takes.
"""
import difflib
import sys
from pathlib import Path

REL = "hdl/srp/KL_srp_listener_fsm.sv"

ARMS = {
    "pt-seed-dropped": [(
        "    seed_v_w = ctl_valid_i && !evt_valid_i && ctl_settle_i\n",
        "    seed_v_w = 1'b0 && ctl_valid_i && !evt_valid_i && ctl_settle_i\n")],
    "pt-never-holds": [(
        "      pt_alloc_w[e] = pt_rx_w && rx_registering_w && (pt_hit_w == '0)\n",
        "      pt_alloc_w[e] = 1'b0 && pt_rx_w && rx_registering_w && (pt_hit_w == '0)\n")],
    "seed-type-advertise": [(
        "        seed_type_w  = seed_type_w  | pt_type_r[e];\n",
        "        seed_type_w  = seed_type_w;\n")],
    "seed-drops-failure-information": [(
        "        seed_fcode_w = seed_fcode_w | pt_fcode_r[e];\n        seed_fsys_w  = seed_fsys_w  | pt_fsys_r[e];\n",
        "        seed_fcode_w = seed_fcode_w;\n        seed_fsys_w  = seed_fsys_w;\n")],
    "seed-no-registered-strobe": [(
        "            evt_tk_registered_o[s]   <= 1'b1;\n",
        "            evt_tk_registered_o[s]   <= 1'b0;\n")],
    "park-retire-declares-next-walk": [(
        "          if (pk_decl_w) begin\n",
        "          if (1'b0 && pk_decl_w) begin\n")],
    "pt-rlv-ignored": [(
        "        if (pt_reg_r[e] == R_IN_C) pt_nreg_w[e] = R_MT_C;   // Δ13; LV: -x-\n",
        "        if (1'b0) pt_nreg_w[e] = R_MT_C;   // Δ13; LV: -x-\n")],
    "pt-leavetimer-never-expires": [(
        "      pt_exp_w[e] = (pt_reg_r[e] == R_LV_C) && !pt_age_w[e][31];\n",
        "      pt_exp_w[e] = 1'b0;\n")],
    "pt-leaveall-ignored": [(
        "      pt_la_w[e]  = leaveall_own_i\n"
        "                 || (pt_type_r[e] ? leaveall_rx_i[SRP_LA_TALKER_FAILED_C]\n"
        "                                  : leaveall_rx_i[SRP_LA_TALKER_ADV_C]);\n",
        "      pt_la_w[e]  = 1'b0;\n")],
    "pt-leaveall-any-lane": [(
        "                 || (pt_type_r[e] ? leaveall_rx_i[SRP_LA_TALKER_FAILED_C]\n"
        "                                  : leaveall_rx_i[SRP_LA_TALKER_ADV_C]);\n",
        "                 || (|leaveall_rx_i);\n")],
    "seed-lv-fresh-deadline": [(
        "        sdl_ms_r <= seed_dl_w;\n",
        "        sdl_ms_r <= now_ms_i + LEAVE_MS_P;\n")],
    "seed-from-current-state": [(
        "        seed_reg_w   = seed_reg_w   | pt_nreg_w[e];\n",
        "        seed_reg_w   = seed_reg_w   | pt_reg_r[e];\n"), (
        "        seed_dl_w    = seed_dl_w    | pt_ndl_w[e];\n",
        "        seed_dl_w    = seed_dl_w    | pt_dl_r[e];\n")],
    "pt-match-ignores-da": [(
        "                 && (pt_sid_r[e] == pt_qsid_w) && (pt_da_r[e] == pt_qda_w)\n",
        "                 && (pt_sid_r[e] == pt_qsid_w)\n")],
    "pt-vid-high-bits-ignored": [(
        "    pt_rx_w = evt_valid_i && evt_msrp_i && (evt_vid_i[15:12] == 4'd0)\n",
        "    pt_rx_w = evt_valid_i && evt_msrp_i\n")],
    "pt-allocation-overwrites-entry-0": [(
        "                   && (pt_reg_r[e] == R_MT_C) && !pt_taken_w;\n",
        "                   && ((pt_reg_r[e] == R_MT_C) || (e == 0)) && !pt_taken_w;\n")],
    "park-retire-ignores-group": [(
        "        pk_alone_w = 1'b0;\n",
        "        pk_alone_w = 1'b1;\n")],
    "park-retire-without-hold": [(
        "      pk_hold_w[s] = lvp_r[s] && (decl_pend_r[s] == D_DECLARE_C)\n",
        "      pk_hold_w[s] = 1'b0 && lvp_r[s] && (decl_pend_r[s] == D_DECLARE_C)\n")],
    "seed-keeps-expiry-strobe": [(
        "            evt_tk_unregistered_o[s] <= 1'b0;\n",
        "")],
    # re-cut (issue #212 moved its trailing context): the same plant
    "listener-retire-skips-group-mark": [(
        "              if (same_w[wsrc_r][t]) wdone_r[t] <= 1'b1;\n",
        "              if (t == 32'(wsrc_r)) wdone_r[t] <= 1'b1;\n")],
    "seed-lv-unguarded": [(
        "            if (seed_reg_w == R_LV_C) tpend_r[s] <= T_ARM_C;\n",
        "")],
}


def main() -> int:
    repo = Path(sys.argv[1])
    src = (repo / REL).read_text()
    out = repo / "tb" / "srp_top" / "mutations"
    for label, edits in ARMS.items():
        text = src
        for old, new in edits:
            assert text.count(old) == 1, (label, old)
            text = text.replace(old, new)
        diff = difflib.unified_diff(src.splitlines(True), text.splitlines(True),
                                    fromfile="a/" + REL, tofile="b/" + REL, n=3)
        (out / (label + ".patch")).write_text("".join(diff))
        print("wrote", label)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
