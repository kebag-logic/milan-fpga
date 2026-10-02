# #19's four mechanisms (pristine model) and #21's four mutations (each under
# its model), to read WHICH checks fail and whether their messages name the
# mechanism; then tb/acmp_nvm's planted defects that its README quotes.
RTL = "hdl/packet_engine/KL_pp_nvm_port.sv"
SIM = "tb/nvm_port/sim_main.cpp"
SHD = "hdl/acmp/KL_acmp_nvm_shadow.sv"
S = "tb/nvm_port"
A = "tb/acmp_nvm"

LATCH = "      if (dev_done_i && dev_cmd_owned_w) done_seen_r <= 1'b1;\n"
M8 = (RTL, "            if (done_seen_r || (dev_done_i && !(dev_rvalid_i && (hidx_r == 3'd7)))) begin",
           "            if (1'b0) begin")
UNSOL = (SIM, "  bool unsol_model = false;", "  bool unsol_model = true;")
COINC = (SIM, "  bool done_on_last_byte = false;", "  bool done_on_last_byte = true;")
SHORT = (SIM, "  bool short_model = false;", "  bool short_model = true;")
SILENT = (SIM, "  bool silent_model = false;", "  bool silent_model = true;")
LAZY = (SIM, "        int r = d_cur.region % N_REGIONS;\n        memset(store[r], 0xFF, REG_BYTES);\n",
             "        int r = d_cur.region % N_REGIONS;\n")

PROBES = [
    # issue #19
    ("I19-1-magic-lo", S, [(RTL, "(hdr_r[1] == MAGIC_LO_C)", "1'b1")]),
    ("I19-2-bound-lt", S, [(RTL, "(hdr_plen_w <= MAXP_C)", "(hdr_plen_w < MAXP_C)")]),
    ("I19-3-latch-deleted", S, [(RTL, LATCH, "")]),
    ("I19-3b-latch-deleted-other-way", S, [(RTL, LATCH, "      if (1'b0) done_seen_r <= 1'b1;\n")]),
    ("I19-4-shortread-defence-off", S, [M8]),
    # issue #21, each under its model
    ("I21-1-M6-unsolicited", S, [UNSOL, (RTL, LATCH, "      if (dev_done_i) done_seen_r <= 1'b1;\n")]),
    ("I21-2-latch-coincident", S, [COINC, (RTL, LATCH, "")]),
    ("I21-3-M8-short", S, [SHORT, M8]),
    ("I21-4-D1-silent", S, [SILENT, (RTL, "  assign dl_w = owe_w && !prog_w && tmo_hit_w;", "  assign dl_w = 1'b0;")]),
    # the models on pristine RTL, for the fail lists
    ("MOD-lazy", S, [LAZY]),
    ("MOD-short", S, [SHORT]),
    ("MOD-silent", S, [SILENT]),
    ("MOD-unsolicited", S, [UNSOL]),
    ("MOD-coincident", S, [COINC]),
    # tb/acmp_nvm
    ("ACMP-pristine", A, []),
    ("ACMP-A1-deadline-as-blank", A, [
        (SHD, "                   && (nvm_err_cause_i != CAUSE_UNFRAMED_C);",
              "                   && (nvm_err_cause_i == 2'd1);"),
        (SHD, "                         && (nvm_err_cause_i == CAUSE_UNFRAMED_C))",
              "                         && (nvm_err_cause_i != 2'd1))")]),
    ("ACMP-A2-no-port-deadline", A, [(RTL, "  assign dl_w = owe_w && !prog_w && tmo_hit_w;", "  assign dl_w = 1'b0;")]),
    ("ACMP-A3-deadline-owes-nothing", A, [
        (RTL, "      end else if (dl_w && dev_cmd_owned_w) begin\n        owed_r <= 1'b1;",
              "      end else if (dl_w && dev_cmd_owned_w) begin\n        owed_r <= 1'b0;")]),
    ("ACMP-A4-crc-forced-true", A, [(SHD, "                      && (rcrc_acc_r == rcrc_rx_r);", "                      && 1'b1;")]),
    ("ACMP-A5-issue20-defect", A, [
        (SHD, "                   && (nvm_err_cause_i != CAUSE_UNFRAMED_C);",
              "                   && 1'b0;"),
        (SHD, "                         && (nvm_err_cause_i == CAUSE_UNFRAMED_C))",
              "                         )")]),
]
