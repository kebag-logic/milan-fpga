# R437-2 reviewer-written directed checks (Z-series), added to a COPY of the
# head's harness, run against the head RTL (must pass, every model, both bounds)
# and against the surviving planted defects Y1, Y11 and Y16 (must fail).
#
# Z1a/Z1b: the device presents its owed byte after exactly TMO silent owed
#   cycles (T24's tolerated arm) while the manager drops rready / wvalid on
#   that very cycle: the dropped cycle owes nothing, so the head must pause and
#   then take the byte: done, byte-exact, no DEADLINE.
# Z2: a backend without erase semantics answers ERASE on its own grant (T21's
#   freedom) and grants the WRITE exactly TMO cycles late (T24's tolerated
#   S_WWREQ arm): done, byte-exact, no DEADLINE.
# INV: the invariant D23's equivalence claim rests on -- owed_r is set only in
#   S_IDLE, S_FIN, S_WHDR, S_WEREQ or S_RHREQ -- as an RTL-side monitor that
#   prints a FAIL line on any violating cycle.

HARNESS = [
    ("SIM", "  int held_since_evt = 0;                 // strobe cycles dropped since the last event\n",
            "  int held_since_evt = 0;                 // strobe cycles dropped since the last event\n"
            "  int probe_drop_gap = -1;                // R437-2: drop the strobe at this gap from the last event\n"
            "  int probe_drops = 0;                    // R437-2: strobes so dropped\n"),
    ("SIM", "    const bool drop = mgr_drop_every > 0 && cycles % mgr_drop_every == 0;\n",
            "    const bool pdrop = probe_drop_gap > 0 && cycles - last_evt == probe_drop_gap;\n"
            "    const bool drop = (mgr_drop_every > 0 && cycles % mgr_drop_every == 0) || pdrop;\n"
            "    if (pdrop && m_mode != 0) ++probe_drops;\n"),
    ("SIM", "  a_manager_strobe_never_holds_the_deadline_off();\n  reset_mid_commit_at_six_stages();\n",
            "  a_manager_strobe_never_holds_the_deadline_off();\n"
            "  {\n"
            "    fresh_reset();\n"
            "    const std::vector<uint8_t> rec = frame(2, pattern(40, 0x31));\n"
            "    CHECK(h.commit(2, rec) == 0, \"Z setup: region 2 committed\");\n"
            "    h.probe_drops = 0; h.probe_drop_gap = TMO + 1;\n"
            "    int rc = silenced(false, rec, SIL_BYTE, 1, TMO, 10);\n"
            "    h.probe_drop_gap = -1;\n"
            "    CHECK(rc == 0 && h.done_pulses == 1 && h.err_pulses == 0 && h.rbytes == rec && h.probe_drops >= 1,\n"
            "          \"Z1a payload byte 10 presented after TMO silent owed cycles, rready dropped on that cycle: \"\n"
            "          \"tolerated, done, byte-exact (rc %d, cause %d, drops %d)\", rc, h.last_cause, h.probe_drops);\n"
            "    fresh_reset(); CHECK(h.commit(2, rec) == 0, \"Z setup b\");\n"
            "    h.probe_drops = 0; h.probe_drop_gap = TMO + 1;\n"
            "    rc = silenced(true, rec, SIL_BYTE, 1, TMO, 20);\n"
            "    h.probe_drop_gap = -1;\n"
            "    CHECK(rc == 0 && h.done_pulses == 1 && h.err_pulses == 0 && h.sent == rec && h.probe_drops >= 1,\n"
            "          \"Z1b WRITE byte 20 taken after TMO silent owed cycles, wvalid dropped on that cycle: \"\n"
            "          \"tolerated, done, byte-exact (rc %d, cause %d, drops %d)\", rc, h.last_cause, h.probe_drops);\n"
            "    fresh_reset(); CHECK(h.commit(2, rec) == 0, \"Z setup c\");\n"
            "    h.gnt_done_on_erase = true;\n"
            "    rc = silenced(true, rec, SIL_GNT, 1, TMO);\n"
            "    h.gnt_done_on_erase = false;\n"
            "    CHECK(rc == 0 && h.done_pulses == 1 && h.err_pulses == 0 && h.sent == rec && h.gnt_done_pairs == 1,\n"
            "          \"Z2 ERASE answered on its own grant, WRITE granted TMO cycles late: tolerated, done, \"\n"
            "          \"byte-exact (rc %d, cause %d, pairs %d)\", rc, h.last_cause, h.gnt_done_pairs);\n"
            "  }\n"
            "  reset_mid_commit_at_six_stages();\n"),
]

INVARIANT = [
    ("RTL", "endmodule\n",
            "  always_ff @(posedge clk_i) begin : r437_owed_invariant\n"
            "    if (rst_n && owed_r && !((state_r == S_IDLE) || (state_r == S_FIN) || (state_r == S_WHDR)\n"
            "                             || (state_r == S_WEREQ) || (state_r == S_RHREQ)))\n"
            "      $display(\"FAIL: R437-2 INV owed_r set in state %0d\", state_r);\n"
            "  end\n"
            "endmodule\n"),
]

WAIT_TERM_OLD = ("                  || (((state_r == S_WEWAIT) || (state_r == S_WWAIT) || (state_r == S_RHWAIT)\n"
                 "                       || (state_r == S_RPWAIT)) && !done_seen_r)\n")
Y1 = [("RTL", WAIT_TERM_OLD,
       "                  || (((state_r == S_WWAIT) || (state_r == S_RHWAIT) || (state_r == S_RPWAIT)) && !done_seen_r)\n"
       "                  || (state_r == S_WEWAIT)\n")]
Y11 = [("RTL", "  assign dl_w = owe_w && !prog_w && tmo_hit_w;",
               "  assign dl_w = (owe_w || (state_r == S_WDPUMP) || (state_r == S_RPPUMP)) && !prog_w && tmo_hit_w;")]
Y16 = [("RTL", "  assign dl_w = owe_w && !prog_w && tmo_hit_w;",
               "  assign dl_w = (state_r != S_IDLE) && (state_r != S_FIN) && !prog_w && tmo_hit_w;")]

PROBES = {
    "Z_head": HARNESS + INVARIANT,
    "Z_Y1": HARNESS + Y1,
    "Z_Y11": HARNESS + Y11,
    "Z_Y16": HARNESS + Y16,
    "Y16_verdict_any_busy_cycle": Y16,
}
ALL_MODELS = ["pristine", "half-page", "page-buffered NOR", "lazy erase", "lazy erase + page-buffered",
              "coincident completion", "unsolicited completion", "short read", "silent"]
RUNS = []
for t in (100, 37):
    for m in ALL_MODELS:
        RUNS.append(("Z_head", m, t))
    for m in ALL_MODELS[:7]:
        RUNS.append(("Y16_verdict_any_busy_cycle", m, t))
    for p in ("Z_Y1", "Z_Y11", "Z_Y16"):
        RUNS.append((p, "pristine", t))
        RUNS.append((p, "coincident completion", t))
