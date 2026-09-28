// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe, round 2, part D (not part of the suite); run with
// --probe-r2d. Needs the harness knob nv_byte_every that run_probe_r2d.sh
// adds to a disposable copy of sim_main.cpp: every READ byte is withheld
// that many cycles, so each wait of each walk is answered just inside the
// per-wait deadline, byte by byte (the ruling's slow-but-live device, slow
// per byte rather than per grant as in D3R13). The port gathers a record's
// 8 header bytes before its manager sees progress, so an 8-byte READ gets
// nv_hdr_every per byte (8 x that inside one wait) and a payload READ
// nv_byte_every per byte (each byte its own wait). With the eight sinks'
// binding records saved (20-byte payloads), the binding walk runs past the
// aggregate bound. Printed, never graded.
struct ProbeR2D {
  H& h;
  const std::vector<uint8_t>& image;
  const std::vector<ImgEnt>& ents;
  ProbeR2D(H& tally, const std::vector<uint8_t>& img, const std::vector<ImgEnt>& e)
      : h(tally), image(img), ents(e) {}
  static constexpr long TMO = D3RestorePhase::RS_TMO;
  static constexpr long AGG = D3RestorePhase::AGG;

  void d1(int gap, bool seeded) {
    D3RestorePhase r{h, image, ents};
    r.fresh();
    if (seeded) {
      r.seed_every_record();
      for (int k = 0; k < 8; ++k) {
        auto b = D3RestorePhase::binding_record(0x00B0B0B0B0B0D400ULL + k,
                                                uint16_t(0x0D40 + k), CTLR_EID);
        b[3] = uint8_t(0x20 + k);
        r.seed(uint8_t(0x20 + k), D3RestorePhase::reframe(b));
      }
    }
    r.x.d->entity_enable_i = 1;
    r.x.d->link_up_i = 1;
    r.x.nv_byte_every = gap;
    r.x.nv_hdr_every = static_cast<int>(TMO / 8 - 400);
    long release = -1, done = -1, closed = -1, bdone = -1;
    long maxbw = 0, maxwd = 0;
    unsigned img_at_closed = 9;
    r.x.d->restore_go_i = 1;
    for (long c = 0; c < 4 * AGG; ++c) {
      if (c == 5) r.x.d->restore_go_i = 0;
      r.x.step();
      maxbw = std::max(maxbw, long(r.x.d->dbg_bind_wd_o));
      maxwd = std::max(maxwd, long(r.x.d->dbg_d3_wd_o));
      if (release < 0 && r.x.d->dbg_lsn_released_o) release = c;
      if (done < 0 && r.x.d->restore_done_o) done = c;
      if (closed < 0 && r.x.d->restore_closed_o) {
        closed = c;
        img_at_closed = unsigned(r.x.d->dbg_img_valid_o);
      }
      if (bdone < 0 && release >= 0 && (done >= 0 || closed >= 0)) bdone = c;
      if (bdone >= 0 && c > bdone + 100) break;
    }
    r.x.nv_byte_every = 0;
    r.x.nv_hdr_every = 0;
    int bind_reads = 0;
    for (const auto& o : r.x.nvm_ops) bind_reads += (o.op == 0 && o.region >= 0x20 && o.region < 0x28);
    printf("        binding-record READs completed: %d\n", bind_reads);
    const auto* d = r.x.d;
    printf("PROBE D1 %s, every payload READ byte withheld %d cycles, header bytes %ld: longest binding wait %ld, "
           "longest D3 wait %ld (per-wait bound %ld); listener released at clock %ld; "
           "done at clock %ld; closed at clock %ld (aggregate %ld); image valid at "
           "CLOSED %u; fail %u rs_cause %u binding cause %u\n",
           seeded ? "records saved" : "erased", gap, TMO / 8 - 400, maxbw, maxwd, TMO,
           release >= 0 ? release + 1 : -1, done >= 0 ? done + 1 : -1,
           closed >= 0 ? closed + 1 : -1, AGG, img_at_closed,
           unsigned(d->restore_fail_o), unsigned(d->rs_cause_o),
           unsigned(d->restore_cause_o));
    r.x.q_aecp.clear();
    r.x.feed(d3_read_entity_cmd(0xD1D1));
    const auto a = r.x.wait_any(r.x.q_aecp, 200);
    printf("PROBE D1: afterwards own %u, adp enable %u, a READ_DESCRIPTOR answered %d, "
           "image valid %u\n", unsigned(d->dbg_d3_own_o), unsigned(d->dbg_adp_enable_o),
           a.empty() ? 0 : 1, unsigned(d->dbg_img_valid_o));
    r.x.d->entity_enable_i = 0;
  }
  void run() {
    d1(static_cast<int>(TMO - 1000), false);  // erased: the walks stay short
    d1(static_cast<int>(TMO - 1000), true);   // saved: the binding walk runs long
  }
};
