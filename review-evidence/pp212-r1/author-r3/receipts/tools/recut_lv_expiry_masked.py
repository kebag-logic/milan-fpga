#!/usr/bin/env python3
"""recut_lv_expiry_masked.py <repo>: cut lv-expiry-masked again. Its talker section is kept verbatim (that
file is unchanged); its listener section is diff -u of the same three edits on the current listener."""
import difflib
import sys
from pathlib import Path

repo = Path(sys.argv[1])
patch = repo / "tb/srp_top/mutations/lv-expiry-masked.patch"
old = patch.read_text()
cut = old.index("--- a/hdl/srp/KL_srp_listener_fsm.sv\n")
talker = old[:cut]
assert talker.startswith("--- a/hdl/srp/KL_srp_talker_fsm.sv\n")
LS = "hdl/srp/KL_srp_listener_fsm.sv"
src = (repo / LS).read_text()
EXP = ("        end else if (exp_hit_w && (exp_idx_w == s)\n"
       "                     && (reg_r[s] == R_LV_C) && (tpend_r[s] != T_ARM_C)) begin\n"
       "          reg_r[s] <= R_MT_C;                // leavetimer! -> MT + Lv\n"
       "          evt_tk_unregistered_o[s] <= 1'b1;\n")
LA = ("        end else if (leaveall_any_w[s] && (reg_r[s] == R_IN_C)) begin\n"
      "          reg_r[s]   <= R_LV_C;\n"
      "          tpend_r[s] <= T_ARM_C;\n")
CMT = ("      // Table 10-4, expiry before reception: New/Join finish IN and cancel\n"
       "      // the obsolete timer (no published withdrawal); Lv/LA finish MT.\n"
       "      // Test expiry before rLv so its one-clock strobe cannot be masked.\n")
edits = [(CMT, ""), (EXP, ""), (LA, LA + EXP)]
text = src
for a, b in edits:
    assert text.count(a) == 1, a
    text = text.replace(a, b)
listener = "".join(difflib.unified_diff(src.splitlines(True), text.splitlines(True),
                                        fromfile="a/" + LS, tofile="b/" + LS, n=3))
patch.write_text(talker + listener)
print("wrote lv-expiry-masked")
