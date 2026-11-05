#!/usr/bin/env python3
"""dl13.py <tree>: the port registrars' leave deadline in PT_DW_C = $clog2(LEAVE_MS_P + 1) bits
(13 at 5000 ms) instead of 32, the seeded arm's absolute deadline rebuilt from the remaining time.

One exact text edit per site of hdl/srp/KL_srp_listener_fsm.sv; refuses drift.
"""
import sys
from pathlib import Path

EDITS = [
    ("  logic [PT_N_C-1:0][31:0]     pt_dl_r;     // leavetimer deadline (absolute ms)\n",
     "  // leavetimer deadline (issue #212): the low PT_DW_C bits of the\n"
     "  // absolute ms, enough for T-MRP-LEAVE (13 at 5000 ms)\n"
     "  localparam int unsigned PT_DW_C = $clog2(LEAVE_MS_P + 1);\n"
     "  localparam logic [PT_DW_C-1:0] PT_SLACK_C = PT_DW_C'((2 ** PT_DW_C) - 1 - LEAVE_MS_P);\n"
     "  logic [PT_N_C-1:0][PT_DW_C-1:0] pt_dl_r;\n"),
    ("  logic [PT_N_C-1:0][31:0] pt_ndl_w;\n  logic [PT_N_C-1:0][31:0] pt_age_w;\n",
     "  logic [PT_N_C-1:0][PT_DW_C-1:0] pt_ndl_w;\n  logic [PT_N_C-1:0][PT_DW_C-1:0] pt_age_w;\n"),
    ("      // wrap-safe, as KL_pp_timer_service: expired once the modular age\n"
     "      // (now - deadline) is not negative\n"
     "      pt_age_w[e] = now_ms_i - pt_dl_r[e];\n"
     "      pt_exp_w[e] = (pt_reg_r[e] == R_LV_C) && !pt_age_w[e][31];\n",
     "      // wrap-safe on PT_DW_C bits: an LV entry is compared on every clock\n"
     "      // and now_ms_i steps by one, so its modular age (now - deadline)\n"
     "      // runs from -T-MRP-LEAVE up to 0, its expiry, and is past it while\n"
     "      // it is at most PT_SLACK_C\n"
     "      pt_age_w[e] = now_ms_i[PT_DW_C-1:0] - pt_dl_r[e];\n"
     "      pt_exp_w[e] = (pt_reg_r[e] == R_LV_C) && (pt_age_w[e] <= PT_SLACK_C);\n"),
    ("        pt_ndl_w[e]  = now_ms_i + LEAVE_MS_P;\n",
     "        pt_ndl_w[e]  = now_ms_i[PT_DW_C-1:0] + PT_DW_C'(LEAVE_MS_P);\n"),
    ("  logic [31:0] seed_dl_w;\n",
     "  logic [PT_DW_C-1:0] seed_dl_w;\n  logic [PT_DW_C-1:0] seed_rem_w;   // its remaining ms\n"),
    ("    seed_dl_w    = 32'd0;\n",
     "    seed_dl_w    = '0;\n"),
    ("    seed_v_w = ctl_valid_i && !evt_valid_i && ctl_settle_i\n",
     "    seed_rem_w = seed_dl_w - now_ms_i[PT_DW_C-1:0];\n"
     "    seed_v_w = ctl_valid_i && !evt_valid_i && ctl_settle_i\n"),
    ("        sdl_ms_r <= seed_dl_w;\n",
     "        sdl_ms_r <= now_ms_i + 32'(seed_rem_w);\n"),
]


def main() -> int:
    p = Path(sys.argv[1]) / "hdl/srp/KL_srp_listener_fsm.sv"
    s = p.read_text()
    for old, new in EDITS:
        assert s.count(old) == 1, old
        s = s.replace(old, new)
    p.write_text(s)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
