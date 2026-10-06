// Reviewer probe: public input strobes; existing harness used only as a driver.
// Expected final states derive from the expiry-first scope ruling and Table 10-4.
#define main supplied_main
#include "sim_main.cpp"
#undef main

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  milan::tb::Model<Vsrp_stream_fsms_wrap> model;
  auto* d = model.get();
  Hn h(d);
  int checks = 0;
  int fails = 0;
  for (bool listener : {false, true}) for (bool own : {false, true})
    for (int oldv : {0, 1}) for (int newv : {0, 1})
      for (int slot = 0; slot < 8; ++slot) for (int ev = 0; ev < 8; ++ev)
        for (bool match : {false, true}) {
          h.reset();
          const int oldtype = listener ? 1 + oldv : 3;
          const int newtype = listener ? 1 + newv : 3;
          if (listener) h.ctl(true, slot, SID0, DA0, VID0);
          else h.gate(true, slot, SID0, DA0, VID0);
          h.inject(true, oldtype, SID0, DA0, VID0, 0, 2 + oldv, 500, 0x1234, 1);
          if (own) h.la_own(); else h.la_rx_lanes(1u << (oldtype - 1));
          const int aged = listener ? h.l_regst(slot) : h.t_reg(slot);
          h.clear_logs();
          d->exp_valid_i = 1;
          d->exp_slot_i = (listener ? 24 : 16) + slot;
          if (ev < 6) {
            h.inject(true, newtype, match ? SID0 : SID0 + 1, DA0, VID0,
                     ev, 2 + newv, 501, 0x5678, 2);
          } else if (ev == 6) {
            h.la_rx_lanes(match ? 1u << (oldtype - 1) : 8u);
          } else h.la_own();
          h.idle(4);
          const bool renewed = match && (ev == 0 || ev == 1 || ev == 3);
          const int want = renewed ? 1 : 0;
          const int got = listener ? h.l_regst(slot) : h.t_reg(slot);
          const auto& arms = listener ? h.l_arm : h.t_arm;
          const bool timer = renewed ? arms.size() == 1 && arms[0].cancel
            && arms[0].slot == (listener ? 24 : 16) + slot : arms.empty();
          bool payload = true;
          if (listener && renewed) {
            payload = h.l_lat(slot) == 501;
            if (newv) payload &= h.l_fcode(slot) == 2 && h.l_fbridge(slot) == 0x5678;
          }
          const bool published = listener ? h.l_tkreg(slot) == (renewed ? newtype : 0)
            : h.t_lstn(slot) == (renewed ? 2 + newv : 0)
              && bool((d->t_active_o >> slot) & 1) == renewed;
          const bool events = listener
            ? h.l_unreg[slot] == int(!renewed)
              && h.l_reg[slot] == int(renewed && oldv != newv)
              && h.l_fchg[slot] == int(renewed && oldv == 1 && newv == 1)
            : h.t_chg[slot] == int(!renewed || oldv != newv);
          CHECK(aged == 2 && got == want && timer && published && payload && events,
                "MATRIX plane=%d own=%d old=%d new=%d slot=%d ev=%d match=%d "
                "aged=%d got=%d want=%d timer=%d pub=%d payload=%d events=%d",
                listener, own, oldv, newv, slot, ev, match, aged, got, want,
                timer, published, payload, events);
        }
  printf("REVIEW_MATRIX %d checks: %d PASS, %d FAIL\n", checks, checks-fails, fails);
  return fails ? 1 : 0;
}
