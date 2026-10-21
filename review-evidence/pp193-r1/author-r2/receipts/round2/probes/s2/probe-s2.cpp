// SPDX-License-Identifier: CERN-OHL-W-2.0
// Probe (issue #193): an applicant handed to a lower-index sink after the
// walk passed that sink. Includes the suite, replaces its entry point; the
// RTL is the candidate's, unedited. Prints PROBE lines and one CHECK per
// variant: the message is never lost and never sent twice; it may go one
// tx! later.
#define main original_suite_main
#include "sim_main.cpp"
#undef main

namespace {

int checks = 0;
int fails = 0;

void probe_check(bool ok, const char* what) {
  ++checks;
  if (!ok) ++fails;
  printf("%s: %s\n", ok ? "PASS" : "FAIL", what);
}

//! join_tick, then `at` clocks later a Talker Advertise registers sink r
//! on SID0; returns the SID0 words of that walk
std::string tick_with_register_at(Hn& h, int at, int r) {
  h.clear_logs();
  h.d->join_tick_i = 1;
  bool done = false;
  for (int i = 0; i < kTxopPollSteps && !done; ++i) {
    if (i == at) {
      h.d->evt_valid_i = 1; h.d->evt_msrp_i = 1; h.d->evt_attr_type_i = 1;
      h.d->evt_stream_id_i = SID0; h.d->evt_da_i = DA0; h.d->evt_vid_i = VID0;
      h.d->evt_mrp_event_i = 3; h.d->evt_fourpacked_i = 0;
      h.d->evt_acc_latency_i = 500; h.d->evt_failure_system_id_i = 0;
      h.d->evt_failure_code_i = 0;
    }
    h.step();
    done = h.d->l_txop_done_o != 0;
  }
  h.idle(2);
  printf("PROBE:   walk with sink %d registering at clock %d: SID0 '%s', app0 %s app5 %s "
         "app7 %s, decl0 %d\n", r, at, listener_words(h.l_push, SID0).c_str(),
         SN[h.l_app(0)], SN[h.l_app(5)], SN[h.l_app(7)], h.l_decl(0));
  return listener_words(h.l_push, SID0);
}

std::string next_tick(Hn& h) {
  h.clear_logs();
  h.tick();
  return listener_words(h.l_push, SID0);
}

}  // namespace

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  const milan::tb::Model<Vsrp_stream_fsms_wrap> model;
  Hn h(model.get());
  // (a) issue #193 alone: sink 5 holds the applicant (AN, its New due),
  // sink 0 a rider settled after the Advertise; sink 0's registration
  // lands after the walk passed sink 0 and before sink 5: the applicant
  // moves to sink 0 (now the owner) with no New (same type)
  for (int at = 1; at <= 6; ++at) {
    h.reset();
    h.ctl(true, 5, SID0, DA0, VID0);
    h.inject(true, 1, SID0, DA0, VID0, 3 /*JoinMt*/, 0, 500);
    h.tick();                                          // VN -> AN, New sent
    h.ctl(true, 0, SID0, DA0, VID0);
    printf("PROBE: (a) owner 5 in %s, rider 0 settled; registration at clock %d\n",
           SN[h.l_app(5)], at);
    const std::string w1 = tick_with_register_at(h, at, 0);
    const std::string w2 = next_tick(h);
    const std::string w3 = next_tick(h);
    printf("PROBE:   then '%s', '%s'\n", w2.c_str(), w3.c_str());
    // one applicant from AN: New (AN), then JoinMt (AA); the walk that
    // moves it may give it its tx! or not, never two
    const bool sent_now = (w1 == "0/2" && w2 == "3/2");
    const bool one_late = (w1.empty() && w2 == "0/2" && w3 == "3/2");
    char what[160];
    snprintf(what, sizeof what, "(a) registration at clock %d: '%s' '%s' '%s' (%s)", at,
             w1.c_str(), w2.c_str(), w3.c_str(),
             sent_now ? "in this walk" : one_late ? "one tx! later" : "other");
    probe_check(sent_now || one_late, what);
  }
  // (b) the parked form: sink 7 alone on SID0 re-binds and parks the Lv;
  // sink 0 settled on SID0, a rider; sink 0's registration lands during
  // the walk: before the walk reaches sink 7, sink 0 takes the parked
  // applicant over (no Lv); after it, the Lv has gone and the New waits
  constexpr uint64_t SIDB = 0x02AABBCCDDEE0002ull;
  constexpr uint64_t DAB  = 0x91E0F0001235ull;
  for (int at = 1; at <= 10; ++at) {
    h.reset();
    h.ctl(true, 7, SID0, DA0, VID0);
    h.inject(true, 1, SID0, DA0, VID0, 3 /*JoinMt*/, 0, 500);
    for (int k = 0; k < 3; ++k) h.tick();               // QA
    h.ctl(true, 7, SIDB, DAB, VID0);                    // parks SID0's Lv
    h.ctl(true, 0, SID0, DA0, VID0);
    printf("PROBE: (b) parker 7 in %s, rider 0 settled; registration at clock %d\n",
           SN[h.l_app(7)], at);
    const std::string w1 = tick_with_register_at(h, at, 0);
    const std::string w2 = next_tick(h);
    printf("PROBE:   then '%s'\n", w2.c_str());
    const bool merged = (w1.empty() && w2 == "0/2");
    const bool lv_first = (w1 == "5/2" && w2 == "0/2");
    char what[160];
    snprintf(what, sizeof what, "(b) registration at clock %d: '%s' '%s' (%s)", at,
             w1.c_str(), w2.c_str(),
             merged ? "taken over, no Lv" : lv_first ? "Lv sent, then New" : "other");
    probe_check(merged || lv_first, what);
  }
  // (c) the order SH16 does not take: sink 0 holds SID0 and parks it;
  // sink 1 re-binds onto SID0 while it owes its own Leave (SIDB) and
  // registers. The walk reaches sink 0's parked Lv before sink 1's own
  // Leave has gone: no sink declares SID0 yet, so the Lv goes out (#188)
  {
    constexpr uint64_t SIDQ = 0x02AABBCCDDEE0003ull;
    constexpr uint64_t DAQ  = 0x91E0F0001236ull;
    h.reset();
    h.ctl(true, 1, SIDB, DAB, VID0);
    h.ctl(true, 0, SID0, DA0, VID0);
    h.inject(true, 1, SIDB, DAB, VID0, 3 /*JoinMt*/, 0, 500);
    h.inject(true, 1, SID0, DA0, VID0, 3 /*JoinMt*/, 0, 500);
    for (int k = 0; k < 3; ++k) h.tick();
    h.ctl(true, 1, SID0, DA0, VID0);
    h.inject(true, 1, SID0, DA0, VID0, 3 /*JoinMt*/, 0, 500);
    h.ctl(true, 0, SIDQ, DAQ, VID0);
    h.clear_logs();
    h.tick();
    const std::string a = listener_words(h.l_push, SID0);
    const std::string b = listener_words(h.l_push, SIDB);
    const std::string c = next_tick(h);
    printf("PROBE: (c) parker 0, re-binder 1: first tx! SID0 '%s' SIDB '%s', then SID0 '%s', "
           "decl1 %d\n", a.c_str(), b.c_str(), c.c_str(), h.l_decl(1));
    probe_check(a == "5/2" && b == "5/2" && c == "0/2",
                "(c) the parked Lv the walk reaches first goes out; the re-binder's New "
                "follows at the next tx!");
  }
  printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
  return fails ? 1 : 0;
}
