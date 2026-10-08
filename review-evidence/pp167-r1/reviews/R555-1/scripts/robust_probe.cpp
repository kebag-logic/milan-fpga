void Harness::cancel_collision() {
  unsigned scenarios = 0;
  for (unsigned expired = 0; expired < N_CTRL; ++expired) {
    for (unsigned command = 0; command < N_CTRL; ++command) {
      for (unsigned mode = 0; mode < 3; ++mode) {
        initialize_inputs();
        std::array<uint64_t, N_CTRL> eids{}, macs{};
        bool exact = true;
        for (unsigned row = 0; row < N_CTRL; ++row) {
          eids[row] = 0x1000000000000000ull + row;
          macs[row] = 0x020000000000ull + row;
          exact &= registers(eids[row], macs[row], row == expired);
          exact &= draws();
          expire(REGMON_BASE + N_CTRL + row, OWN_MON | row);
          bool found = false;
          for (unsigned c = 0; c < 64; ++c) {
            d->clk_i = 0; d->eval();
            if (d->ca_valid_o) {
              found = d->ca_owner_o == row && d->ca_ctlr_eid_o == eids[row]
                      && static_cast<uint64_t>(d->ca_mac_o) == macs[row];
              tick(); break;
            }
            tick();
          }
          exact &= found;
        }
        expire(REGMON_BASE + expired, OWN_TL | expired);
        std::vector<unsigned> owners, cycles;
        int collision = -1;
        bool targeted = false;
        for (unsigned c = 0; c < 128; ++c) {
          d->rx_cmd_valid_i = 0;
          d->clk_i = 0; d->eval();
          if (collision < 0 && d->ca_cancel_valid_o
              && d->ca_cancel_owner_o == expired) collision = static_cast<int>(c);
          if (collision >= 0) {
            const unsigned age = c - static_cast<unsigned>(collision);
            if (age < (mode == 1 ? 3u : 1u)) {
              d->rx_cmd_eid_i = eids[command];
              d->rx_cmd_mac_i = macs[command];
              d->rx_cmd_valid_i = 1;
            }
            d->eval();
          }
          if (d->ca_cancel_valid_o) {
            owners.push_back(d->ca_cancel_owner_o); cycles.push_back(c);
          }
          if (d->uns_valid_o) {
            const bool hit = d->uns_kind_o == KIND_DEREG
                          && static_cast<uint64_t>(d->uns_mac_o) == macs[expired];
            targeted |= hit; exact &= hit;
          }
          tick();
          if (mode == 2 && collision >= 0) {
            d->rx_cmd_valid_i = 0;
            warm_reset();
            for (unsigned j = 0; j < 32; ++j) {
              d->clk_i = 0; d->eval();
              exact &= !d->ca_cancel_valid_o && d->dbg_reg_cnt_o == 0;
              tick();
            }
            break;
          }
        }
        d->rx_cmd_valid_i = 0;
        exact &= collision >= 0 && !owners.empty() && owners[0] == expired;
        if (mode == 2) exact &= owners.size() == 1;
        else {
          exact &= targeted && d->dbg_reg_cnt_o == N_CTRL - 1;
          if (command == expired) exact &= owners.size() == 1;
          else exact &= owners.size() == 2 && owners[1] == command
                        && cycles[1] == cycles[0] + 1;
        }
        ++scenarios;
        CHECK(exact, "RP1 expired=%u command=%u mode=%u: ordered unique cancellation, registry and reset", expired, command, mode);
      }
    }
  }
  printf("RP1: %u scenarios, %u controller rows, distinct/same owner, command held 1/3 clocks, pending reset\n", scenarios, N_CTRL);
}
