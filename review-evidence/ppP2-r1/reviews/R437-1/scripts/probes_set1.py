# Reviewer-planted defects in the watchdog and owed-command logic of
# hdl/packet_engine/KL_pp_nvm_port.sv at 70bf017d, plus behavioural probes.
# Each entry: (name, suite dir, [(file, old, new), ...]); every old must occur once.
RTL = "hdl/packet_engine/KL_pp_nvm_port.sv"
SIM = "tb/nvm_port/sim_main.cpp"
MK = "tb/nvm_port/Makefile"
S = "tb/nvm_port"

# ---- a reviewer phase appended before the run-wide checks -------------------
TOGGLE_MEMBER = (SIM, "  int mgr_rstall = 0;\n", "  int mgr_rstall = 0;\n  int rr_toggle = 0;\n")
TOGGLE_W = (SIM, "      bool v = (m_widx < m_wbytes.size() && m_stall == 0);",
            "      bool v = (m_widx < m_wbytes.size() && m_stall == 0)\n"
            "               && !(rr_toggle > 0 && cycles % rr_toggle == 0);")
TOGGLE_R = (SIM, "      dut->nvm_rready_i = (m_stall == 0);",
            "      dut->nvm_rready_i = (m_stall == 0)\n"
            "               && !(rr_toggle > 0 && cycles % rr_toggle == 0);")

def phase(body):
    return (SIM, "  a_short_command_is_a_device_error();\n  every_operation_got_what_it_was_owed();",
            "  a_short_command_is_a_device_error();\n  {\n" + body + "\n  }\n"
            "  every_operation_got_what_it_was_owed();")

PROBE_RR = phase(r'''
    fresh_reset();
    h.deadline_ok = true;
    const std::vector<uint8_t> rec = frame(2, pattern(40, 0x24));
    CHECK(h.commit(2, rec) == 0, "PROBE setup: region 2 committed");
    // the device stops presenting the payload READ's 11th byte for ever, and
    // the manager drops rready one cycle in every 50 (a legal ready)
    h.rr_toggle = 50;
    int rc = silenced(false, rec, SIL_BYTE, 1, -1, 10);
    CHECK(rc == 1 && h.err_pulses == 1 && h.last_cause == 3,
          "PROBE-RR silent payload READ, manager rready low 1 cycle in 50: one err "
          "DEADLINE within a bound (rc %d, cause %d)", rc, h.last_cause);
    h.rr_toggle = 0;
    h.quiesce_model();
    fresh_reset();
    CHECK(h.commit(2, rec) == 0, "PROBE setup 2: region 2 committed");
    // the device stops taking the WRITE's 21st byte for ever, and the manager
    // drops wvalid one cycle in every 50 while that byte is not accepted
    h.rr_toggle = 50;
    rc = silenced(true, rec, SIL_BYTE, 1, -1, 20);
    CHECK(rc == 1 && h.err_pulses == 1 && h.last_cause == 3,
          "PROBE-WV silent WRITE byte, manager wvalid low 1 cycle in 50: one err "
          "DEADLINE within a bound (rc %d, cause %d)", rc, h.last_cause);
    h.rr_toggle = 0;
    h.quiesce_model();
    fresh_reset();
    h.deadline_ok = false;
    h.wedges = 0;   // keep RW1 about the original run''')

TMO64 = [(MK, "-GMEM_TIMEOUT_CYC_P=100", "-GMEM_TIMEOUT_CYC_P=64"),
         (SIM, "constexpr int TMO       = 100;", "constexpr int TMO       = 64;")]
TMO37 = [(MK, "-GMEM_TIMEOUT_CYC_P=100", "-GMEM_TIMEOUT_CYC_P=37"),
         (SIM, "constexpr int TMO       = 100;", "constexpr int TMO       = 37;")]
X15 = (RTL, ": $clog2(33'(MEM_TIMEOUT_CYC_P) + 33'd1)", ": $clog2(33'(MEM_TIMEOUT_CYC_P))")

PROBES = [
    ("P0-pristine", S, []),
    ("P1-manager-toggle", S, [TOGGLE_MEMBER, TOGGLE_W, TOGGLE_R, PROBE_RR]),
    ("P2-tmo64-pristine", S, TMO64),
    ("P3-tmo37-pristine", S, TMO37),
    # X1 the header collect owes nothing
    ("X01-owe-no-rhcoll", S, [(RTL, "                  || (state_r == S_WHPUMP) || (state_r == S_RHCOLL)\n",
                                    "                  || (state_r == S_WHPUMP)\n")]),
    # X2 the header pump owes nothing
    ("X02-owe-no-whpump", S, [(RTL, "                  || (state_r == S_WHPUMP) || (state_r == S_RHCOLL)\n",
                                    "                  || (state_r == S_RHCOLL)\n")]),
    # X3 a read byte is not progress
    ("X03-rbyte-not-progress", S, [(RTL, "                  || (dev_rvalid_i && dev_rready_o);",
                                         "                  ;")]),
    # X5 an owed command's err does not end it
    ("X05-owed-not-ended-by-err", S, [(RTL, "        if (dev_done_i || dev_err_i) owed_r <= 1'b0;",
                                           "        if (dev_done_i) owed_r <= 1'b0;")]),
    # X10 a deadline in the payload pump leaves an undrained owed command
    ("X10-rd-st-no-rppump", S, [(RTL, "                  || (state_r == S_RPPUMP) || (state_r == S_RPWAIT);\n  assign owe_w",
                                      "                  || (state_r == S_RPWAIT);\n  assign owe_w")]),
    # X11 a late-granted header READ is owed as a WRITE (no drain)
    ("X11-rd-st-no-rhreq", S, [(RTL, "  assign rd_st_w  = (state_r == S_RHREQ) || (state_r == S_RHCOLL)",
                                     "  assign rd_st_w  = (state_r == S_RHCOLL)")]),
    # X12 a deadline in the WRITE's completion window leaves nothing owed
    ("X12-wwait-not-owed", S, [(RTL, "      end else if (dl_w && dev_cmd_owned_w) begin",
                                     "      end else if (dl_w && dev_cmd_owned_w && (state_r != S_WWAIT)) begin")]),
    # X14 the guard refuses the largest legal value
    ("X14-guard-off-by-one", S, [(RTL, "(MEM_TIMEOUT_CYC_P > 32'h7FFF_FFFF)", "(MEM_TIMEOUT_CYC_P >= 32'h7FFF_FFFF)")]),
    # X15 the counter one bit narrow at a power of two
    ("X15-width-at-100", S, [X15]),
    ("X15-width-at-64", S, TMO64 + [X15]),
    # X16 a request blocked by an owed command never times out
    ("X16-blocked-req-owes-nothing", S, [(RTL, "  assign owe_w    = req_st_w\n",
                                              "  assign owe_w    = (req_st_w && !owed_r)\n")]),
    # X17 the owed command's done is not progress
    ("X17-owed-done-not-progress", S, [(RTL, "                  || (dev_done_i && (dev_cmd_owned_w || owed_r))",
                                             "                  || (dev_done_i && dev_cmd_owned_w)")]),
    # X18 a drained byte of the owed READ is not progress
    ("X18-drain-not-progress", S, [(RTL, "                  || (dev_rvalid_i && dev_rready_o);",
                                         "                  || (dev_rvalid_i && dev_rready_o && !owed_r);")]),
    # X20 a late grant that carries err is still owed
    ("X20-late-gnt-err-owed", S, [(RTL, "      end else if (lg_r && dev_gnt_i && !dev_done_i && !dev_err_i) begin",
                                        "      end else if (lg_r && dev_gnt_i && !dev_done_i) begin")]),
    # X21 reset does not clear the owed command
    ("X21-owed-survives-reset", S, [(RTL, "      owed_r    <= 1'b0;\n      owed_rd_r <= 1'b0;",
                                          "      owed_rd_r <= 1'b0;")]),
    # X22 reset does not clear the count (expected equivalent: idle clears it)
    ("X22-tmo-survives-reset", S, [(RTL, "    if (!rst_n)                tmo_r <= '0;\n    else if (!owe_w || prog_w) tmo_r <= '0;",
                                         "    if (!owe_w || prog_w) tmo_r <= '0;")]),
    # X23 the late-grant flag survives reset
    ("X23-lg-survives-reset", S, [(RTL, "      owed_rd_r <= 1'b0;\n      lg_r      <= 1'b0;\n",
                                        "      owed_rd_r <= 1'b0;\n")]),
    # X24 an owed command's terminal consumed by a waiting header-READ request
    ("X24-rhreq-unguarded", S, [(RTL, "        S_RHREQ: if (!owed_r) begin   // an owed command blocks the request",
                                      "        S_RHREQ: begin")]),
    ("X24b-all-req-unguarded", S, [
        (RTL, "        S_RHREQ: if (!owed_r) begin   // an owed command blocks the request", "        S_RHREQ: begin"),
        (RTL, "        S_RPREQ: if (!owed_r) begin   // an owed command blocks the request", "        S_RPREQ: begin"),
        (RTL, "        S_WEREQ: if (!owed_r) begin   // an owed command blocks the request", "        S_WEREQ: begin"),
        (RTL, "        S_WWREQ: if (!owed_r) begin   // an owed command blocks the request", "        S_WWREQ: begin")]),
    # X25 the counter does not saturate (expected equivalent)
    ("X25-no-saturation", S, [(RTL, "    else if (!tmo_hit_w)       tmo_r <= tmo_r + TMO_W_C'(1);",
                                    "    else                       tmo_r <= tmo_r + TMO_W_C'(1);")]),
    # X26 the owed drain also needs the port to be idle (drain stops in a blocked request)
    ("X26-drain-only-idle", S, [(RTL, "                      || (owed_r && owed_rd_r);        // the owed READ's drain",
                                      "                      || (owed_r && owed_rd_r && !req_st_w);")]),
    # X27 a deadline verdict also needs the device's busy (busy is informational)
    ("X27-verdict-needs-busy", S, [(RTL, "  assign dl_w = owe_w && !prog_w && tmo_hit_w;",
                                         "  assign dl_w = owe_w && !prog_w && tmo_hit_w && (dev_busy_i || req_st_w);")]),
    # X28 the late grant window two cycles (owed on a grant two cycles late)
    ("X28-cause-deadline-as-device-on-req", S, [(RTL, "    end else if (dl_w) begin\n      cause_r <= CAUSE_DEADLINE_C;",
                                                      "    end else if (dl_w && !req_st_w) begin\n      cause_r <= CAUSE_DEADLINE_C;")]),
]
