#!/usr/bin/env python3
"""Reviewer probe arms: exact one-occurrence textual replacements on a disposable copy."""
import sys, pathlib
ARMS = {
 "p1-note8-ignored": ("hdl/srp/srp_pkg.sv",
   "SRP_AP_AN_C: nx = reg_in ? SRP_AP_QA_C : SRP_AP_AA_C;   // note 8",
   "SRP_AP_AN_C: nx = SRP_AP_QA_C;   // note 8"),
 "p2-mvrp-la-only-when-declaring": ("hdl/srp/KL_srp_top.sv",
   "        p_tx_mvrp_la_r   <= la_mvrp_pend_r && !dec_la_mvrp_w;\n        mla_r            <= la_mvrp_pend_r && !dec_la_mvrp_w;",
   "        p_tx_mvrp_la_r   <= la_mvrp_pend_r && !dec_la_mvrp_w && (|dbg_vid_active_o);\n        mla_r            <= la_mvrp_pend_r && !dec_la_mvrp_w && (|dbg_vid_active_o);"),
 "p3-domain-periodic-ignored": ("hdl/srp/KL_srp_domain.sv",
   "app_per_w = (periodic_tick_i && declared_r)",
   "app_per_w = (1'b0 && periodic_tick_i && declared_r)"),
 "p4-vlan-periodic-ignored": ("hdl/srp/KL_srp_vlan.sv",
   "if (periodic_tick_i && alloc_r[i])",
   "if (1'b0 && periodic_tick_i && alloc_r[i])"),
 "p5-mvrp-leaveall-not-restarted": ("hdl/srp/KL_srp_top.sv",
   "              la_mvrp_pend_r <= 1'b1;  // Active: sLA at the next MVRP tx!\n              need_draw_r[1] <= 1'b1;",
   "              la_mvrp_pend_r <= 1'b1;  // Active: sLA at the next MVRP tx!"),
}
root, arm = pathlib.Path(sys.argv[1]), sys.argv[2]
f, old, new = ARMS[arm]
p = root / f
s = p.read_text()
assert s.count(old) == 1, (arm, s.count(old))
p.write_text(s.replace(old, new))
print("applied", arm)
