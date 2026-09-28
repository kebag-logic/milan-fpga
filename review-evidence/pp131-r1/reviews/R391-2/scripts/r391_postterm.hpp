// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe R391-2 P7 (disposable): one boot that ends COMPLETE before
// the (overridden, small) aggregate bound, then observed past the bound.
// Run on the golden and on the agg_not_stopped_at_terminal mutant.
static void run_r391(H& h) {
  Suite setup(h);
  setup.load_descriptor_image();
  const std::vector<uint8_t> image = h.dram;
  D3RestorePhase r{h, image, setup.image_ents};
  auto& x = r.x;
  r.fresh();
  r.seed_every_record();
  long complete_at = -1;
  long c = 0;
  x.d->restore_go_i = 1;
  for (; c < 20000; ++c) {
    if (c == 5) x.d->restore_go_i = 0;
    x.step();
    if (complete_at < 0 && x.d->restore_done_o) {
      complete_at = c + 1;
      std::printf("R391-P7 at clock %ld: done %u fail %u cause %u rb %u applied %u "
                  "cfg_valid %u rate_valid %u ws %u\n", c + 1, unsigned(x.d->restore_done_o),
                  unsigned(x.d->restore_fail_o), unsigned(x.d->rs_cause_o),
                  unsigned(x.d->restore_rb_o), unsigned(x.d->dbg_d3_applied_o),
                  unsigned(x.d->dbg_dyn_cfg_v_o), unsigned(x.d->dbg_dyn_rate_v_o),
                  unsigned(x.d->dbg_r391_ws_o));
    }
  }
  std::printf("R391-P7 at clock %ld (bound %ld): done %u fail %u cause %u rb %u applied %u "
              "cfg_valid %u rate_valid %u rows_cleared %u ws %u own %u\n", c, R391_AGG_VALUE_L,
              unsigned(x.d->restore_done_o), unsigned(x.d->restore_fail_o),
              unsigned(x.d->rs_cause_o), unsigned(x.d->restore_rb_o),
              unsigned(x.d->dbg_d3_applied_o), unsigned(x.d->dbg_dyn_cfg_v_o),
              unsigned(x.d->dbg_dyn_rate_v_o), unsigned(r.rows_cleared()),
              unsigned(x.d->dbg_r391_ws_o), unsigned(x.d->dbg_d3_own_o));
}
