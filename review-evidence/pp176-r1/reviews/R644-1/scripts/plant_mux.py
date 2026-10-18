#!/usr/bin/env python3
"""Plant runtime-selectable mutants (+MUT=<n>) into a scratch copy of
hdl/aecp/KL_aecp_engine.sv at head 29f58ad3. MUT=0 (or no plusarg) is the
unmodified behaviour. Each anchor must match exactly once, or the script
refuses. Usage: plant_mux.py <tree-root>

 1  author M38: the 2013 body refused again (!si13_w -> 1)
 2  author M39: the answer keeps the command's length
 3  author M40: si13_pad_w tied 0 (bytes past @69 echo the slot)
 4  author M41: SI13_ECHO_C 46 -> 48 (reserved word echoed into ip_flags)
 5  author M42: si13_w compares >= (any longer-than-48 short body is 2013)
 6  author M43: 2013 latency never captured
 7  author M44: flag gate forced open
 8  reviewer: the 2013 zero-pad applied to every SET_STREAM_INFO echo
 9  reviewer: every SET_STREAM_INFO echo lengthened/clamped to 84 bytes
10  reviewer: si13_w without its cdl conjunct
11  reviewer: si13_w without its walked-length conjunct
12  reviewer: SI13_ECHO_C 46 -> 44 (stream_vlan_id zeroed)
13  reviewer: si13_w matches cdl 59 instead of 60
14  reviewer: si13_w matches cdl 61 instead of 60 (with pld 49)
15  reviewer: 2013 body skips the streaming refusal
16  reviewer: 2013 body skips the bit-31 BAD_ARGUMENTS route
17  reviewer: 2013 body skips the Stream Input NOT_SUPPORTED route
"""
import pathlib
import sys

EDITS = [
    # the selector
    ("  logic si13_w;\n",
     "  int unsigned rv_mut;\n"
     "  initial begin\n"
     "    if (!$value$plusargs(\"MUT=%d\", rv_mut)) rv_mut = 0;\n"
     "  end\n"
     "  logic si13_w;\n"),
    ("  assign si13_w = ssinfo_r && (cmd_r.cdl == SI13_CDL_C)\n"
     "                  && (pld_cmd_r == SI13_PLD_C);\n",
     "  assign si13_w = ssinfo_r && (\n"
     "      (rv_mut == 5)  ? ((cmd_r.cdl >= SI13_CDL_C) && (pld_cmd_r >= SI13_PLD_C)) :\n"
     "      (rv_mut == 10) ? (pld_cmd_r == SI13_PLD_C) :\n"
     "      (rv_mut == 11) ? (cmd_r.cdl == SI13_CDL_C) :\n"
     "      (rv_mut == 13) ? ((cmd_r.cdl == 11'd59) && (pld_cmd_r == 11'd47)) :\n"
     "      (rv_mut == 14) ? ((cmd_r.cdl == 11'd61) && (pld_cmd_r == 11'd49)) :\n"
     "      ((cmd_r.cdl == SI13_CDL_C) && (pld_cmd_r == SI13_PLD_C)));\n"),
    ("  assign si13_pad_w = si13_w\n"
     "                      && (bidx_r >= (11'(FRAME_HDR_C) + SI13_ECHO_C));\n",
     "  assign si13_pad_w = (rv_mut == 3) ? 1'b0 :\n"
     "                      ((rv_mut == 8) ? ssinfo_r : si13_w)\n"
     "                      && (bidx_r >= (11'(FRAME_HDR_C)\n"
     "                          + ((rv_mut == 4) ? 11'd48 : (rv_mut == 12) ? 11'd44\n"
     "                             : SI13_ECHO_C)));\n"),
    ("              if (!si13_w\n"
     "                  && ((cmd_r.cdl < 11'd96)\n",
     "              if (((rv_mut == 1) ? 1'b1 : !si13_w)\n"
     "                  && ((cmd_r.cdl < 11'd96)\n"),
    ("              else if (cfg_ix_r != DT_STREAM_OUTPUT_C)\n"
     "                                                      upc_r <= UPC_NSUPPE_C;\n"
     "              //! §5.4.2.9's own SHALL",
     "              else if ((cfg_ix_r != DT_STREAM_OUTPUT_C)\n"
     "                       && !((rv_mut == 17) && si13_w))\n"
     "                                                      upc_r <= UPC_NSUPPE_C;\n"
     "              //! §5.4.2.9's own SHALL"),
    ("              else if (run_this_w)                    upc_r <= UPC_SIRUN_C;\n"
     "              else if (setval_r[63:32] != SIF_ACC_LAT_C)\n",
     "              else if (run_this_w && !((rv_mut == 15) && si13_w))\n"
     "                                                      upc_r <= UPC_SIRUN_C;\n"
     "              else if ((rv_mut != 7) && (setval_r[63:32] != SIF_ACC_LAT_C))\n"),
    ("              else if (silat_r[31])                   upc_r <= UPC_BADARG_C;\n"
     "              else                                    upc_r <= UPC_SINFO_C;\n",
     "              else if (silat_r[31] && !((rv_mut == 16) && si13_w))\n"
     "                                                      upc_r <= UPC_BADARG_C;\n"
     "              else                                    upc_r <= UPC_SINFO_C;\n"),
    ("              11'd26: if (ssinfo_r) silat_r[31:24] <= rxs_rd_data_i;\n"
     "              11'd27: if (ssinfo_r) silat_r[23:16] <= rxs_rd_data_i;\n"
     "              11'd28: if (ssinfo_r) silat_r[15:8]  <= rxs_rd_data_i;\n"
     "              11'd29: if (ssinfo_r) silat_r[7:0]   <= rxs_rd_data_i;\n",
     "              11'd26: if (ssinfo_r && !((rv_mut == 6) && si13_w)) silat_r[31:24] <= rxs_rd_data_i;\n"
     "              11'd27: if (ssinfo_r && !((rv_mut == 6) && si13_w)) silat_r[23:16] <= rxs_rd_data_i;\n"
     "              11'd28: if (ssinfo_r && !((rv_mut == 6) && si13_w)) silat_r[15:8]  <= rxs_rd_data_i;\n"
     "              11'd29: if (ssinfo_r && !((rv_mut == 6) && si13_w)) silat_r[7:0]   <= rxs_rd_data_i;\n"),
    ("                pld_r <= si13_w ? SI21_PLD_C : pld_cmd_r;\n",
     "                pld_r <= (rv_mut == 2) ? pld_cmd_r\n"
     "                         : (rv_mut == 9) ? (ssinfo_r ? SI21_PLD_C : pld_cmd_r)\n"
     "                         : (si13_w ? SI21_PLD_C : pld_cmd_r);\n"),
]


def main() -> int:
    path = pathlib.Path(sys.argv[1]) / "hdl/aecp/KL_aecp_engine.sv"
    text = path.read_text(encoding="utf-8")
    for old, new in EDITS:
        n = text.count(old)
        if n != 1:
            print(f"REFUSE: anchor matched {n} times:\n{old}", file=sys.stderr)
            return 2
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")
    print(f"planted {len(EDITS)} edits into {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
