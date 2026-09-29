// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probes, round 2, part C (not part of the suite); run with
// --probe-r2c after probe_r2.hpp. Printed, never graded.
// C1 the aggregate bound landing on a grant: every grant withheld TMO - 200
//    cycles, and near the bound the grant is forced at clock AGG - 1 + d
//    (d = -3..3). Per d: the terminal clock and cause, whether the NVM
//    arbiter drained an abandoned READ, and whether a later SET's record is
//    written (the arbiter is not wedged by an orphaned grant).
// C2 the aggregate expiring DURING a roll-back: erased device, every grant
//    withheld TMO - 200 cycles (the bound falls in pass 1); a device error
//    is planted on the pass-1 READ requested at clock AGG - k, its grant
//    forced then, so the roll-back straddles the bound. Terminal, cause.
struct ProbeR2C {
  H& h;
  const std::vector<uint8_t>& image;
  const std::vector<ImgEnt>& ents;
  ProbeR2C(H& tally, const std::vector<uint8_t>& img, const std::vector<ImgEnt>& e)
      : h(tally), image(img), ents(e) {}
  static constexpr long TMO = D3RestorePhase::RS_TMO;
  static constexpr long AGG = D3RestorePhase::AGG;

  void c1(long dd) {
    D3RestorePhase r{h, image, ents};
    r.fresh();
    r.seed_every_record();
    r.x.nv_gnt_every = static_cast<int>(TMO - 200);
    long done = -1, closed = -1, forced_at = -1;
    bool drain_seen = false;
    r.x.d->restore_go_i = 1;
    for (long c = 0; c < AGG + 4 * TMO; ++c) {
      if (c == 5) r.x.d->restore_go_i = 0;
      if (c == AGG - 1 + dd - 1 && forced_at < 0) {   // grant in the next step
        r.x.nv_gnt_hold = 0;
        r.x.nv_gnt_seen = true;
        forced_at = c + 1;
      }
      r.x.step();
      drain_seen = drain_seen || r.x.d->dbg_nvm_drain_o;
      if (done < 0 && r.x.d->restore_done_o) done = c;
      if (closed < 0 && r.x.d->restore_closed_o) closed = c;
      if ((done >= 0 || closed >= 0) && c > std::max(done, closed) + 100) break;
    }
    r.x.nv_gnt_every = 0;
    const unsigned cause = r.x.d->rs_cause_o;
    for (long c = 0; c < TMO; ++c) r.x.step();
    const size_t ops0 = r.x.nvm_ops.size();
    const bool set = r.ok(AEM_SET_STREAM_INFO, D3ServicePhase::pl_ptof(0, 4242420 + dd));
    for (long c = 0; c < 2 * D3RestorePhase::WINDOW; ++c) r.x.step();
    int writes = 0;
    for (size_t i = ops0; i < r.x.nvm_ops.size(); i++)
      writes += r.x.nvm_ops[i].op == 1 && r.x.nvm_ops[i].region == 0x50;
    const bool persisted = std::equal(r.x.nv_mem[0x50].begin(), r.x.nv_mem[0x50].begin() + 12,
                                      d3_record(0x50, 4242420 + dd, 4).begin());
    printf("PROBE C1 d=%+ld: grant forced at step %ld; done at clock %ld closed %ld "
           "(bound %ld) cause %u; drain seen %d; later SET ok %d, writes %d, "
           "persisted %d\n", dd, forced_at, done >= 0 ? done + 1 : -1,
           closed >= 0 ? closed + 1 : -1, AGG, cause, drain_seen ? 1 : 0,
           set ? 1 : 0, writes, persisted ? 1 : 0);
  }
  void c2(long k) {
    D3RestorePhase r{h, image, ents};
    r.fresh();
    r.x.nv_gnt_every = static_cast<int>(TMO - 200);
    long done = -1, closed = -1, planted = -1, rb_at = -1;
    r.x.d->restore_go_i = 1;
    for (long c = 0; c < AGG + 4 * TMO; ++c) {
      if (c == 5) r.x.d->restore_go_i = 0;
      if (planted < 0 && c >= AGG - k && r.x.d->nvm_dev_req_o && r.x.nv_st == H::NvState::NV_IDLE) {
        r.x.nv_rd_region = r.x.d->nvm_dev_region_o;
        r.x.nv_rd_nth = 1;
        r.x.nv_rd_after = 0;
        r.x.nv_rd_silent = false;
        r.x.nv_rd_seen = 0;
        r.x.nv_gnt_hold = 0;
        r.x.nv_gnt_seen = true;
        planted = c;
      }
      r.x.step();
      if (rb_at < 0 && r.x.d->dbg_d3_rb_rst_o) rb_at = c;
      if (done < 0 && r.x.d->restore_done_o) done = c;
      if (closed < 0 && r.x.d->restore_closed_o) closed = c;
      if ((done >= 0 || closed >= 0) && c > std::max(done, closed) + 100) break;
    }
    r.x.nv_gnt_every = 0;
    r.x.nv_rd_region = -1;
    printf("PROBE C2 k=%ld: error planted at %ld, roll-back strobe from %ld; done at "
           "clock %ld, closed at clock %ld (bound %ld); fail %u cause %u rb %u\n",
           k, planted, rb_at, done >= 0 ? done + 1 : -1, closed >= 0 ? closed + 1 : -1,
           AGG, unsigned(r.x.d->restore_fail_o), unsigned(r.x.d->rs_cause_o),
           unsigned(r.x.d->restore_rb_o));
  }
  void run() {
    for (long dd = -3; dd <= 3; ++dd) c1(dd);
    c2(300);
    c2(3000);
  }
};
