// ==== PS. a Talker registered before the settle (issue #212) =============
// (802.1Q-2022 10.7 and 10.7.8: a registrar's state does not depend on when
// the application became interested in the attribute; Milan v1.2 5.3.8.5
// and 5.5.3.5.18 step 4: a settled sink with a matching Talker registered
// declares at once.) The listener registers every Talker Advertise/Failed
// value of the port, kPortRegs of them at most, and a settle on one starts
// its sink's registrar in that registrar's state. Every expectation is the
// suite's Table 10-3/10-4 model, with Δ13 and T-MRP-LEAVE (LEAVE_MS).
constexpr uint64_t SIDF  = 0x02AABBCCDDEE0005ull;   // a Talker Failed stream
constexpr uint64_t DAF   = 0x91E0F0001238ull;
constexpr uint64_t SYSF  = 0x0011223344556677ull;   // its FailureInformation
constexpr uint8_t  FCODE = 9;
constexpr int      kLsSlot = 24;                    // sink 0's leave slot
constexpr int      R_MT = 0;
constexpr int      R_IN = 1;
constexpr int      R_LV = 2;

//! the Talker Failed of SIDF, as the decoder presents a received one
void SrpStreamFsmsSuite::inject_failed(uint8_t ev) {
  h.inject(true, 2, SIDF, DAF, VID0, ev, 0, 888, SYSF, FCODE);
}

//! acceptance 1: a Talker Advertise or Failed registered on the port before
//! the settle is applied at the settle, and the first tx! declares New
void SrpStreamFsmsSuite::a_talker_registered_before_the_settle_is_applied_at_the_settle() {
  const int sN = app_msg(VN, false, false);
  h.reset();
  h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
  const bool before = h.l_reg[0] == 0 && h.l_tkreg(0) == 0;
  h.clear_logs();
  h.ctl(true, 0, SID0, DA0, VID0);
  CHECK(before && h.l_reg[0] == 1 && h.l_unreg[0] == 0 && h.l_tkreg(0) == 1
        && h.l_regst(0) == R_IN && h.l_lat(0) == 777 && h.l_arm.empty(),
        "PS1: a Talker Advertise registered before the settle registers at the "
        "settle: one EVT_TK_REGISTERED, ADVERTISE, IN, its latency, no timer op "
        "(before %d, reg %d unreg %d, tk %d, state %d, lat %u, %zu timer ops)",
        before, h.l_reg[0], h.l_unreg[0], h.l_tkreg(0), h.l_regst(0), h.l_lat(0),
        h.l_arm.size());
  h.clear_logs();
  h.tick();
  CHECK(listener_pushes(h.l_push, {{sN, 2, SID0}}) && h.l_decl(0) == 2,
        "PS1: the first tx! after the settle declares Listener Ready, New (%zu "
        "pushes: %s, decl %d)", h.l_push.size(), push_words(h.l_push).c_str(),
        h.l_decl(0));

  h.reset();
  inject_failed(1 /*JoinIn*/);
  h.clear_logs();
  h.ctl(true, 0, SIDF, DAF, VID0);
  CHECK(h.l_reg[0] == 1 && h.l_fchg[0] == 0 && h.l_tkreg(0) == 2
        && h.l_fcode(0) == FCODE && h.l_fbridge(0) == SYSF && h.l_lat(0) == 888,
        "PS2: a Talker Failed registered before the settle registers at the "
        "settle: FAILED, its failure code and system id, its latency (reg %d "
        "fchg %d, tk %d, code %u, bridge %016llx, lat %u)", h.l_reg[0],
        h.l_fchg[0], h.l_tkreg(0), h.l_fcode(0),
        static_cast<unsigned long long>(h.l_fbridge(0)), h.l_lat(0));
  h.clear_logs();
  h.tick();
  CHECK(listener_pushes(h.l_push, {{sN, 1, SIDF}}) && h.l_decl(0) == 1,
        "PS2: the first tx! after the settle declares Listener Asking Failed, "
        "New (%zu pushes: %s, decl %d)", h.l_push.size(),
        push_words(h.l_push).c_str(), h.l_decl(0));
}

//! the failure information of SIDF reads at once on sink 0
bool SrpStreamFsmsSuite::failed_at_once() const {
  return h.l_reg[0] == 1 && h.l_tkreg(0) == 2 && h.l_fcode(0) == FCODE
         && h.l_fbridge(0) == SYSF;
}

//! acceptance 2: a re-bind (unbind, then bind to the same or another
//! stream) with the Talker already declared
void SrpStreamFsmsSuite::a_rebind_with_the_talker_declared_declares_on_the_next_tx() {
  const int sN = app_msg(VN, false, false);
  // the same stream, re-bound before tx!: LA + New! is VN, no Lv
  h.reset();
  h.ctl(true, 0, SIDF, DAF, VID0);
  inject_failed(3 /*JoinMt*/);
  int m = app_next(VO, eNew, false, true);
  for (int k = 0; k < 3; ++k) { h.tick(); m = app_next(m, eTx, false, true); }
  const bool qa = m == QA && h.l_app(0) == QA && h.l_decl(0) == 1;
  h.ctl(false, 0, SIDF, DAF, VID0);              // unbind: Lv!
  m = app_next(m, eLv, false, true);
  h.clear_logs();
  h.ctl(true, 0, SIDF, DAF, VID0);               // bind again, before tx!
  bool now = failed_at_once();
  m = app_next(m, eNew, false, true);
  h.clear_logs();
  h.tick();
  CHECK(qa && now && m == VN && listener_pushes(h.l_push, {{sN, 1, SIDF}})
        && h.l_decl(0) == 1,
        "PS3: unbind, then bind again before tx! to the stream whose Talker "
        "Failed is declared: FAILED with its failure code and system id at the "
        "settle, and the next tx! sends New Asking Failed, no Lv (QA %d, at "
        "once %d, %zu pushes: %s, decl %d)", qa, now, h.l_push.size(),
        push_words(h.l_push).c_str(), h.l_decl(0));
  // the same stream, re-bound after the Lv went out
  h.reset();
  h.ctl(true, 0, SIDF, DAF, VID0);
  inject_failed(3 /*JoinMt*/);
  for (int k = 0; k < 3; ++k) h.tick();
  h.ctl(false, 0, SIDF, DAF, VID0);
  h.clear_logs();
  h.tick();
  const bool lv = listener_pushes(h.l_push, {{app_msg(LA, false, false), 1, SIDF}});
  h.clear_logs();
  h.ctl(true, 0, SIDF, DAF, VID0);
  now = failed_at_once();
  h.clear_logs();
  h.tick();
  CHECK(lv && now && listener_pushes(h.l_push, {{sN, 1, SIDF}}) && h.l_decl(0) == 1,
        "PS3: unbind, its Lv sent, then bind again: FAILED at the settle and "
        "the next tx! sends New Asking Failed (Lv %d, at once %d, %zu pushes: "
        "%s)", lv, now, h.l_push.size(), push_words(h.l_push).c_str());

  // another stream whose Talker Failed is declared, bound before the old
  // stream's Lv: the two values each have the walk's tx!
  h.reset();
  m = l_goto(h, QA);
  inject_failed(1 /*JoinIn*/);
  h.ctl(false, 0, SID0, DA0, VID0);              // unbind SID0: Lv!
  m = app_next(m, eLv, false, true);
  h.clear_logs();
  h.ctl(true, 0, SIDF, DAF, VID0);               // bind to SIDF, before tx!
  now = failed_at_once() && h.l_decl(0) == 0;
  h.clear_logs();
  h.tick();
  CHECK(now && m == LA
        && listener_pushes(h.l_push, {{app_msg(m, false, false), 2, SID0},
                                      {sN, 1, SIDF}})
        && h.l_decl(0) == 1,
        "PS4: unbind, then bind before tx! to another stream whose Talker "
        "Failed is declared: FAILED with its failure information at the "
        "settle, and the next tx! sends the old stream's Lv, Ready, then New "
        "Asking Failed (at once %d, %zu pushes: %s, decl %d)", now,
        h.l_push.size(), push_words(h.l_push).c_str(), h.l_decl(0));
  h.clear_logs();
  h.tick();
  CHECK(listener_pushes(h.l_push, {{app_msg(AN, false, false), 1, SIDF}}),
        "PS4: the tx! after it sends the new stream's next message alone (%zu "
        "pushes: %s)", h.l_push.size(), push_words(h.l_push).c_str());

  // another stream, bound after the old stream's Lv went out
  h.reset();
  l_goto(h, QA);
  inject_failed(1 /*JoinIn*/);
  h.ctl(false, 0, SID0, DA0, VID0);
  h.clear_logs();
  h.tick();
  const bool lv0 = listener_pushes(h.l_push, {{app_msg(LA, false, false), 2, SID0}});
  h.clear_logs();
  h.ctl(true, 0, SIDF, DAF, VID0);
  now = failed_at_once();
  h.clear_logs();
  h.tick();
  CHECK(lv0 && now && listener_pushes(h.l_push, {{sN, 1, SIDF}}) && h.l_decl(0) == 1,
        "PS5: unbind, its Lv sent, then bind to another stream whose Talker "
        "Failed is declared: FAILED at the settle and the next tx! sends New "
        "Asking Failed (Lv %d, at once %d, %zu pushes: %s)", lv0, now,
        h.l_push.size(), push_words(h.l_push).c_str());
}

//! nothing registered or declared for sink 0, and the next tx! sends nothing
bool SrpStreamFsmsSuite::nothing_applied() {
  const bool quiet = h.l_reg[0] == 0 && h.l_tkreg(0) == 0 && h.l_regst(0) == R_MT
                     && h.l_arm.empty();
  h.clear_logs();
  h.tick();
  return quiet && h.l_push.empty() && h.l_decl(0) == 0;
}

//! acceptance 3: a Talker attribute withdrawn before the settle (rLv, or a
//! LeaveAll with no re-declaration) is not applied
void SrpStreamFsmsSuite::a_talker_withdrawn_before_the_settle_is_not_applied() {
  for (int type : {1, 2}) {
    h.reset();
    h.inject(true, type, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777, SYSF, FCODE);
    h.inject(true, type, SID0, DA0, VID0, 5 /*Lv*/);   // Δ13: IN -> MT
    h.clear_logs();
    h.ctl(true, 0, SID0, DA0, VID0);
    CHECK(nothing_applied(),
          "PS6: a Talker %s withdrawn (rLv) before the settle is not applied: "
          "nothing registered or declared, and the next tx! sends nothing (reg "
          "%d, tk %d, decl %d)", type == 1 ? "Advertise" : "Failed", h.l_reg[0],
          h.l_tkreg(0), h.l_decl(0));
  }
  // a LeaveAll (received on the value's lane, or the own) and no
  // re-declaration within T-MRP-LEAVE: leavetimer! ends the registration
  struct Case { int type; bool own; unsigned lanes; const char* what; };
  for (const Case& c : {Case{1, false, kLaTalkerAdv, "a received Talker Advertise LeaveAll"},
                        Case{2, false, kLaTalkerFailed, "a received Talker Failed LeaveAll"},
                        Case{1, true, 0, "the own LeaveAll"}}) {
    h.reset();
    h.inject(true, c.type, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777, SYSF, FCODE);
    if (c.own) h.la_own(); else h.la_rx_lanes(c.lanes);
    h.now = NOW + LEAVE_MS;
    h.idle(2);
    h.clear_logs();
    h.ctl(true, 0, SID0, DA0, VID0);
    CHECK(nothing_applied(),
          "PS7: a Talker %s aged by %s and not re-declared within T-MRP-LEAVE "
          "is not applied at a settle after it (reg %d, tk %d, decl %d)",
          c.type == 1 ? "Advertise" : "Failed", c.what, h.l_reg[0], h.l_tkreg(0),
          h.l_decl(0));
  }
  // a LeaveAll on another lane ages nothing: the Advertise is still applied
  h.reset();
  h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
  h.la_rx_lanes(kLaTalkerFailed | kLaListener | kLaDomain);
  h.now = NOW + LEAVE_MS;
  h.idle(2);
  h.clear_logs();
  h.ctl(true, 0, SID0, DA0, VID0);
  CHECK(h.l_reg[0] == 1 && h.l_tkreg(0) == 1 && h.l_regst(0) == R_IN,
        "PS7: a LeaveAll on the other lanes leaves the Talker Advertise IN: "
        "applied at a settle after T-MRP-LEAVE (reg %d, tk %d, state %d)",
        h.l_reg[0], h.l_tkreg(0), h.l_regst(0));
  // re-declared within T-MRP-LEAVE: IN again, applied
  h.reset();
  h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
  h.la_rx_lanes(kLaTalkerAdv);
  h.now = NOW + 1000;
  h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
  h.now = NOW + LEAVE_MS + 1000;
  h.idle(2);
  h.clear_logs();
  h.ctl(true, 0, SID0, DA0, VID0);
  CHECK(h.l_reg[0] == 1 && h.l_tkreg(0) == 1 && h.l_regst(0) == R_IN
        && h.l_arm.empty(),
        "PS7: a LeaveAll answered by a re-declaration within T-MRP-LEAVE: the "
        "Talker is IN and applied at a later settle, no timer op (reg %d, tk "
        "%d, state %d, %zu timer ops)", h.l_reg[0], h.l_tkreg(0),
        h.l_regst(0), h.l_arm.size());
}

//! a settle inside a LeaveAll's T-MRP-LEAVE: the registration starts LV and
//! keeps the port registrar's leavetimer deadline (Table 10-4 timing
//! unchanged, Milan v1.2 Table 4.3 LeaveTime)
void SrpStreamFsmsSuite::a_settle_inside_the_leave_period_keeps_its_deadline() {
  const int sN = app_msg(VN, false, false);
  h.reset();
  h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
  h.la_rx_lanes(kLaTalkerAdv);                    // LV, deadline NOW + 5000
  h.now = NOW + 2000;
  h.idle(2);
  h.clear_logs();
  h.ctl(true, 0, SID0, DA0, VID0);
  CHECK(h.l_reg[0] == 1 && h.l_tkreg(0) == 1 && h.l_regst(0) == R_LV
        && h.l_arm.size() == 1 && !h.l_arm[0].cancel && h.l_arm[0].slot == kLsSlot
        && h.l_arm[0].owner == 0x60 && h.l_arm[0].deadline == NOW + LEAVE_MS,
        "PS8: a settle 2000 ms into the LeaveAll's T-MRP-LEAVE registers LV, "
        "the sink's leave slot armed with the deadline the LeaveAll set "
        "(reg %d, tk %d, state %d, %zu ops, deadline %u, want %u)", h.l_reg[0],
        h.l_tkreg(0), h.l_regst(0), h.l_arm.size(),
        h.l_arm.empty() ? 0u : h.l_arm[0].deadline, NOW + LEAVE_MS);
  h.clear_logs();
  h.tick();
  const bool ready = listener_pushes(h.l_push, {{sN, 2, SID0}}) && h.l_decl(0) == 2;
  h.now = NOW + LEAVE_MS;
  h.clear_logs();
  h.expire(kLsSlot);
  CHECK(ready && h.l_unreg[0] == 1 && h.l_tkreg(0) == 0 && h.l_regst(0) == R_MT,
        "PS8: the LV registration declares Ready and ends at that deadline's "
        "leavetimer!: EVT_TK_UNREGISTERED, MT (ready %d, unreg %d, tk %d, "
        "state %d)", ready, h.l_unreg[0], h.l_tkreg(0), h.l_regst(0));
  // re-declared after the settle: IN, the timer cancelled
  h.reset();
  h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
  h.la_rx_lanes(kLaTalkerAdv);
  h.now = NOW + 2000;
  h.ctl(true, 0, SID0, DA0, VID0);
  h.clear_logs();
  h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
  CHECK(h.l_regst(0) == R_IN && h.l_reg[0] == 0 && h.l_arm.size() == 1
        && h.l_arm[0].cancel && h.l_arm[0].slot == kLsSlot,
        "PS8: a re-declaration after such a settle returns IN silently and "
        "cancels the leave slot (state %d, reg %d, %zu ops, cancel %d)",
        h.l_regst(0), h.l_reg[0], h.l_arm.size(),
        h.l_arm.empty() ? -1 : int(h.l_arm[0].cancel));
}

//! the settle takes the port registrar's state after the events of its own
//! clock: a LeaveAll, or the leavetimer!, on the settle's clock
void SrpStreamFsmsSuite::a_settle_takes_its_own_clocks_leaveall_and_expiry() {
  h.reset();
  h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
  h.now = NOW + 300;
  h.clear_logs();
  d->ctl_valid_i = 1; d->ctl_settle_i = 1; d->ctl_sink_i = 0;
  d->ctl_stream_id_i = SID0; d->ctl_da_i = DA0; d->ctl_vid_i = VID0;
  d->leaveall_rx_i = kLaTalkerAdv;
  h.step();
  h.idle(2);
  CHECK(h.l_reg[0] == 1 && h.l_regst(0) == R_LV && h.l_arm.size() == 1
        && !h.l_arm[0].cancel && h.l_arm[0].deadline == NOW + 300 + LEAVE_MS,
        "PS9: a LeaveAll on the settle's clock ages the registration the settle "
        "starts: LV, its leave slot armed for now + T-MRP-LEAVE (reg %d, state "
        "%d, %zu ops, deadline %u)", h.l_reg[0], h.l_regst(0), h.l_arm.size(),
        h.l_arm.empty() ? 0u : h.l_arm[0].deadline);
  h.reset();
  h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
  h.la_rx_lanes(kLaTalkerAdv);
  h.now = NOW + LEAVE_MS;                         // leavetimer! on this clock
  h.clear_logs();
  h.ctl(true, 0, SID0, DA0, VID0);
  CHECK(nothing_applied(),
        "PS9: a settle on the clock of the port registrar's leavetimer! is not "
        "applied (reg %d, tk %d, decl %d)", h.l_reg[0], h.l_tkreg(0), h.l_decl(0));
}

//! the exact {stream_id, DA, VLAN} (Milan v1.2 5.3.8.9) and the bound
void SrpStreamFsmsSuite::the_port_registrars_match_exactly_and_are_bounded() {
  h.reset();
  h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
  h.inject(true, 1, SID0 + 7, DA0 + 7, VID0 | 0x1000, 1 /*JoinIn*/, 0, 777);
  h.clear_logs();
  h.ctl(true, 0, SID0, DA0 ^ 1, VID0);
  h.ctl(true, 1, SID0, DA0, VID0 + 1);
  h.ctl(true, 2, SID0 ^ 1, DA0, VID0);
  h.ctl(true, 3, SID0 + 7, DA0 + 7, VID0);
  const bool miss = h.l_reg[0] + h.l_reg[1] + h.l_reg[2] + h.l_reg[3] == 0
                    && h.l_tkreg(0) + h.l_tkreg(1) + h.l_tkreg(2) + h.l_tkreg(3) == 0;
  h.ctl(true, 4, SID0, DA0, VID0);
  CHECK(miss && h.l_reg[4] == 1 && h.l_tkreg(4) == 1,
        "PS10: a settle on a near miss of a registered value (its DA, VLAN or "
        "stream_id, or a VLAN that differs above bit 11) takes nothing; the "
        "exact value is taken (miss %d, exact reg %d tk %d)", miss, h.l_reg[4],
        h.l_tkreg(4));

  // every port registrar held: a value registered next is not held
  h.reset();
  fill_port_registrars();
  h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
  h.clear_logs();
  h.ctl(true, 0, SID0, DA0, VID0);
  const bool unheld = h.l_reg[0] == 0 && h.l_tkreg(0) == 0;
  h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
  const bool next = h.l_reg[0] == 1 && h.l_tkreg(0) == 1;
  h.clear_logs();
  h.ctl(true, 1, SID0 + 0x103, DA0 + 0x103, VID0);
  CHECK(unheld && next && h.l_reg[1] == 1 && h.l_tkreg(1) == 1,
        "PS11: with all %d port registrars held, a value registered next is not "
        "held: its settle takes nothing and the talker's next declaration "
        "registers it; a held value is taken (unheld %d, next %d, held reg %d)",
        kPortRegs, unheld, next, h.l_reg[1]);
  h.inject(true, 1, SID0 + 0x105, DA0 + 0x105, VID0, 5 /*Lv*/);  // frees one
  inject_failed(1 /*JoinIn*/);
  h.clear_logs();
  h.ctl(true, 2, SIDF, DAF, VID0);
  CHECK(h.l_reg[2] == 1 && h.l_tkreg(2) == 2,
        "PS11: a withdrawal frees its port registrar: the next value registered "
        "is held and taken at its settle (reg %d, tk %d)", h.l_reg[2],
        h.l_tkreg(2));
}

//! two sinks settled on one pre-registered stream share one declaration
//! (issue #193), and a re-bind onto a stream another sink declares adds no
//! second declaration of it
void SrpStreamFsmsSuite::pre_registered_streams_keep_one_declaration_per_stream() {
  h.reset();
  h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
  h.ctl(true, 0, SID0, DA0, VID0);
  h.ctl(true, 3, SID0, DA0, VID0);
  const bool both = h.l_reg[0] == 1 && h.l_reg[3] == 1;
  const int sinks[] = {0, 3};
  CHECK(both && ticks_follow_the_model(VN, 2, 3, "PS12: two sinks settled on one "
        "pre-registered stream: each tx! sends what ONE applicant sends") == QA
        && h.l_app(3) == VO && h.l_decl(sinks[0]) == 2 && h.l_decl(sinks[1]) == 2,
        "PS12: both register at the settle, one applicant (sink 0) declares "
        "Ready for both, the rider is VO (both %d, rider %s)", both, SN[h.l_app(3)]);

  constexpr uint64_t SIDB = 0x02AABBCCDDEE0002ull;
  constexpr uint64_t DAB  = 0x91E0F0001235ull;
  h.reset();
  h.ctl(true, 1, SIDB, DAB, VID0);
  h.inject(true, 1, SIDB, DAB, VID0, 3 /*JoinMt*/, 0, 500);
  for (int k = 0; k < 3; ++k) h.tick();               // sink 1: SIDB, QA
  int m = l_goto(h, QA);                              // sink 0: SID0, QA
  h.ctl(false, 0, SID0, DA0, VID0);
  m = app_next(m, eLv, false, true);
  h.clear_logs();
  h.ctl(true, 0, SIDB, DAB, VID0);                    // onto SIDB, before tx!
  const bool now = h.l_reg[0] == 1 && h.l_tkreg(0) == 1;
  h.clear_logs();
  h.tick();
  const bool lv = listener_pushes(h.l_push, {{app_msg(m, false, false), 2, SID0}});
  h.clear_logs();
  h.tick();
  CHECK(now && lv && h.l_push.empty() && h.l_decl(0) == 2 && h.l_decl(1) == 2,
        "PS13: a re-bind before tx! onto a stream another sink declares: the "
        "next tx! sends the old stream's Lv only and the stream stays one "
        "declaration, both sinks Ready (at once %d, Lv %d, then %zu pushes, "
        "decl %d/%d)", now, lv, h.l_push.size(), h.l_decl(0), h.l_decl(1));
}

//! A registration change of the new stream on any clock of the walk that
//! sends the parked Lv: after that walk and the next, the sink's declaration
//! follows the registration and a peer Registrar of the new stream agrees.
void SrpStreamFsmsSuite::a_registration_change_during_the_retiring_walk_is_followed() {
  constexpr uint64_t SIDB = 0x02AABBCCDDEE0002ull;
  constexpr uint64_t DAB  = 0x91E0F0001235ull;
  for (const bool swap : {false, true}) {
    std::string bad;
    for (int at = 0; at <= 8 && bad.empty(); ++at) {
      h.reset();
      l_goto(h, QA);                                   // sink 0: SID0, QA
      h.inject(true, 1, SIDB, DAB, VID0, 1 /*JoinIn*/, 0, 500);
      h.ctl(false, 0, SID0, DA0, VID0);
      h.ctl(true, 0, SIDB, DAB, VID0);                 // parked, request waits
      h.clear_logs();
      d->join_tick_i = 1;
      bool fired = false;
      bool done = false;
      for (int i = 0; i < kTxopPollSteps && !done; ++i) {
        if (!fired && i == at) {
          d->evt_valid_i = 1; d->evt_msrp_i = 1;
          d->evt_attr_type_i = swap ? 2 : 1;
          d->evt_stream_id_i = SIDB; d->evt_da_i = DAB; d->evt_vid_i = VID0;
          d->evt_mrp_event_i = swap ? 1 /*JoinIn*/ : 5 /*Lv*/;
          d->evt_fourpacked_i = 0; d->evt_acc_latency_i = 500;
          d->evt_failure_system_id_i = SYSF; d->evt_failure_code_i = FCODE;
          fired = true;
        }
        h.step();
        done = d->l_txop_done_o != 0;
      }
      h.idle(4);
      std::vector<Push> all = h.l_push;
      h.clear_logs();
      h.tick();
      all.insert(all.end(), h.l_push.begin(), h.l_push.end());
      bool peer_in = false;
      int last_fp = -1;
      int lv0 = 0;
      for (const Push& p : all) {
        uint64_t got = 0;
        for (int k = 0; k < 8; ++k) got = (got << 8) | p.val[k];
        if (p.type == 3 && got == SID0 && p.code == 5) ++lv0;
        if (p.type != 3 || got != SIDB) continue;
        if (p.code == 0 || p.code == 1 || p.code == 3) { peer_in = true; last_fp = p.fp; }
        if (p.code == 5) peer_in = false;
      }
      const bool ok = swap ? (done && lv0 == 1 && h.l_tkreg(0) == 2 && h.l_decl(0) == 1
                              && peer_in && last_fp == 1)
                           : (done && lv0 == 1 && h.l_tkreg(0) == 0 && h.l_decl(0) == 0
                              && !peer_in);
      if (!ok) {
        bad = "clock " + std::to_string(at) + ": " + push_words(all) + ", tk "
              + std::to_string(h.l_tkreg(0)) + ", decl " + std::to_string(h.l_decl(0));
      }
    }
    CHECK(bad.empty(),
          "PS14: the new stream's Talker %s on any clock of the walk that sends "
          "the parked Lv: the old Lv goes once, and after that walk and the next "
          "the sink %s and a peer Registrar of the new stream %s (%s)",
          swap ? "turns Failed (JoinIn)" : "withdraws (rLv)",
          swap ? "declares Asking Failed" : "declares nothing",
          swap ? "holds Asking Failed" : "is MT", bad.empty() ? "every clock" : bad.c_str());
  }
}

//! the old registration's leavetimer! on the clock of a seeding settle is
//! the teardown's: no EVT_TK_UNREGISTERED beside the new registration
void SrpStreamFsmsSuite::a_seeding_settle_silences_the_old_expiry() {
  h.reset();
  h.inject(true, 1, SIDF, DAF, VID0, 1 /*JoinIn*/, 0, 500);  // held, no sink
  h.ctl(true, 0, SID0, DA0, VID0);
  h.inject(true, 1, SID0, DA0, VID0, 1 /*JoinIn*/, 0, 777);
  h.la_rx_lanes(kLaTalkerAdv);       // both LV: sink 0's slot armed
  h.inject(true, 1, SIDF, DAF, VID0, 1 /*JoinIn*/, 0, 500);  // SIDF IN again
  const bool lv = h.l_regst(0) == R_LV;
  h.clear_logs();
  d->ctl_valid_i = 1; d->ctl_settle_i = 1; d->ctl_sink_i = 0;
  d->ctl_stream_id_i = SIDF; d->ctl_da_i = DAF; d->ctl_vid_i = VID0;
  d->exp_valid_i = 1; d->exp_slot_i = kLsSlot;
  h.step();
  h.idle(2);
  CHECK(lv && h.l_reg[0] == 1 && h.l_unreg[0] == 0 && h.l_tkreg(0) == 1
        && h.l_regst(0) == R_IN,
        "PS15: the old registration's leavetimer! on the clock of a settle onto "
        "a held stream: one EVT_TK_REGISTERED, no EVT_TK_UNREGISTERED, IN (LV "
        "before %d, reg %d, unreg %d, tk %d, state %d)", lv, h.l_reg[0],
        h.l_unreg[0], h.l_tkreg(0), h.l_regst(0));
}
