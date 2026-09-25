#!/usr/bin/env python3
"""Make a disposable copy of <base> at <dst> (no .git, no build dirs) and apply
one named mutation to hdl/aecp/KL_aecp_engine.sv. Prints the unified diff."""
import difflib, shutil, sys, pathlib
base, dst, name = map(str, sys.argv[1:4])
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
if name == 'waived-success-echo':
    # MVU 0x0001..0x0004 only: keep the echo, jump to an existing
    # SET_STATUS SUCCESS / BUILD_HDR / SEND_RESP / END sequence (ROM word 135)
    new = anchor + (
        "            if ((cmd_r.protocol == PP_PROTO_MVU) && (pld_cmd_r >= MVU_CMD_PLD_C)\n"
        "                && (raw_ct_r == MVU_PID_HI_C) && (cfg_ix_r == MVU_PID_MD_C)\n"
        "                && (pid_lo_r == 2'b11) && (desc_ty_r >= 16'h0001)\n"
        "                && (desc_ty_r <= 16'h0004))\n"
        "              upc_r <= 11'd135;  // R318 probe\n")
    out = src.replace(anchor, new)
elif name == 'any-type-milan-info':
    old = "                                && (desc_ty_r  == MVU_GET_MILAN_INFO_C);"
    assert src.count(old) == 1
    out = src.replace(old, "                                && (desc_ty_r[14:3] == 12'd0);  // R318 probe: 0x0000..0x0007 all get Figure 5.4")
else:
    sys.exit('unknown mutation ' + name)
f.write_text(out)
sys.stdout.writelines(difflib.unified_diff(src.splitlines(True), out.splitlines(True),
                                           'a/hdl/aecp/KL_aecp_engine.sv', 'b/hdl/aecp/KL_aecp_engine.sv'))
