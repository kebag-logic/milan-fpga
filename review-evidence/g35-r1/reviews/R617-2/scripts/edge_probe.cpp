// Appended to a disposable copy of the exact-head parser harness.
// Its frame builders are reused; this driver and oracle are reviewer-owned.
int main(int argc, char **argv) {
  Verilated::commandArgs(argc, argv);
  RxParserHarness h;
  h.reset_the_parser();
  auto *d = h.dut;
  int after = 0;
  auto idle = [&](int n, bool error = false) {
    d->rx_valid_i = 0; d->rx_sof_i = 0; d->rx_eof_i = 0;
    d->rx_err_i = error;
    for (int j = 0; j < n; ++j) h.tick();
  };
  auto drive = [&](const Frame &f, int flag, bool held, int gap) {
    after = 0;
    for (size_t i = 0; i < f.b.size(); ++i) {
      if (i) {
        const int before_gap = h.bank_writes;
        idle(gap, true); // invalid-cycle flags must never become bytes
        if (flag >= 0 && int(i) > flag) after += h.bank_writes - before_gap;
      }
      d->rx_valid_i = 1; d->rx_sof_i = i == 0;
      d->rx_eof_i = i + 1 == f.b.size(); d->rx_data_i = f.b[i];
      d->rx_err_i = flag >= 0 && (int(i) == flag || (held && int(i) >= flag));
      h.tick();
      if (flag >= 0 && int(i) > flag) after += bool(d->bank_we_o);
    }
  };
  auto arms = rx_err_arms();
  Frame pdrfu = arms[3].f; pdrfu.b[14] = 0x1A;
  Hdr signal; signal.mtype = 0xC; signal.seq = 0x351C;
  arms.push_back({"pdrfu", pdrfu, 6});
  arms.push_back({"signal", common(signal, 0), 7});
  arms.push_back({"ann-empty", announce_frame(0x351B, AGM, 0, ASRC, {}), 3});
  arms.push_back({"ann-path", announce_frame(0x352B, AGM, 2, ASRC,
                        {AGM, ASRC, 0x123456789ABCDEF0ull}), 3});
  Frame padded = arms[0].f;
  padded.b.resize(96, 0xA5);
  arms.push_back({"sync-padded", padded, 1});
  unsigned frames = 0;
  for (auto &a : arms) {
    unsigned count = 0;
    for (int gap : {0, 1, 3}) for (bool held : {false, true}) {
      for (size_t pos = 0; pos < a.f.b.size(); ++pos) {
        const uint16_t drops = d->drop_cnt_o;
        const int events = h.ev_count;
        drive(a.f, int(pos), held, gap);
        for (int j = 0; j < 3; ++j) { idle(1); after += bool(d->bank_we_o); }
        h.expect_eq("extended refusal drop", d->drop_cnt_o, uint16_t(drops + 1));
        h.expect_eq("extended refusal event", h.ev_count, events);
        h.expect_eq("extended refusal writes after", after, 0);
        drive(a.f, -1, false, gap); idle(3);
        h.expect_eq("extended clean successor drop", d->drop_cnt_o, uint16_t(drops + 1));
        h.expect_eq("extended clean successor event", h.ev_count, events + 1);
        h.expect_eq("extended clean successor code", h.ev_code, a.ev);
        ++count;
      }
    }
    frames += count;
    printf("INFO extended %s: %u pulse/held/gap refusals and clean controls\n", a.tag, count);
  }
  // Every error position, all sixteen ordered type pairs, no idle gap,
  // and no bank clear. Compare every type-defined word at the accepted event.
  unsigned pairs = 0;
  for (uint8_t rt : {0x0, 0x8, 0x2, 0x3}) {
    for (uint8_t ct : {0x0, 0x8, 0x2, 0x3}) {
      auto r = salted(rt, 21); auto c = salted(ct, 42);
      for (size_t pos = 0; pos < r.f.b.size(); ++pos) {
        const uint16_t drops = d->drop_cnt_o;
        const int events = h.ev_count;
        drive(r.f, int(pos), false, 0);
        drive(c.f, -1, false, 0); idle(3);
        h.expect_eq("adjacent all-pair drop", d->drop_cnt_o, uint16_t(drops + 1));
        h.expect_eq("adjacent all-pair event count", h.ev_count, events + 1);
        h.expect_eq("adjacent all-pair event code", h.ev_code, c.ev);
        h.expect_eq("adjacent all-pair event sequence", h.ev_seq, c.seq);
        for (auto [address, word] : c.words) {
          h.expect_eq("adjacent all-pair word", h.ev_bank.count(address) ? h.ev_bank[address] : 0, word);
        }
        ++pairs;
      }
    }
  }
  // Reset cancels a poisoned partial frame; the next frame is independent.
  auto partial = arms[0].f; partial.b.resize(35);
  drive(partial, 20, false, 0);
  h.reset_the_parser();
  int events = h.ev_count;
  drive(arms[0].f, -1, false, 0); idle(3);
  h.expect_eq("reset clears refusal", d->drop_cnt_o, 0);
  h.expect_eq("reset accepts clean frame", h.ev_count, events + 1);
  // A flagged runt increments once even on the prior refusal's finalize edge.
  auto refused = arms[0].f;
  drive(refused, 20, false, 0);
  d->rx_valid_i = 1; d->rx_sof_i = 1; d->rx_eof_i = 1; d->rx_err_i = 1;
  h.tick(); idle(3);
  h.expect_eq("overlapping refused EOF and error runt", d->drop_cnt_o, 2);
  // The diagnostic counter is explicitly sixteen bits and wraps modulo 65536.
  for (unsigned j = 0; j < 65536; ++j) {
    d->rx_valid_i = 1; d->rx_sof_i = 1; d->rx_eof_i = 1; d->rx_err_i = 1;
    h.tick();
  }
  idle(3);
  h.expect_eq("error runt counter wraps once", d->drop_cnt_o, 2);
  h.expect_eq("error runts never dispatch", h.ev_count, events + 1);
  printf("INFO totals: %u extended refusals, %u zero-gap type pairs, 65536 wrap runts\n", frames, pairs);
  return h.report();
}
