# R437-3 reviewer-planted defects in the owed READ's drain bound (B-series).
# Each is run by the suite under pristine and coincident completion at 100, 37
# and 20, and by the randomized harness at bounds 1, 3 and 37.
RPPUMP = "                 : (state_r == S_RPPUMP) ? (plen_r - bcnt_r)\n"
RHCOLL = "  assign left_w  = (state_r == S_RHCOLL) ? (HDR_LEN_C - 16'(hidx_r))\n"
REST = "                 : dev_len_o;\n"
DEC = "    else if (drain_w && dev_rvalid_i) owed_left_r <= owed_left_r - 16'd1;\n"
DRAIN = "  assign drain_w = owed_r && owed_rd_r && (owed_left_r != 16'd0);\n"
PROBES = {
    "base": [],
    # under-drain: a legal device's last owed byte is never taken
    "B1_rppump_one_short": [("RTL", RPPUMP, "                 : (state_r == S_RPPUMP) ? (plen_r - bcnt_r - 16'd1)\n")],
    "B2_rhcoll_one_short": [("RTL", RHCOLL, "  assign left_w  = (state_r == S_RHCOLL) ? (HDR_LEN_C - 16'(hidx_r) - 16'd1)\n")],
    "B3_request_one_short": [("RTL", REST, "                 : (dev_len_o != 16'd0) ? (dev_len_o - 16'd1) : 16'd0;\n")],
    "B4_request_none": [("RTL", REST, "                 : 16'd0;\n")],
    # over-drain: a babbling device's byte past the length taken as progress
    "B5_rppump_one_over": [("RTL", RPPUMP, "                 : (state_r == S_RPPUMP) ? (plen_r - bcnt_r + 16'd1)\n")],
    "B6_rhcoll_one_over": [("RTL", RHCOLL, "  assign left_w  = (state_r == S_RHCOLL) ? (HDR_LEN_C - 16'(hidx_r) + 16'd1)\n")],
    "B6b_rhcoll_whole": [("RTL", RHCOLL, "  assign left_w  = (state_r == S_RHCOLL) ? HDR_LEN_C\n")],
    "B7_request_one_over": [("RTL", REST, "                 : (dev_len_o != 16'd0) ? (dev_len_o + 16'd1) : 16'd0;\n")],
    "B8_wait_states_owe_eight": [("RTL", REST, "                 : ((state_r == S_RHWAIT) || (state_r == S_RPWAIT)) ? HDR_LEN_C : dev_len_o;\n")],
    # the count runs below zero and wraps, so the drain resumes
    "B9_decrement_unguarded": [("RTL", DEC, "    else if (owed_r && dev_rvalid_i)  owed_left_r <= owed_left_r - 16'd1;\n")],
    # the count eight bits wide
    "B10_count_eight_bits": [("RTL", "  logic       [15:0] owed_left_r;   // ...as many as it still owes",
                              "  logic        [7:0] owed_left_r;   // ...as many as it still owes")],
    # the drain no longer conditioned on the owed command being a READ
    "B12_drain_any_owed": [("RTL", DRAIN, "  assign drain_w = owed_r && (owed_left_r != 16'd0);\n")],
    # the count loaded at the late grant instead of at the deadline (stale for a late READ)
    "B13_load_only_owned": [("RTL", "    else if (dl_w && !owed_r)         owed_left_r <= left_w;",
                             "    else if (dl_w && !owed_r && dev_cmd_owned_w) owed_left_r <= left_w;")],
}
RUNS = []
for p in PROBES:
    for m in ("pristine", "coincident completion"):
        for t in (100, 37, 20):
            RUNS.append((p, m, t))
    for t in (1, 3, 37):
        RUNS.append(("FZ:" + p, "pristine", t))
PROBES.update({"FZ:" + k: v for k, v in list(PROBES.items())})
