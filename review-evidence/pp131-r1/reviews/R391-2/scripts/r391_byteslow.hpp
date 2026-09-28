// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe R391-2 P8 (disposable): a device that answers EVERY wait of
// the walks inside the per-wait deadline, at the top's own derived deadlines
// (no override). The probe copy's device model withholds each READ byte:
// nv_hdr_gap cycles for the 8 header bytes (the port gathers the header
// before the walk sees progress, so 8 x gap stays inside one deadline) and
// nv_byte_gap cycles for each payload byte (each one the walk's own wait).
// Every sink holds a saved binding. Case A slows both walks from
// restore_go_i; case B slows only the D3 walk (after the listener's release).
static void r391_byteslow_case(D3RestorePhase& r, bool from_go) {
  auto& x = r.x;
  const long TMO = D3RestorePhase::RS_TMO, AGG = D3RestorePhase::AGG;
  r.fresh();
  for (uint8_t k = 0; k < 8; ++k) {
    const auto rec = Suite::nv_record(uint8_t(0x20 + k), 0x00B0B0B0B0B00000ULL + k,
                                      uint16_t(0x0B00 + k), CTLR_EID);
    std::copy(rec.begin(), rec.end(), x.nv_mem[0x20 + k].begin());
  }
  long rel = -1, closed = -1, done = -1, bind_wd = 0, d3_wd = 0;
  bool slowed = false;
  x.d->restore_go_i = 1;
  long c = 0;
  for (; c < 6 * AGG; ++c) {
    if (c == 5) x.d->restore_go_i = 0;
    if (!slowed && (from_go || rel >= 0)) {
      x.nv_hdr_gap = int((TMO - 400) / 8);
      x.nv_byte_gap = int(TMO - 200);
      slowed = true;
    }
    x.step();
    bind_wd = std::max(bind_wd, long(x.d->dbg_bind_wd_o));
    d3_wd = std::max(d3_wd, long(x.d->dbg_d3_wd_o));
    if (rel < 0 && x.d->dbg_lsn_released_o) rel = c + 1;
    if (closed < 0 && x.d->restore_closed_o) closed = c + 1;
    if (done < 0 && x.d->restore_done_o) done = c + 1;
    if (done >= 0 && c > done + 1000) break;
  }
  std::printf("R391-P8 %s: listener released at %ld; D3 CLOSED at %ld, restore_done at %ld "
              "(AGG %ld, RS_TMO %ld); after %ld clocks: fail %u cause %u closed %u done %u "
              "own %u adp_enable %u; longest binding wait %ld, longest D3 wait %ld\n",
              from_go ? "A both walks slowed" : "B D3 walk slowed", rel, closed, done, AGG, TMO,
              c, unsigned(x.d->restore_fail_o), unsigned(x.d->rs_cause_o),
              unsigned(x.d->restore_closed_o), unsigned(x.d->restore_done_o),
              unsigned(x.d->dbg_d3_own_o), unsigned(x.d->dbg_adp_enable_o), bind_wd, d3_wd);
  x.nv_hdr_gap = 0;
  x.nv_byte_gap = 0;
}
static void run_r391(H& h) {
  Suite setup(h);
  setup.load_descriptor_image();
  const std::vector<uint8_t> image = h.dram;
  D3RestorePhase r{h, image, setup.image_ents};
  r.x.d->entity_enable_i = 1;
  r391_byteslow_case(r, true);
  r.x.d->entity_enable_i = 1;
  r391_byteslow_case(r, false);
}
