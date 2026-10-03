# R437-3: the randomized harness (fuzz_main.cpp) against my round-2 pause plants
# (exact round-2 edit text) and further false-DEADLINE plants, at bounds 1, 2, 3
# and 37; and the head's randomized harness at the bounds no build covers (4-19)
# and above (100, 1000). Names starting FZ: build fuzz_main.cpp.
PROBES = {
    "FZ:base": [],
    "FZ:Y1_wewait_owes_latched": [('RTL', '                  || (((state_r == S_WEWAIT) || (state_r == S_WWAIT) || (state_r == S_RHWAIT)\n                       || (state_r == S_RPWAIT)) && !done_seen_r)\n', '                  || (((state_r == S_WWAIT) || (state_r == S_RHWAIT) || (state_r == S_RPWAIT)) && !done_seen_r) || (state_r == S_WEWAIT)\n')],
    "FZ:Y2_rhwait_owes_latched": [('RTL', '                  || (((state_r == S_WEWAIT) || (state_r == S_WWAIT) || (state_r == S_RHWAIT)\n                       || (state_r == S_RPWAIT)) && !done_seen_r)\n', '                  || (((state_r == S_WEWAIT) || (state_r == S_WWAIT) || (state_r == S_RPWAIT)) && !done_seen_r) || (state_r == S_RHWAIT)\n')],
    "FZ:Y3_wwait_owes_latched": [('RTL', '                  || (((state_r == S_WEWAIT) || (state_r == S_WWAIT) || (state_r == S_RHWAIT)\n                       || (state_r == S_RPWAIT)) && !done_seen_r)\n', '                  || (((state_r == S_WEWAIT) || (state_r == S_RHWAIT) || (state_r == S_RPWAIT)) && !done_seen_r) || (state_r == S_WWAIT)\n')],
    "FZ:Y4_rpwait_owes_latched": [('RTL', '                  || (((state_r == S_WEWAIT) || (state_r == S_WWAIT) || (state_r == S_RHWAIT)\n                       || (state_r == S_RPWAIT)) && !done_seen_r)\n', '                  || (((state_r == S_WEWAIT) || (state_r == S_WWAIT) || (state_r == S_RHWAIT)) && !done_seen_r) || (state_r == S_RPWAIT)\n')],
    "FZ:Y5_count_paused_cycles": [('RTL', "    else if (owe_w && !tmo_hit_w)           tmo_r <= tmo_r + TMO_W_C'(1);", "    else if (!tmo_hit_w && (state_r != S_FIN)) tmo_r <= tmo_r + TMO_W_C'(1);")],
    "FZ:Y6_rhfwd_owed": [('RTL', '                  || (state_r == S_WHPUMP) || (state_r == S_RHCOLL)\n', '                  || (state_r == S_WHPUMP) || (state_r == S_RHCOLL) || (state_r == S_RHFWD)\n')],
    "FZ:Y7_whdr_owed": [('RTL', '                  || (state_r == S_WHPUMP) || (state_r == S_RHCOLL)\n', '                  || (state_r == S_WHPUMP) || (state_r == S_RHCOLL) || (state_r == S_WHDR)\n')],
    "FZ:Y8_owed_wait_paused": [('RTL', '  assign owe_w    = req_st_w\n', '  assign owe_w    = (req_st_w && !owed_r)\n')],
    "FZ:Y11_verdict_on_paused_cycle": [('RTL', '  assign dl_w = owe_w && !prog_w && tmo_hit_w;', '  assign dl_w = (owe_w || (state_r == S_WDPUMP) || (state_r == S_RPPUMP)) && !prog_w && tmo_hit_w;')],
    "FZ:Y12_manager_handshake_is_progress": [('RTL', '                  || (dev_rvalid_i && dev_rready_o);', '                  || (dev_rvalid_i && dev_rready_o)\n                  || (nvm_rvalid_o && nvm_rready_i) || (nvm_wvalid_i && nvm_wready_o);')],
    "FZ:Y13_rppump_pause_clears": [('RTL', "    else if (prog_w || (state_r == S_IDLE)) tmo_r <= '0;", "    else if (prog_w || (state_r == S_IDLE) || ((state_r == S_RPPUMP) && !nvm_rready_i)) tmo_r <= '0;")],
    "FZ:Y15_counter_one_bit_short": [('RTL', '  logic [TMO_W_C-1:0] tmo_r;        // owed cycles without the owed event', '  logic [TMO_W_C-2:0] tmo_r;        // owed cycles without the owed event')],
    "FZ:Y16_verdict_any_busy_cycle": [("RTL", "  assign dl_w = owe_w && !prog_w && tmo_hit_w;",
                                       "  assign dl_w = (state_r != S_IDLE) && (state_r != S_FIN) && !prog_w && tmo_hit_w;")],
    # the verdict one owed cycle early (D2-like)
    "FZ:V1_verdict_one_early": [("RTL", "  assign tmo_hit_w = (tmo_r == TMO_W_C'(MEM_TIMEOUT_CYC_P));",
                                 "  assign tmo_hit_w = (tmo_r == TMO_W_C'(MEM_TIMEOUT_CYC_P - 1));")],
    # a stray done (owned by nobody) counted as progress
    "FZ:V2_stray_done_progress": [("RTL", "                  || (dev_done_i && (dev_cmd_owned_w || owed_r))",
                                   "                  || dev_done_i")],
}
RUNS = [("FZ:base", "pristine", t) for t in list(range(1, 20)) + [37, 100, 1000]]
RUNS += [(p, "pristine", t) for p in PROBES if p != "FZ:base" for t in (1, 2, 3, 37)]
