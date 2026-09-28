// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probes (not part of the suite), run with --probe-gaps:
// G1: a record erased (unframed) in pass 0 and framed at rest before pass 1
//     must abort (cause 5): the passes disagree record by record.
// G2: while the D3 writer backs off after a failed WRITE, AECP dispatch is
//     free: a GET sent during the backoff is answered promptly.
struct ProbeGaps {
  H& h;
  const std::vector<uint8_t>& image;
  const std::vector<ImgEnt>& ents;
  ProbeGaps(H& tally, const std::vector<uint8_t>& img, const std::vector<ImgEnt>& e)
      : h(tally), image(img), ents(e) {}

  void g1() {
    D3RestorePhase r{h, image, ents};
    r.fresh();
    r.seed(0x00, d3_record(0x00, 1, 2));          // applied before 0x50 in pass 1
    const size_t ops0 = r.x.nvm_ops.size();
    bool planted = false;
    const auto b = r.boot_with(6 * D3RestorePhase::RS_TMO, [&] {
      if (!planted && r.reads_of(ops0, 0x50) == 1 && r.x.nv_st == H::NvState::NV_IDLE) {
        r.seed(0x50, d3_record(0x50, 1500000, 4)); // framed at rest after pass 0
        planted = true;
      }
    });
    printf("PROBE G1 blank-in-pass-0 then whole-in-pass-1: planted %d done %ld "
           "fail %u cause %u rolled back %u applied %u ptof0 valid %u value %u\n",
           planted ? 1 : 0, b.done, unsigned(r.x.d->restore_fail_o),
           unsigned(r.x.d->rs_cause_o), unsigned(r.x.d->restore_rb_o),
           unsigned(r.x.d->dbg_d3_applied_o),
           unsigned(r.x.d->aecp_pt_offset_v_o & 1),
           unsigned(r.x.d->aecp_pt_offset_o.at(0)));
  }

  void g2() {
    D3ServicePhase s{h, image};
    s.power_up();
    s.x.nv_err_region = 0x50;
    s.x.nv_err_writes = 1000;
    const bool a = s.set_ok(AEM_SET_STREAM_INFO, D3ServicePhase::pl_ptof(0, 7000001));
    long c = 0;
    for (; c < 6 * D3ServicePhase::WINDOW && !s.x.d->dbg_d3_merr_o; ++c) s.x.step();
    for (int k = 0; k < 1000; ++k) s.x.step();    // inside the 50,000-cycle backoff
    const uint16_t q = 0x7777;
    s.x.q_aecp.clear();
    s.x.feed(d3_read_entity_cmd(q));
    long lat = -1;
    for (long t = 0; t < 120000 && lat < 0; ++t) {
      s.x.step();
      if (!s.x.q_aecp.empty()) lat = t;
    }
    printf("PROBE G2 SET ok %d; first failed attempt err at %ld; a READ_DESCRIPTOR "
           "sent 1000 cycles into the backoff answered after %ld cycles "
           "(own now %u)\n", a ? 1 : 0, c, lat, unsigned(s.x.d->dbg_d3_own_o));
  }
  void run() { g1(); g2(); }
};
