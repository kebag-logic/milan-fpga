// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe R391-2 (disposable, never part of the product tree).
// Included after d3_phases.hpp in a scratch copy of tb/pp_top/sim_main.cpp.
// P1/P2 re-run the round-1 head-of-line probes at the round-2 head and add
// the dropped-while-held counter (snapshot word 37); P1b/P1c add traffic the
// round-1 probe did not send; P3-P5 re-run the round-1 restore probes.
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
  //! a frame with no inter-frame gap after it (the next frame's first byte
  //! follows in the next cycle)
  void feed_tight(const std::vector<uint8_t>& f) {
    for (size_t i = 0; i < f.size(); i++) {
      x.d->rx_valid_i = 1;
      x.d->rx_data_i = f[i];
      x.d->rx_last_i = (i + 1 == f.size()) ? 1 : 0;
      x.step();
    }
    x.d->rx_valid_i = 0;
    x.d->rx_last_i = 0;
  }
  int answered(uint16_t seq) const {
    int n = 0;
    for (const auto& r : x.q_aecp) n += (r.size() >= 38 && fv_u64(r, 34, 2) == seq) ? 1 : 0;
    return n;
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
  bool to_closed() {
    std::vector<uint8_t> bad = image;
    bad[0] ^= 0xFF;
    power_up(bad);
    go(12000, 0);
    x.idle(12000);
    return x.d->restore_closed_o;
  }

  void closed_case(int n_aecp) {
    const bool closed = to_closed();
    const uint32_t d0 = x.snap(37);
    const long before = ask_rx_state(0x7100, 50);
    for (int i = 0; i < n_aecp; ++i) x.feed(d3_read_entity_cmd(uint16_t(0x7200 + i)));
    x.idle(2000);
    const long after = ask_rx_state(0x7101, 200);
    const long after2 = ask_rx_state(0x7102, 200);
    std::printf("R391-P1 CLOSED n_aecp=%d closed=%u acmp_before=%ld acmp_after=%ld "
                "acmp_after2=%ld aecp_responses=%zu dropped_word37=%u (from %u) own=%u\n",
                n_aecp, unsigned(closed), before, after, after2, x.q_aecp.size(),
                x.snap(37), d0, unsigned(x.d->dbg_d3_own_o));
  }

  //! CLOSED, AECP traffic the engine would drop at once when not held:
  //! responses to this entity, commands for another entity id, and AVDECC
  //! multicast commands, then a GET_RX_STATE
  void closed_mixed_case() {
    const bool closed = to_closed();
    const long before = ask_rx_state(0x7110, 50);
    std::vector<uint8_t> rd(8, 0);
    for (int i = 0; i < 3; ++i) {
      x.feed(aecp_frame(OWN_MAC, CTLR_MAC, 1, 0, EID, CTLR_EID, uint16_t(0x7400 + i),
                        AEM_READ_DESCRIPTOR, rd));
      x.feed(aecp_frame(OWN_MAC, CTLR_MAC, 0, 0, EID ^ 0x1ull, CTLR_EID,
                        uint16_t(0x7410 + i), AEM_READ_DESCRIPTOR, rd));
      x.feed(aecp_frame(0x91E0F0010000ull, CTLR_MAC, 0, 0, EID, CTLR_EID,
                        uint16_t(0x7420 + i), AEM_READ_DESCRIPTOR, rd));
    }
    x.idle(2000);
    const long after = ask_rx_state(0x7111, 200);
    std::printf("R391-P1b CLOSED mixed 9 AECP frames (3 responses, 3 other-entity, 3 "
                "multicast): closed=%u acmp_before=%ld acmp_after=%ld dropped_word37=%u\n",
                unsigned(closed), before, after, x.snap(37));
  }

  //! CLOSED, eight AECP / GET_RX_STATE pairs with no inter-frame gap at all
  void closed_tight_case() {
    const bool closed = to_closed();
    x.q_acmp.clear();
    for (int i = 0; i < 8; ++i) {
      feed_tight(d3_read_entity_cmd(uint16_t(0x7500 + i)));
      feed_tight(rx_state_cmd(uint16_t(0x7600 + i)));
    }
    x.idle(3000);
    int got = 0;
    for (int i = 0; i < 8; ++i)
      for (const auto& f : x.q_acmp)
        if (f.size() > 63 && (f[15] & 0x0F) == 11 && fv_u64(f, 62, 2) == uint64_t(0x7600 + i)) {
          ++got;
          break;
        }
    std::printf("R391-P1c CLOSED tight interleave: closed=%u GET_RX_STATE answered %d of 8, "
                "dropped_word37=%u aecp_responses=%zu\n",
                unsigned(closed), got, x.snap(37), x.q_aecp.size());
  }

  void walk_case(int n_aecp) {
    power_up(image);
    x.d->link_up_i = 1;
    const long rel = go(200000, 18000);   // D3's first read granted 18,000 late
    const long t_rel_abs = long(x.t);
    for (int i = 0; i < n_aecp; ++i) x.feed(d3_read_entity_cmd(uint16_t(0x7300 + i)));
    const long t_ask = long(x.t);
    const long lat = ask_rx_state(0x7301, 400);
    const bool walking = !x.d->dbg_d3_done_o;
    for (int c = 0; c < 60000 && !x.d->dbg_d3_done_o; ++c) x.step();
    const bool done = x.d->dbg_d3_done_o;
    x.idle(3000);
    int answered_n = 0;
    for (int i = 0; i < n_aecp; ++i) answered_n += answered(uint16_t(0x7300 + i));
    const bool first_exact = n_aecp == 0 || [&] {
      for (const auto& r : x.q_aecp)
        if (r.size() >= 38 && fv_u64(r, 34, 2) == 0x7300) return r == d3_read_entity_rsp(0x7300);
      return false;
    }();
    const long lat2 = ask_rx_state(0x7302, 200);
    std::printf("R391-P2 WALK n_aecp=%d release=%ld asked %ld cycles after the release, "
                "walking_at_ask_end=%u acmp_latency=%ld d3_done=%u restore_fail=%u "
                "held_aecp_answered=%d first_byte_exact=%u dropped_word37=%u "
                "acmp_after_terminal=%ld\n",
                n_aecp, rel, t_ask - t_rel_abs, unsigned(walking), lat, unsigned(done),
                unsigned(x.d->restore_fail_o), answered_n, unsigned(first_exact), x.snap(37),
                lat2);
  }
  void run() {
    for (const int n : {0, 3, 4, 5, 6, 8, 16}) closed_case(n);
    closed_mixed_case();
    closed_tight_case();
    for (const int n : {0, 6, 8, 16}) walk_case(n);
  }
};

//! P3-P5 on the suite's own restore phase helpers (a fresh model each)
static void r391_restore_probes(H& h, const std::vector<uint8_t>& image,
                                const std::vector<ImgEnt>& ents) {
  D3RestorePhase r{h, image, ents};
  auto& x = r.x;
  const long TMO = D3RestorePhase::RS_TMO;
  const long AGG = D3RestorePhase::AGG;
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
  // P5: every D3 device READ after the release granted 200 inside the
  // per-wait deadline (the binding walk served at once)
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
    long own_after = 0;
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
    own_after = x.d->dbg_d3_own_o;
    std::printf("R391-P5 slow-but-inside device: %ld D3 reads each held %ld cycles; "
                "terminal at clock %ld from restore_go_i (AGG %ld, RS_TMO %ld); done %ld "
                "closed %ld fail %u rb %u cause %u own_after %ld\n",
                reads, TMO - 200, term + 1, AGG, TMO, b.done, b.closed,
                unsigned(x.d->restore_fail_o), unsigned(x.d->restore_rb_o),
                unsigned(x.d->rs_cause_o), own_after);
  }
}

static void run_r391(H& h) {
  Suite setup(h);
  setup.load_descriptor_image();
  const std::vector<uint8_t> image = h.dram;
  R391Probe{h, image}.run();
  r391_restore_probes(h, image, setup.image_ents);
}
