// SPDX-License-Identifier: CERN-OHL-W-2.0
// Issue #193 with #188: a pending Leave must share identity with a new declarer.
#define main original_suite_main
#include "sim_main.cpp"
#undef main

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  const milan::tb::Model<Vsrp_stream_fsms_wrap> model;
  Hn h(model.get());
  int fails = 0;
  for (int old = 0; old < 2; ++old) {
    const int fresh = 1-old;
    h.reset();
    h.ctl(true, old, SID0, DA0, VID0);
    h.inject(true, 1, SID0, DA0, VID0, 3, 0, 500);
    for (int n = 0; n < 4; ++n) h.tick();
    if (h.l_app(old) != QA) return 2;
    h.ctl(false, old, SID0, DA0, VID0);
    h.ctl(true, old, SID0+1, DA0+1, VID0);
    if (h.l_app(old) != LA) return 3;
    h.ctl(true, fresh, SID0, DA0, VID0);
    h.inject(true, 1, SID0, DA0, VID0, 3, 0, 500);
    if (h.l_decl(fresh) != 2 || h.l_tkreg(fresh) != 1) return 4;
    h.clear_logs();
    if (!h.tick()) return 5;
    int count = 0, leaves = 0;
    bool peer_registered = true;
    printf("old_sink=%d current_sink=%d current_decl=%d\n",old,fresh,h.l_decl(fresh));
    for (const auto& p : h.l_push) {
      uint64_t sid = 0;
      for (int i=0;i<8;++i) sid = (sid<<8)|p.val[i];
      if (sid != SID0) continue;
      ++count;
      if (p.code == 0 || p.code == 1 || p.code == 3) peer_registered = true;
      if (p.code == 5) {++leaves; peer_registered = false;}
      printf("  encoder_event stream=%016llx event=%u fourpacked=%u peer_IN=%d\n",
             static_cast<unsigned long long>(sid),p.code,p.fp,peer_registered);
    }
    const bool pass = count == 1 && leaves == 0 && peer_registered;
    printf("%s: one applicant for a reoccupied parked value: count=%d leaves=%d peer_IN=%d\n",
           pass?"PASS":"FAIL",count,leaves,peer_registered);
    fails += !pass;
  }
  printf("2 checks: %d PASS, %d FAIL\n",2-fails,fails);
  return fails ? 1 : 0;
}
