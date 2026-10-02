# Round-1 probes re-run at the exact head c0715410, edits copied unchanged from
# the round-1 public packets: R436-1 (scripts/probe.py: W15, W15b, W16) and
# R437-1 (scripts/probes_set1.py: X12, X17, X18, X20, X24, X24b).
#
# W6 (R436-1) planted "the count paused, not cleared, on unowed cycles" into the
# round-1 RTL; its anchor ("else if (!owe_w || prog_w) tmo_r <= '0;") no longer
# exists because the pause IS the head's design. Its semantics at the head are
# the pause WITHOUT the round-2 latched-done term, i.e. the head with
# "&& !done_seen_r" removed from the wait-state owe term (the same edit as the
# figures gate's D26); run here as W6@head.
#
# P1 (R437-1 S1, manager toggling its strobe one cycle in 50 against a silent
# device): its toggle member's anchor no longer exists; the head's harness now
# has the same mechanism (mgr_drop_every). The phase body is otherwise round 1's.
RTL_W15 = [("RTL", "S_RHREQ: if (!owed_r) begin", "S_RHREQ: begin")]
RTL_W15b = [("RTL", "S_WEREQ: if (!owed_r) begin", "S_WEREQ: begin")]
RTL_W16 = [("RTL", "|| (dev_rvalid_i && dev_rready_o);", "|| (dev_rvalid_i && dev_rready_o && !owed_r);")]
X12 = [("RTL", "      end else if (dl_w && dev_cmd_owned_w) begin",
               "      end else if (dl_w && dev_cmd_owned_w && (state_r != S_WWAIT)) begin")]
X17 = [("RTL", "                  || (dev_done_i && (dev_cmd_owned_w || owed_r))",
               "                  || (dev_done_i && dev_cmd_owned_w)")]
X18 = [("RTL", "                  || (dev_rvalid_i && dev_rready_o);",
               "                  || (dev_rvalid_i && dev_rready_o && !owed_r);")]
X20 = [("RTL", "      end else if (lg_r && dev_gnt_i && !dev_done_i && !dev_err_i) begin",
               "      end else if (lg_r && dev_gnt_i && !dev_done_i) begin")]
X24 = [("RTL", "        S_RHREQ: if (!owed_r) begin   // an owed command blocks the request",
               "        S_RHREQ: begin")]
X24b = [("RTL", "        S_RHREQ: if (!owed_r) begin   // an owed command blocks the request", "        S_RHREQ: begin"),
        ("RTL", "        S_RPREQ: if (!owed_r) begin   // an owed command blocks the request", "        S_RPREQ: begin"),
        ("RTL", "        S_WEREQ: if (!owed_r) begin   // an owed command blocks the request", "        S_WEREQ: begin"),
        ("RTL", "        S_WWREQ: if (!owed_r) begin   // an owed command blocks the request", "        S_WWREQ: begin")]
W6 = [("RTL", "                       || (state_r == S_RPWAIT)) && !done_seen_r)",
              "                       || (state_r == S_RPWAIT)))")]
P1 = [("SIM", "  a_short_command_is_a_device_error();\n  every_operation_got_what_it_was_owed();",
       "  a_short_command_is_a_device_error();\n  {\n"
       "    fresh_reset();\n"
       "    h.deadline_ok = true;\n"
       "    const std::vector<uint8_t> rec = frame(2, pattern(40, 0x24));\n"
       "    CHECK(h.commit(2, rec) == 0, \"PROBE setup: region 2 committed\");\n"
       "    h.mgr_drop_every = 50;\n"
       "    int rc = silenced(false, rec, SIL_BYTE, 1, -1, 10);\n"
       "    CHECK(rc == 1 && h.err_pulses == 1 && h.last_cause == 3,\n"
       "          \"PROBE-RR silent payload READ, manager rready low 1 cycle in 50: one err \"\n"
       "          \"DEADLINE within a bound (rc %d, cause %d)\", rc, h.last_cause);\n"
       "    h.mgr_drop_every = 0;\n"
       "    h.quiesce_model();\n"
       "    fresh_reset();\n"
       "    CHECK(h.commit(2, rec) == 0, \"PROBE setup 2: region 2 committed\");\n"
       "    h.mgr_drop_every = 50;\n"
       "    rc = silenced(true, rec, SIL_BYTE, 1, -1, 20);\n"
       "    CHECK(rc == 1 && h.err_pulses == 1 && h.last_cause == 3,\n"
       "          \"PROBE-WV silent WRITE byte, manager wvalid low 1 cycle in 50: one err \"\n"
       "          \"DEADLINE within a bound (rc %d, cause %d)\", rc, h.last_cause);\n"
       "    h.mgr_drop_every = 0;\n"
       "    h.quiesce_model();\n"
       "    fresh_reset();\n"
       "    h.deadline_ok = false;\n"
       "  }\n"
       "  every_operation_got_what_it_was_owed();")]

PROBES = {"W15": RTL_W15, "W15b": RTL_W15b, "W16": RTL_W16, "W6at_head": W6,
          "X12": X12, "X17": X17, "X18": X18, "X20": X20, "X24": X24, "X24b": X24b,
          "P1_head": P1}
LEGAL = ["pristine", "half-page", "page-buffered NOR", "lazy erase", "lazy erase + page-buffered",
         "coincident completion", "unsolicited completion"]
RUNS = []
for t in (100, 37):
    for p in PROBES:
        models = LEGAL if p in ("W6at_head", "X20") else ["pristine", "coincident completion"]
        for m in models:
            RUNS.append((p, m, t))
