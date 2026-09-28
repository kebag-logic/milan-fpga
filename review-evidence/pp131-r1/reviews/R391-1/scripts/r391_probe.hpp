// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe (disposable, never part of the product tree): does an AECP
// queue that the D3 writer holds block ACMP listener service?
// Included after d3_phases.hpp in a scratch copy of tb/pp_top/sim_main.cpp.
struct R391Probe {
  const milan::tb::Model<Vpp_top_wrap> model;
  H x;
  const std::vector<uint8_t>& image;
  explicit R391Probe(H&, const std::vector<uint8_t>& img) : x(model.get()), image(img) {}

  std::vector<uint8_t> rx_state_cmd(uint16_t seq) {
    return acmp_frame(CTLR_MAC, 10, 0, 0, CTLR_EID, 0, EID, 0, 0, 0, 0, seq, 0, 0);
  }
  //! cycles from the ACMP command's last byte to its GET_RX_STATE_RESPONSE,
  //! or -1 if none within `ms`
  long ask_rx_state(uint16_t seq, int ms) {
    x.q_acmp.clear();
    x.feed(rx_state_cmd(seq));
    const long t0 = long(x.t);
    const auto g = x.wait_frame(x.q_acmp, ms, [seq](const std::vector<uint8_t>& f) {
      return f.size() > 63 && (f[15] & 0x0F) == 11 && fv_u64(f, 62, 2) == seq;
    });
    return g.empty() ? -1 : long(x.t) - t0;
  }
  void power_up(const std::vector<uint8_t>& dram) {
    x.dram = dram;
    x.dram_silent = false;
    x.erase_nvm();
    x.reset();
    x.q_aecp.clear();
    x.q_acmp.clear();
  }
  //! restore_go_i, then `cycles`; returns the admission release cycle
  long go(long cycles, long hold_first_d3_read) {
    long rel = -1;
    bool armed = false;
    x.d->restore_go_i = 1;
    for (long c = 0; c < cycles; ++c) {
      if (c == 5) x.d->restore_go_i = 0;
      if (rel >= 0 && !armed && hold_first_d3_read > 0 && x.d->nvm_dev_req_o) {
        x.nv_gnt_hold = int(hold_first_d3_read);
        armed = true;
      }
      x.step();
      if (rel < 0 && x.d->dbg_lsn_released_o) rel = c;
      if (rel >= 0 && (hold_first_d3_read == 0 || armed) && c > rel + 20) break;
    }
    x.d->restore_go_i = 0;
    return rel;
  }

  void closed_case(int n_aecp) {
    std::vector<uint8_t> bad = image;
    bad[0] ^= 0xFF;
    power_up(bad);
    go(12000, 0);
    x.idle(12000);
    const bool closed = x.d->restore_closed_o;
    const long before = ask_rx_state(0x7100, 50);
    for (int i = 0; i < n_aecp; ++i) x.feed(d3_read_entity_cmd(uint16_t(0x7200 + i)));
    x.idle(2000);
    const long after = ask_rx_state(0x7101, 200);
    const long after2 = ask_rx_state(0x7102, 200);
    std::printf("R391-P1 CLOSED n_aecp=%d closed=%u acmp_before=%ld acmp_after=%ld "
                "acmp_after2=%ld aecp_responses=%zu\n",
                n_aecp, unsigned(closed), before, after, after2, x.q_aecp.size());
  }

  void walk_case(int n_aecp) {
    power_up(image);
    x.d->link_up_i = 1;
    const long rel = go(200000, 18000);   // D3's first read granted 18,000 late
    const long t_rel_abs = long(x.t);
    for (int i = 0; i < n_aecp; ++i) x.feed(d3_read_entity_cmd(uint16_t(0x7300 + i)));
    const long t_ask = long(x.t);
    const long lat = ask_rx_state(0x7301, 400);
    long d3_done_at = -1;
    // find when D3 finished relative to the ask (it is already done if lat is late)
    for (int c = 0; c < 60000 && !x.d->dbg_d3_done_o; ++c) x.step();
    d3_done_at = x.d->dbg_d3_done_o ? 1 : 0;
    x.idle(3000);
    const size_t aecp_answered = x.q_aecp.size();
    const long lat2 = ask_rx_state(0x7302, 200);
    std::printf("R391-P2 WALK n_aecp=%d release=%ld asked %ld cycles after the release, "
                "acmp_latency=%ld d3_done_now=%ld restore_fail=%u held_aecp_answered=%zu "
                "acmp_after_terminal=%ld\n",
                n_aecp, rel, t_ask - t_rel_abs, lat, d3_done_at,
                unsigned(x.d->restore_fail_o), aecp_answered, lat2);
  }
  void run() {
    closed_case(0);
    closed_case(3);
    closed_case(4);
    closed_case(5);
    closed_case(6);
    closed_case(8);
    walk_case(0);
    walk_case(8);
  }
};

//! P3-P5 on the suite's own restore phase helpers (a fresh model each)
static void r391_restore_probes(H& h, const std::vector<uint8_t>& image,
                                const std::vector<ImgEnt>& ents) {
  D3RestorePhase r{h, image, ents};
  auto& x = r.x;
  const long TMO = D3RestorePhase::RS_TMO;
  // P3: pass 1's header READ of 0x50 never answered (indefinitely delayed)
  {
    const auto b = r.faulted_boot(3, 0, true);
    const auto* d = x.d;
    std::printf("R391-P3 pass-1 silent read: done %ld closed %ld fail %u rb %u cause %u "
                "rows_cleared %u own %u img_valid %u\n", b.done - b.release, b.closed,
                unsigned(d->restore_fail_o), unsigned(d->restore_rb_o),
                unsigned(d->rs_cause_o), unsigned(r.rows_cleared()),
                unsigned(d->dbg_d3_own_o), unsigned(d->dbg_img_valid_o));
  }
  // P4: the integrator's format judge never answers in pass 1
  {
    r.fresh();
    r.seed(0x00, d3_record(0x00, 1, 2));
    r.seed(0x30, d3_record(0x30, H::SFMT_MAIN_C, 8));
    x.gsi_stuck = true;
    const auto b = r.boot(8 * TMO);
    x.gsi_stuck = false;
    const auto* d = x.d;
    std::printf("R391-P4 judge silent: done %ld closed %ld fail %u rb %u cause %u "
                "rows_cleared %u own %u\n", b.done - b.release, b.closed,
                unsigned(d->restore_fail_o), unsigned(d->restore_rb_o),
                unsigned(d->rs_cause_o), unsigned(r.rows_cleared()),
                unsigned(d->dbg_d3_own_o));
  }
  // P5: every D3 device READ granted just inside the per-wait deadline
  {
    r.fresh();
    r.seed(0x00, d3_record(0x00, 1, 2));
    r.seed(0x02, d3_record(0x02, 48000, 4));
    r.seed(0x0A, d3_record(0x0A, 1, 2));
    r.seed(0x50, d3_record(0x50, 1500000, 4));
    r.seed(0x51, d3_record(0x51, 1600000, 4));
    long reads = 0;
    bool prev = false;
    bool released = false;
    const auto b = r.boot_with(400 * TMO, [&] {
      released = released || x.d->dbg_lsn_released_o;
      const bool req = x.d->nvm_dev_req_o;
      if (released && req && !prev && x.nv_gnt_hold == 0) {
        x.nv_gnt_hold = int(TMO - 200);
        ++reads;
      }
      prev = req;
    });
    const long term = b.done >= 0 ? b.done : b.closed;
    std::printf("R391-P5 slow-but-inside device: %ld D3 reads each held %ld cycles; "
                "terminal %ld cycles after the release = %.1f x RS_TMO (the ratified "
                "aggregate is 50 x the per-wait candidate); fail %u cause %u\n",
                reads, TMO - 200, term - b.release, double(term - b.release) / double(TMO),
                unsigned(x.d->restore_fail_o), unsigned(x.d->rs_cause_o));
  }
}

static void run_r391(H& h) {
  Suite setup(h);
  setup.load_descriptor_image();
  const std::vector<uint8_t> image = h.dram;
  R391Probe{h, image}.run();
  r391_restore_probes(h, image, setup.image_ents);
}
