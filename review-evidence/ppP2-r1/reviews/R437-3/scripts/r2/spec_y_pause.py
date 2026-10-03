# R437-2 reviewer-planted defects in the deadline's pause logic (Y-series),
# plus the baseline. Each is run at TMO 100 and 37 under the models named.
WAIT_TERM_OLD = ("                  || (((state_r == S_WEWAIT) || (state_r == S_WWAIT) || (state_r == S_RHWAIT)\n"
                 "                       || (state_r == S_RPWAIT)) && !done_seen_r)\n")


def _wait_term(drop):
    keep = [s for s in ("S_WEWAIT", "S_WWAIT", "S_RHWAIT", "S_RPWAIT") if s not in drop]
    terms = "((" + " || ".join(f"(state_r == {s})" for s in keep) + ") && !done_seen_r)"
    loose = " || ".join(f"(state_r == {s})" for s in drop)
    return f"                  || {terms} || {loose}\n"


PROBES = {
    "base": [],
    # the latched-done term dropped from ONE wait state at a time
    "Y1_wewait_owes_latched": [("RTL", WAIT_TERM_OLD, _wait_term(["S_WEWAIT"]))],
    "Y2_rhwait_owes_latched": [("RTL", WAIT_TERM_OLD, _wait_term(["S_RHWAIT"]))],
    "Y3_wwait_owes_latched": [("RTL", WAIT_TERM_OLD, _wait_term(["S_WWAIT"]))],
    "Y4_rpwait_owes_latched": [("RTL", WAIT_TERM_OLD, _wait_term(["S_RPWAIT"]))],
    # a paused (owes-nothing) cycle counted anyway
    "Y5_count_paused_cycles": [("RTL", "    else if (owe_w && !tmo_hit_w)           tmo_r <= tmo_r + TMO_W_C'(1);",
                                       "    else if (!tmo_hit_w && (state_r != S_FIN)) tmo_r <= tmo_r + TMO_W_C'(1);")],
    # the header forward / header collection charged to the device
    "Y6_rhfwd_owed": [("RTL", "                  || (state_r == S_WHPUMP) || (state_r == S_RHCOLL)\n",
                              "                  || (state_r == S_WHPUMP) || (state_r == S_RHCOLL) || (state_r == S_RHFWD)\n")],
    "Y7_whdr_owed": [("RTL", "                  || (state_r == S_WHPUMP) || (state_r == S_RHCOLL)\n",
                             "                  || (state_r == S_WHPUMP) || (state_r == S_RHCOLL) || (state_r == S_WHDR)\n")],
    # a request waiting on an owed command pauses instead of counting (starvation)
    "Y8_owed_wait_paused": [("RTL", "  assign owe_w    = req_st_w\n", "  assign owe_w    = (req_st_w && !owed_r)\n")],
    # the pump owes only when the device is already ready/valid (starvation)
    "Y9_wdpump_owes_only_when_ready": [("RTL", "                  || ((state_r == S_WDPUMP) && nvm_wvalid_i)\n",
                                               "                  || ((state_r == S_WDPUMP) && nvm_wvalid_i && dev_wready_i)\n")],
    "Y10_rppump_owes_only_when_valid": [("RTL", "                  || ((state_r == S_RPPUMP) && nvm_rready_i);",
                                                "                  || ((state_r == S_RPPUMP) && nvm_rready_i && dev_rvalid_i);")],
    # the verdict fires on a paused cycle once the count is at its bound
    "Y11_verdict_on_paused_cycle": [("RTL", "  assign dl_w = owe_w && !prog_w && tmo_hit_w;",
                                            "  assign dl_w = (owe_w || (state_r == S_WDPUMP) || (state_r == S_RPPUMP)) && !prog_w && tmo_hit_w;")],
    # a manager handshake counted as progress
    "Y12_manager_handshake_is_progress": [("RTL", "                  || (dev_rvalid_i && dev_rready_o);",
                                                  "                  || (dev_rvalid_i && dev_rready_o)\n"
                                                  "                  || (nvm_rvalid_o && nvm_rready_i) || (nvm_wvalid_i && nvm_wready_o);")],
    # a paused cycle in the payload pumps restarts the count (half of the round-1 rule)
    "Y13_rppump_pause_clears": [("RTL", "    else if (prog_w || (state_r == S_IDLE)) tmo_r <= '0;",
                                        "    else if (prog_w || (state_r == S_IDLE) || ((state_r == S_RPPUMP) && !nvm_rready_i)) tmo_r <= '0;")],
    "Y14_wdpump_pause_clears": [("RTL", "    else if (prog_w || (state_r == S_IDLE)) tmo_r <= '0;",
                                        "    else if (prog_w || (state_r == S_IDLE) || ((state_r == S_WDPUMP) && !nvm_wvalid_i)) tmo_r <= '0;")],
    # the count width one bit short (wraps before the bound at 100 and 37)
    "Y15_counter_one_bit_short": [("RTL", "  logic [TMO_W_C-1:0] tmo_r;        // owed cycles without the owed event",
                                          "  logic [TMO_W_C-2:0] tmo_r;        // owed cycles without the owed event")],
}

ALL_MODELS = ["pristine", "half-page", "page-buffered NOR", "lazy erase", "lazy erase + page-buffered",
              "coincident completion", "unsolicited completion", "short read", "silent"]
RUNS = []
for p in PROBES:
    if p == "base":
        for m in ALL_MODELS:
            for t in (100, 37):
                RUNS.append((p, m, t))
    elif p.startswith(("Y1_", "Y2_", "Y3_", "Y4_")):
        for m in ALL_MODELS[:7]:
            for t in (100, 37):
                RUNS.append((p, m, t))
    else:
        RUNS.append((p, "pristine", 100))
        RUNS.append((p, "pristine", 37))
