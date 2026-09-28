// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe (not part of the suite): during a D3 walk slowed inside
// its per-wait deadline, after the S4 release, is a GET_RX_STATE answered
// before the D3 terminal (contract 8.1: ACMP waits for S4 only), with and
// without AECP commands queued ahead of it? Run with --probe-hol-restore.
struct ProbeHolRestore {
  H& h;
  const milan::tb::Model<Vpp_top_wrap> model;
  H x;
  const std::vector<uint8_t>& image;
  ProbeHolRestore(H& tally, const std::vector<uint8_t>& img)
      : h(tally), x(model.get()), image(img) {}

  void one(int n_aecp) {
    x.dram = image;
    x.dram_silent = false;
    x.erase_nvm();
    x.reset();
    x.q_aecp.clear(); x.q_acmp.clear();
    x.d->restore_go_i = 1;
    long c = 0;
    for (; c < 200000 && !x.d->dbg_lsn_released_o; ++c) {
      if (c == 5) x.d->restore_go_i = 0;
      x.step();
    }
    x.d->restore_go_i = 0;
    x.nv_gnt_hold = 15000;              // the D3 walk's next grant waits
    const long rel = c;
    for (int k = 0; k < n_aecp; ++k) {
      x.feed(d3_read_entity_cmd(uint16_t(0x7200 + k)));
    }
    x.q_acmp.clear();
    x.feed(ProbeHol::getrx(0x7300));
    long ans = -1, done = -1;
    for (long t = 0; t < 400000 && (ans < 0 || done < 0); ++t) {
      x.step();
      if (ans < 0 && !x.q_acmp.empty()) ans = t;
      if (done < 0 && x.d->dbg_d3_done_o) done = t;
    }
    printf("PROBE-R n_aecp=%d: released at %ld; after the GET was fed: "
           "GET_RX_STATE answered at %ld, D3 terminal at %ld (%s)\n",
           n_aecp, rel, ans, done,
           ans < 0 ? "never answered"
                   : (ans < done ? "answered before the D3 terminal"
                                 : "answered only after the D3 terminal"));
  }
  void run() { one(0); one(2); one(6); }
};
