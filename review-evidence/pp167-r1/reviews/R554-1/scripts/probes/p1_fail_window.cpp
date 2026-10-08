// Probe P1 (reviewer, disposable). Inserted into a private copy of
// tb/aecp_notify/sim_main.cpp as a Harness member. SC1's setup with the
// expired row 0 and the commanding row 1; a failure report for owner 1 is
// presented at offset `fail_at` cycles after the coincidence cycle (0 = the
// coincidence cycle itself). Reports the cancellations, the registry count
// and any DEREGISTER addressed to the commanding controller.
void Harness::probe_fail_window(int fail_at) {
  warm_reset();
  d->rx_cmd_valid_i = 0;
  d->ca_ready_i = 1;
  d->uns_done_i = 1;
  d->prng_draw_busy_i = 1;
  const unsigned expired = 0;
  const std::array<uint64_t, N_CTRL> eids = {0x1111000000000001ull, EID_C};
  const std::array<uint64_t, N_CTRL> macs = {0x020000000001ull, MAC_C};
  bool setup = true;
  for (unsigned row = 0; row < N_CTRL; ++row) {
    setup &= registers(eids[row], macs[row], row == expired);
    setup &= draws();
    expire(REGMON_BASE + N_CTRL + row, OWN_MON | row);
    bool probe = false;
    for (int c = 0; c < PROBE_WAIT_CYCLES; ++c) {
      d->clk_i = 0; d->eval();
      if (d->ca_valid_o) { probe = d->ca_owner_o == row; tick(); break; }
      tick();
    }
    setup &= probe;
  }
  expire(REGMON_BASE + expired, OWN_TL | expired);
  std::array<unsigned, N_CTRL> cancels = {};
  int met_at = -1;
  int cancel1_at = -1;
  unsigned dereg_live = 0;
  for (int c = 0; c < 400; ++c) {
    d->rx_cmd_valid_i = 0;
    d->ca_fail_valid_i = 0;
    d->clk_i = 0; d->eval();
    if (met_at < 0 && d->ca_cancel_valid_o && d->ca_cancel_owner_o == expired) {
      met_at = c;
      d->rx_cmd_eid_i = eids[1];
      d->rx_cmd_mac_i = macs[1];
      d->rx_cmd_valid_i = 1;
      d->eval();
    }
    if (met_at >= 0 && c == met_at + fail_at) {
      d->ca_fail_valid_i = 1;
      d->ca_fail_owner_i = 1;
      d->eval();
    }
    if (d->ca_cancel_valid_o && d->ca_cancel_owner_o < N_CTRL) {
      ++cancels[d->ca_cancel_owner_o];
      if (d->ca_cancel_owner_o == 1 && cancel1_at < 0) cancel1_at = c - met_at;
    }
    if (d->uns_valid_o && d->uns_kind_o == KIND_DEREG
        && static_cast<uint64_t>(d->uns_mac_o) == macs[1]) ++dereg_live;
    tick();
  }
  d->rx_cmd_valid_i = 0;
  d->ca_fail_valid_i = 0;
  printf("[probe P1] fail_at=%d setup=%d met=%d cancels={%u,%u} owner1_cancel_offset=%d "
         "registry_count=%u dereg_cycles_to_commanding_controller=%u\n",
         fail_at, int(setup), int(met_at >= 0), cancels[0], cancels[1], cancel1_at,
         unsigned(d->dbg_reg_cnt_o), dereg_live);
}
