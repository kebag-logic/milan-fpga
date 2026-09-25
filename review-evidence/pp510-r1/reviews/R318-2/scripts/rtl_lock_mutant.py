#!/usr/bin/env python3
"""Disposable RTL fault probe (never committed). Copy <base> to <dst> (no .git,
no build dirs) and make the waived MVU SETs (command_type 0x0001 and 0x0003,
full MVU protocol_id match) lock-checked: when the ENTITY lock is held by a
controller other than the command's, re-dispatch to the existing E_LOCKED1
ENTITY_LOCKED refusal instead of the NOT_IMPLEMENTED echo. Everything else is
unchanged, so only a test that sends a waived SET under another controller's
lock can see it. 06 section 6.8 claims these SETs take the unsupported-command
path without a lock check; tb/pp_top M4L is the response-level pin for that
claim and should reject this mutant. Prints the unified diff."""
import difflib, shutil, sys, pathlib
base, dst = sys.argv[1:3]
d = pathlib.Path(dst)
if d.exists():
    shutil.rmtree(d)
shutil.copytree(base, dst, ignore=shutil.ignore_patterns('.git', 'obj_dir', 'obj_vid'))
f = d / 'hdl/aecp/KL_aecp_engine.sv'
src = f.read_text()
anchor = ("            if (mvu_get_milan_info_w) begin\n"
          "              upc_r  <= UPC_MVUINFO_C;\n"
          "              echo_r <= 1'b0;\n"
          "            end\n")
assert src.count(anchor) == 1, 'anchor not unique'
new = anchor + (
    "            if ((cmd_r.protocol == PP_PROTO_MVU) && (pld_cmd_r >= MVU_CMD_PLD_C)\n"
    "                && (raw_ct_r == MVU_PID_HI_C) && (cfg_ix_r == MVU_PID_MD_C)\n"
    "                && (pid_lo_r == 2'b11)\n"
    "                && ((desc_ty_r == 16'h0001) || (desc_ty_r == 16'h0003))\n"
    "                && lock_held_i && (lock_ctlr_i != cmd_r.controller_eid)) begin\n"
    "              upc_r  <= UPC_LOCKED1_C;  // R318 probe: lock-checked waived SET\n"
    "              echo_r <= 1'b0;\n"
    "            end\n")
out = src.replace(anchor, new)
f.write_text(out)
sys.stdout.writelines(difflib.unified_diff(src.splitlines(True), out.splitlines(True),
                                           'a/hdl/aecp/KL_aecp_engine.sv', 'b/hdl/aecp/KL_aecp_engine.sv'))
