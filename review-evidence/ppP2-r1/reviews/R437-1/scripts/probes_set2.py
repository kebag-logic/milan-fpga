# Directed probes: does each surviving planted defect change observable
# behaviour? Each probe phase runs on the pristine RTL and on its mutant.

RTL = "hdl/packet_engine/KL_pp_nvm_port.sv"
SIM = "tb/nvm_port/sim_main.cpp"
S = "tb/nvm_port"

def phase(body):
    return (SIM, "  a_short_command_is_a_device_error();\n  every_operation_got_what_it_was_owed();",
            "  a_short_command_is_a_device_error();\n  {\n" + body + "\n  }\n"
            "  every_operation_got_what_it_was_owed();")

# drained bytes of an owed READ must restart the count of a request blocked on it
PH_X18 = phase(r'''
    fresh_reset();
    h.deadline_ok = true;
    const std::vector<uint8_t> rec = frame(2, pattern(40, 0x29));
    CHECK(h.commit(2, rec) == 0, "PROBE setup");
    h.rstall = 60;                                   // a slow but moving device
    int rc = silenced(false, rec, SIL_BYTE, 1, TMO + 20, 10);
    CHECK(rc == 1 && h.last_cause == 3, "PROBE-X18 setup: payload READ abandoned (rc %d)", rc);
    h.ops.clear();
    rc = h.restore(2);                               // blocked while the owed READ drains slowly
    CHECK(rc == 0 && h.rbytes == rec,
          "PROBE-X18 a restore blocked on an owed READ that drains one byte every 60 "
          "cycles is served, never DEADLINE (rc %d, cause %d)", rc, h.last_cause);
    h.rstall = 0;
    h.quiesce_model();
    h.deadline_ok = false;''')

# the owed command's done must restart the count of a request blocked on it
PH_X17 = phase(r'''
    fresh_reset();
    h.deadline_ok = true;
    const std::vector<uint8_t> rec = frame(2, pattern(40, 0x2A));
    const std::vector<uint8_t> other = frame(5, pattern(24, 0x2A));
    CHECK(h.commit(2, rec) == 0 && h.commit(5, other) == 0, "PROBE setup");
    int rc = silenced(true, rec, SIL_DONE, 0, TMO + 1 + 90);   // ERASE done 90 after the verdict
    CHECK(rc == 1 && h.last_cause == 3 && h.d_busy, "PROBE-X17 setup: ERASE abandoned (rc %d)", rc);
    h.gnt_delay = 60;                                 // a legal grant delay, below TMO
    h.ops.clear();
    rc = h.restore(5);
    CHECK(rc == 0 && h.rbytes == other,
          "PROBE-X17 a restore blocked on an owed ERASE whose done comes ~60 cycles "
          "into its wait, then granted 60 cycles later, is served (rc %d, cause %d)",
          rc, h.last_cause);
    h.gnt_delay = 1;
    h.quiesce_model();
    h.deadline_ok = false;''')

# an owed command ending in err while a request waits is credited to no operation
PH_X24 = phase(r'''
    fresh_reset();
    h.deadline_ok = true;
    const std::vector<uint8_t> rec = frame(2, pattern(40, 0x2B));
    const std::vector<uint8_t> other = frame(5, pattern(24, 0x2B));
    CHECK(h.commit(2, rec) == 0 && h.commit(5, other) == 0, "PROBE setup");
    int rc = silenced(true, rec, SIL_DONE, 0, -1);    // ERASE never done: owed
    CHECK(rc == 1 && h.last_cause == 3 && h.d_busy, "PROBE-X24 setup: ERASE abandoned (rc %d)", rc);
    h.clear_capture(); h.ops.clear();
    h.m_mode = 2; h.m_stall = 0;
    h.start(false, 5);
    for (int i = 0; i < 20; ++i) h.tick();           // the restore waits on the owed ERASE
    h.end_command_now(/*with_err=*/true);            // the device ends the ERASE with err
    rc = h.run_op();
    CHECK(rc == 0 && h.rbytes == other,
          "PROBE-X24 an owed ERASE ending in err while a restore waits: the err is "
          "credited to no operation and the restore is served (rc %d, cause %d)",
          rc, h.last_cause);
    h.quiesce_model();
    h.deadline_ok = false;''')

# a deadline in the WRITE's completion window leaves the WRITE owed
PH_X12 = phase(r'''
    fresh_reset();
    h.deadline_ok = true;
    const std::vector<uint8_t> rec = frame(2, pattern(40, 0x2C));
    CHECK(h.commit(2, rec) == 0, "PROBE setup");
    int rc = silenced(true, rec, SIL_DONE, 1, 3 * TMO);   // the WRITE's done 3 deadlines late
    CHECK(rc == 1 && h.last_cause == 3 && h.d_busy, "PROBE-X12 setup: WRITE abandoned in S_WWAIT (rc %d)", rc);
    h.ops.clear();
    rc = h.commit(2, rec);
    CHECK(h.req_while_owed == 0,
          "PROBE-X12 a commit issued while the abandoned WRITE is still owed requests "
          "nothing over it (%d request cycles, rc %d)", h.req_while_owed, rc);
    for (int i = 0; i < 4 * TMO && h.d_busy; ++i) h.tick();
    h.quiesce_model();
    h.deadline_ok = false;''')

M_X18 = (RTL, "                  || (dev_rvalid_i && dev_rready_o);",
              "                  || (dev_rvalid_i && dev_rready_o && !owed_r);")
M_X17 = (RTL, "                  || (dev_done_i && (dev_cmd_owned_w || owed_r))",
              "                  || (dev_done_i && dev_cmd_owned_w)")
M_X24 = (RTL, "        S_WEREQ: if (!owed_r) begin   // an owed command blocks the request",
              "        S_WEREQ: begin")
M_X24R = (RTL, "        S_RHREQ: if (!owed_r) begin   // an owed command blocks the request",
               "        S_RHREQ: begin")
M_X12 = (RTL, "      end else if (dl_w && dev_cmd_owned_w) begin",
              "      end else if (dl_w && dev_cmd_owned_w && (state_r != S_WWAIT)) begin")

PROBES_ALL = [
    ("Q18-pristine", S, [PH_X18]), ("Q18-mutant", S, [PH_X18, M_X18]),
    ("Q17-pristine", S, [PH_X17]), ("Q17-mutant", S, [PH_X17, M_X17]),
    ("Q24-pristine", S, [PH_X24]), ("Q24-mutant-rhreq", S, [PH_X24, M_X24R]),
    ("Q12-pristine", S, [PH_X12]), ("Q12-mutant", S, [PH_X12, M_X12]),
]

# Round 1 ran PROBES_ALL with Q17/Q24 restoring region 2, which the abandoned
# ERASE itself erases (a probe error: UNFRAMED on pristine). Round 2 restores an
# untouched region 5 and re-ran Q17/Q24 only. Set ALL=1 to run all eight.
import os
PROBES = PROBES_ALL if os.environ.get("ALL") else [p for p in PROBES_ALL if p[0][:3] in ("Q17", "Q24")]
