// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe R391-3 D1 (disposable, never part of the product tree).
// Included after d3_phases.hpp in a scratch copy of tb/pp_top/sim_main.cpp at
// the top's own derived deadlines (bench clock 1,000,001 Hz, no override).
// Every sink holds a saved binding and every D3 record is saved; the device
// withholds each header byte RS_TMO/8 - 400 clocks and each payload byte
// RS_TMO - 1000 clocks (probe D1's shape), so the binding walk alone
// outlasts the aggregate bound while no single wait trips its deadline.
// Arms vary what the D3 walk's image proof then meets:
//   valid   the store already holds a validated image (W_IMG proves it)
//   late    no image at reset; loaded before the go, proven by the writer's
//           own LOCATE (W_IMGLOC answers after the bound)
//   refused the image's magic flipped: the LOCATE errs (cause 7)
//   silent  no image at reset and the descriptor memory silent from the
//           release on: the LOCATE is answered by the store's own watchdog
//   lateslow as late, and from the listener's release on the device moves
//           bytes at once but withholds every grant RS_TMO - 200 clocks (the
//           ratification's just-inside device) for the D3 walk
static void r391_d1_arm(D3RestorePhase& r, const char* what, int kind) {
  auto& x = r.x;
  const long TMO = D3RestorePhase::RS_TMO, AGG = D3RestorePhase::AGG;
  x.dram = r.image;
  if (kind == 2) x.dram[0] ^= 0xFF;
  if (kind == 1 || kind == 3 || kind == 4) x.dram.clear();
  x.dram_silent = false;
  x.erase_nvm();
  r.power_cycle();
  if (kind == 1 || kind == 3 || kind == 4) {
    x.idle(2000);                        // the store finds no image at reset
    x.dram = r.image;                    // loaded before PP_CTRL[1]
  }
  r.seed_every_record();
  r.seed_every_binding();
  x.d->entity_enable_i = 1;
  x.d->link_up_i = 1;
  x.nv_hdr_every = static_cast<int>(TMO / 8 - 400);
  x.nv_byte_every = static_cast<int>(TMO - 1000);
  const bool img0 = x.d->dbg_img_valid_o;
  const size_t ops0 = x.nvm_ops.size();
  long c = 0, bound = -1, fired = -1, bind_end = -1, release = -1, term = -1;
  long bind_wd = 0, d3_wd = 0, adp_early = 0;
  bool silent_set = false;
  x.d->restore_go_i = 1;
  for (; c < (kind == 4 ? 6 * AGG : AGG + 4 * TMO); ++c) {
    if (c == 5) x.d->restore_go_i = 0;
    x.step();
    const auto* d = x.d;
    if (bound < 0 && d->dbg_d3_agg_o == uint32_t(AGG - 1)) bound = c + 2;
    if (fired < 0 && d->dbg_d3_agg_fired_o) fired = c + 1;
    if (bind_end < 0 && d->restore_cause_o != 0) bind_end = c + 1;
    if (release < 0 && d->dbg_lsn_released_o) {
      release = c + 1;
      if (kind == 3) { x.dram_silent = true; silent_set = true; }
      if (kind == 4) {
        x.nv_hdr_every = 0;
        x.nv_byte_every = 0;
        x.nv_gnt_every = static_cast<int>(TMO - 200);
      }
    }
    bind_wd = std::max(bind_wd, long(d->dbg_bind_wd_o));
    d3_wd = std::max(d3_wd, long(d->dbg_d3_wd_o));
    if (d->dbg_adp_enable_o && !(d->dbg_d3_done_o && d->dbg_lsn_released_o)) ++adp_early;
    if (term < 0 && (d->restore_done_o || d->restore_closed_o)) term = c + 1;
    if (term >= 0 && c > term + 2000) break;
  }
  const auto* d = x.d;
  int d3_reads = 0;
  for (size_t i = ops0; i < x.nvm_ops.size(); i++) {
    const auto& o = x.nvm_ops[i];
    d3_reads += (o.op == 0 || o.op == 4) && (o.region < 0x20 || o.region > 0x27);
  }
  std::printf("R391-D1 %-7s: image valid at go %u; bound clock %ld, agg_o from %ld, binding "
              "walk failed at %ld (restore_cause_o %u, bound sinks 0x%02x), listener released "
              "%ld; terminal %ld (%+ld after the bound, firmware budget %s): done %u closed %u "
              "fail %u rs_cause %u rb %u own %u adp_enable %u (early %ld); image valid %u; D3 "
              "record READs %d; longest waits binding %ld D3 %ld of %ld; drain %u%s\n",
              what, unsigned(img0), bound, fired, bind_end, unsigned(d->restore_cause_o),
              unsigned(d->acmp_bound_o & 0xFF), release, term, term - bound,
              (term >= 0 && term <= AGG + 2 * TMO) ? "met" : "EXCEEDED",
              unsigned(d->restore_done_o), unsigned(d->restore_closed_o),
              unsigned(d->restore_fail_o), unsigned(d->rs_cause_o), unsigned(d->restore_rb_o),
              unsigned(d->dbg_d3_own_o), unsigned(d->dbg_adp_enable_o), adp_early,
              unsigned(d->dbg_img_valid_o), d3_reads, bind_wd, d3_wd, TMO,
              unsigned(d->dbg_nvm_drain_o), silent_set ? " (memory silenced at release)" : "");
  x.dram_silent = false;
  x.nv_hdr_every = 0;
  x.nv_byte_every = 0;
  x.nv_gnt_every = 0;
  if (d->restore_done_o) {
    x.q_aecp.clear();
    x.feed(d3_read_entity_cmd(0xD391));
    const auto got = x.wait_any(x.q_aecp, 50);
    for (long k = 0; k < TMO; ++k) x.step();
    const size_t ops1 = x.nvm_ops.size();
    const bool set = r.ok(AEM_SET_STREAM_INFO, D3ServicePhase::pl_ptof(0, 3913913));
    for (long k = 0; k < 2 * D3RestorePhase::WINDOW; ++k) x.step();
    int writes = 0;
    for (size_t i = ops1; i < x.nvm_ops.size(); i++)
      writes += x.nvm_ops[i].op == 1 && x.nvm_ops[i].region == 0x50;
    std::printf("R391-D1 %-7s: READ_DESCRIPTOR answered byte-exact %u; later SET accepted %u, "
                "WRITEs of 0x50 %d, unflushed %u\n", what,
                unsigned(got == d3_read_entity_rsp(0xD391)), unsigned(set), writes,
                unsigned(x.d->d3_unflushed_o));
  } else {
    x.q_acmp.clear();
    x.feed(acmp_frame(CTLR_MAC, 10, 0, 0, CTLR_EID, 0, EID, 0, 0, 0, 0, 0x7391, 0, 0));
    const auto g = x.wait_frame(x.q_acmp, 50, [](const std::vector<uint8_t>& f) {
      return f.size() > 63 && (f[15] & 0x0F) == 11 && fv_u64(f, 62, 2) == 0x7391;
    });
    std::printf("R391-D1 %-7s: CLOSED; GET_RX_STATE answered %u\n", what, unsigned(!g.empty()));
  }
  x.d->entity_enable_i = 0;
  x.d->link_up_i = 0;
  x.dram = r.image;
}

static void run_r391(H& h) {
  Suite setup(h);
  setup.load_descriptor_image();
  const std::vector<uint8_t> image = h.dram;
  D3RestorePhase r{h, image, setup.image_ents};
  r391_d1_arm(r, "valid", 0);
  r391_d1_arm(r, "late", 1);
  r391_d1_arm(r, "refused", 2);
  r391_d1_arm(r, "silent", 3);
  r391_d1_arm(r, "lateslow", 4);
}
