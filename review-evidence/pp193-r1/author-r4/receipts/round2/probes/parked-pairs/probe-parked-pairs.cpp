// SPDX-License-Identifier: CERN-OHL-W-2.0
// Probe (issue #193 with #188): a parked Leave's group under coincident
// events. Includes the suite, replaces its entry point; the RTL is the
// candidate's, unedited. Each CHECK requires at most one Listener value
// for the stream per tx! and a final declaration; PROBE lines record the
// words per tick.
#define main original_suite_main
#include "sim_main.cpp"
#undef main

namespace {

int checks = 0;
int fails = 0;
constexpr uint64_t SIDB = 0x02AABBCCDDEE0002ull;
constexpr uint64_t DAB  = 0x91E0F0001235ull;
constexpr uint64_t SIDC = 0x02AABBCCDDEE0003ull;
constexpr uint64_t DAC  = 0x91E0F0001236ull;

int values(const std::vector<Push>& pushes) {
  int n = 0;
  for (const Push& p : pushes) {
    uint64_t got = 0;
    for (int i = 0; i < 8; ++i) got = (got << 8) | p.val[i];
    if (p.type == 3 && got == SID0) ++n;
  }
  return n;
}

void park(Hn& h, int parker) {
  h.reset();
  h.ctl(true, parker, SID0, DA0, VID0);
  h.inject(true, 1, SID0, DA0, VID0, 3 /*JoinMt*/, 0, 500);
  for (int k = 0; k < 3; ++k) h.tick();
  h.ctl(true, parker, SIDB, DAB, VID0);
}

void set_register(Hn& h) {
  h.d->evt_valid_i = 1; h.d->evt_msrp_i = 1; h.d->evt_attr_type_i = 1;
  h.d->evt_stream_id_i = SID0; h.d->evt_da_i = DA0; h.d->evt_vid_i = VID0;
  h.d->evt_mrp_event_i = 3; h.d->evt_fourpacked_i = 0;
  h.d->evt_acc_latency_i = 500; h.d->evt_failure_system_id_i = 0;
  h.d->evt_failure_code_i = 0;
}

//! the walk already run (its pushes logged), then three ticks; checks one
//! value per tick
bool ticks_one_value(Hn& h, std::string& words) {
  bool one = values(h.l_push) <= 1;
  words = listener_words(h.l_push, SID0);
  for (int k = 0; k < 3; ++k) {
    h.clear_logs();
    h.tick();
    one = one && values(h.l_push) <= 1;
    words += " | " + listener_words(h.l_push, SID0);
  }
  return one;
}

void check(bool ok, const std::string& what) {
  ++checks;
  if (!ok) ++fails;
  printf("%s: %s\n", ok ? "PASS" : "FAIL", what.c_str());
}

}  // namespace

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  const milan::tb::Model<Vsrp_stream_fsms_wrap> model;
  Hn h(model.get());
  Vsrp_stream_fsms_wrap* d = model.get();
  // (1) the joiner's registration in one clock with a periodic!, a
  // received Listener LeaveAll and/or the join tick (offset: the join tick
  // a clock before or after)
  for (int parker = 0; parker < 2; ++parker)
    for (int broadcast = 0; broadcast < 4; ++broadcast)
      for (int offset = -1; offset <= 1; ++offset) {
        const int joiner = 1 - parker;
        park(h, parker);
        h.ctl(true, joiner, SID0, DA0, VID0);
        h.clear_logs();
        if (offset < 0) { d->join_tick_i = 1; h.step(); }
        set_register(h);
        d->periodic_tick_i = (broadcast & 1) != 0;
        d->leaveall_rx_i = (broadcast & 2) ? kLaListener : 0;
        if (offset == 0) d->join_tick_i = 1;
        h.step();
        if (offset > 0) { d->join_tick_i = 1; h.step(); }
        h.idle(60);
        std::string words;
        const bool one = ticks_one_value(h, words);
        char what[200];
        snprintf(what, sizeof what, "(1) parker %d joiner %d broadcast %d join offset %d: "
                 "'%s', decl %d", parker, joiner, broadcast, offset, words.c_str(),
                 h.l_decl(joiner));
        check(one && h.l_decl(joiner) == 2, what);
        printf("PROBE: %s Lv %s\n", what,
               words.find("5/2") == std::string::npos ? "none" : "sent");
      }
  // (2) the parked sink re-binds again while the joiner, on the stream,
  // does not declare: the applicant goes to the joiner, which sends the Lv
  // once; then the joiner declares: one New
  for (int parker = 0; parker < 2; ++parker) {
    const int joiner = 1 - parker;
    park(h, parker);
    h.ctl(true, joiner, SID0, DA0, VID0);
    h.ctl(true, parker, SIDC, DAC, VID0);
    const int app_j = h.l_app(joiner);
    const int app_p = h.l_app(parker);
    h.clear_logs();
    h.tick();
    const std::string a = listener_words(h.l_push, SID0);
    h.inject(true, 1, SID0, DA0, VID0, 3 /*JoinMt*/, 0, 500);
    h.clear_logs();
    h.tick();
    const std::string b = listener_words(h.l_push, SID0);
    char what[200];
    snprintf(what, sizeof what, "(2) parker %d re-binds again, joiner %d holds %s (parker %s): "
             "'%s' then '%s'", parker, joiner, SN[app_j], SN[app_p], a.c_str(), b.c_str());
    check(app_j == LA && app_p == VO && a == "5/2" && b == "0/2", what);
  }
  // (3) the joiner, a rider of the parked group, unbinds (A8) before the
  // tx!: the parked Lv goes out once
  for (int parker = 0; parker < 2; ++parker) {
    const int joiner = 1 - parker;
    park(h, parker);
    h.ctl(true, joiner, SID0, DA0, VID0);
    h.ctl(false, joiner, SID0, DA0, VID0);
    h.clear_logs();
    h.tick();
    const std::string a = listener_words(h.l_push, SID0);
    char what[200];
    snprintf(what, sizeof what, "(3) parker %d, joiner %d unbinds first: '%s'", parker, joiner,
             a.c_str());
    check(a == "5/2", what);
  }
  // (4) the joiner declares, then its talker withdraws before the tx!:
  // VN + Lv! is LA, one Lv
  for (int parker = 0; parker < 2; ++parker) {
    const int joiner = 1 - parker;
    park(h, parker);
    h.ctl(true, joiner, SID0, DA0, VID0);
    h.inject(true, 1, SID0, DA0, VID0, 3 /*JoinMt*/, 0, 500);
    h.inject(true, 1, SID0, DA0, VID0, 5 /*Lv*/, 0, 500);
    h.clear_logs();
    h.tick();
    const std::string a = listener_words(h.l_push, SID0);
    h.clear_logs();
    h.tick();
    const std::string b = listener_words(h.l_push, SID0);
    char what[200];
    snprintf(what, sizeof what, "(4) parker %d, joiner %d declares and withdraws: '%s' then "
             "'%s', decl %d", parker, joiner, a.c_str(), b.c_str(), h.l_decl(joiner));
    check(a == "5/2" && b.empty() && h.l_decl(joiner) == 0, what);
  }
  // (5) an LO parked applicant (owes an Empty): the joiner declares: LO +
  // New! is VN, one New and no Empty
  for (int parker = 0; parker < 2; ++parker) {
    const int joiner = 1 - parker;
    h.reset();
    h.ctl(true, parker, SID0, DA0, VID0);
    h.inject(true, 3, SID0, 0, 0, 5 /*rLv*/, 2);       // VO + rLv! is LO
    h.ctl(true, parker, SIDB, DAB, VID0);               // parks the Empty
    const int app_p = h.l_app(parker);
    h.ctl(true, joiner, SID0, DA0, VID0);
    h.inject(true, 1, SID0, DA0, VID0, 3 /*JoinMt*/, 0, 500);
    h.clear_logs();
    h.tick();
    const std::string a = listener_words(h.l_push, SID0);
    char what[200];
    snprintf(what, sizeof what, "(5) LO parked by %d (%s), joiner %d declares: '%s'", parker,
             SN[app_p], joiner, a.c_str());
    check(app_p == LO && a == "0/2", what);
  }
  printf("%d checks: %d PASS, %d FAIL\n", checks, checks - fails, fails);
  return fails ? 1 : 0;
}
