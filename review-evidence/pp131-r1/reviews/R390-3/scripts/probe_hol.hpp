// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe (not part of the suite): does a held AECP dispatch queue
// stall the shared ingress (normalizer -> dispatch) and so block ACMP
// listener work after the S4 release? Appended to a disposable copy of
// tb/pp_top/d3_phases.hpp; run with --probe-hol.
struct ProbeHol {
  H& h;
  const milan::tb::Model<Vpp_top_wrap> model;
  H x;
  const std::vector<uint8_t>& image;
  ProbeHol(H& tally, const std::vector<uint8_t>& img)
      : h(tally), x(model.get()), image(img) {}

  static std::vector<uint8_t> getrx(uint16_t seq) {
    return acmp_frame(CTLR_MAC, 10, 0, 0, CTLR_EID, 0, EID, 0, 0, 0, 0, seq,
                      0, 0);
  }
  void boot(const std::vector<uint8_t>& dram, long cycles) {
    x.dram = dram;
    x.dram_silent = false;
    x.erase_nvm();
    x.reset();
    x.q_aecp.clear(); x.q_acmp.clear();
    x.d->restore_go_i = 1;
    for (long c = 0; c < cycles; ++c) {
      if (c == 5) x.d->restore_go_i = 0;
      x.step();
    }
    x.d->restore_go_i = 0;
  }
  void flood(const char* tag) {
    printf("PROBE %s: done %u closed %u released %u own %u\n", tag,
           unsigned(x.d->dbg_d3_done_o), unsigned(x.d->dbg_d3_closed_o),
           unsigned(x.d->dbg_lsn_released_o), unsigned(x.d->dbg_d3_own_o));
    x.q_acmp.clear();
    x.feed(getrx(0x7000));
    auto r0 = x.wait_any(x.q_acmp, 50);
    printf("PROBE %s: k=0 AECP frames queued, GET_RX_STATE answered %d\n",
           tag, r0.empty() ? 0 : 1);
    for (int k = 1; k <= 10; ++k) {
      x.feed(d3_read_entity_cmd(uint16_t(0x7100 + k)));
      x.q_acmp.clear();
      x.feed(getrx(uint16_t(0x7000 + k)));
      auto r = x.wait_any(x.q_acmp, 50);
      printf("PROBE %s: k=%d AECP frames sent, GET_RX_STATE answered %d, "
             "aecp head %u, aecp responses so far %zu\n", tag, k,
             r.empty() ? 0 : 1, unsigned(x.d->dbg_aecp_head_o),
             x.q_aecp.size());
    }
    // a long wait at the end: does anything drain by time alone?
    x.q_acmp.clear();
    x.feed(getrx(0x70FF));
    auto rl = x.wait_any(x.q_acmp, 2000);
    printf("PROBE %s: after 2000 ms, GET_RX_STATE answered %d\n", tag,
           rl.empty() ? 0 : 1);
  }
  void run() {
    boot(image, 3000);                    // healthy image: COMPLETE
    flood("COMPLETE");
    std::vector<uint8_t> bad = image;
    bad[0] ^= 0xFF;                       // D3O2's unprovable image: CLOSED
    boot(bad, 12000);
    flood("CLOSED");
  }
};
