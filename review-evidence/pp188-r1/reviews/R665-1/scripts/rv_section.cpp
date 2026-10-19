// ==== RV. reviewer probe section (scratch only; never committed) =========
// Settle-table arms of 10 §6.4 and the KL_srp_listener_fsm banner that
// section M does not reach: a settle while parked (a third stream, and back
// to the parked one), an LO applicant (an Empty owed), a txLA! walk while
// parked, and a received Listener value while parked. Expectations come from
// the suite's own Table 10-3 model (app_next/app_msg).
void SrpStreamFsmsSuite::reviewer_rv_probes() {
  constexpr uint64_t SIDB = 0x02AABBCCDDEE0002ull;
  constexpr uint64_t DAB  = 0x91E0F0001235ull;
  constexpr uint64_t SIDC = 0x02AABBCCDDEE0003ull;
  constexpr uint64_t DAC  = 0x91E0F0001236ull;
  const int sL = app_msg(LA, false, false);
  const int sN = app_msg(VN, false, false);
  const int sE = app_msg(LO, false, false);   // LO tx!: s (Mt, reg_in tied 0)

  // RV1: parked on SID0 (rebind to SIDB), then a second rebind to SIDC before
  // tx!: the applicant still holds SID0, so the tx! sends SID0's Lv.
  h.reset();
  int m = l_goto(h, QA);
  h.ctl(false, 0, SID0, DA0, VID0);
  m = app_next(m, eLv, false, true);
  h.ctl(true, 0, SIDB, DAB, VID0);
  h.ctl(false, 0, SIDB, DAB, VID0);
  h.ctl(true, 0, SIDC, DAC, VID0);
  h.clear_logs();
  h.tick();
  CHECK(one_listener_push(h.l_push, sL, 2, SID0) && m == LA,
        "RV1: a second rebind while parked: the tx! sends the held stream's Lv "
        "(%zu pushes, code %d)", h.l_push.size(),
        h.l_push.empty() ? -1 : h.l_push[0].code);

  // RV2: parked on SID0, then rebound back to SID0 before tx!, whose talker
  // registers again: the applicant it holds is kept, LA + New! is VN.
  h.reset();
  m = l_goto(h, QA);
  h.ctl(false, 0, SID0, DA0, VID0);
  m = app_next(m, eLv, false, true);
  h.ctl(true, 0, SIDB, DAB, VID0);
  h.ctl(false, 0, SIDB, DAB, VID0);
  h.ctl(true, 0, SID0, DA0, VID0);
  h.inject(true, 1, SID0, DA0, VID0, 3 /*JoinMt*/, 0, 500);
  m = app_next(m, eNew, false, true);
  h.clear_logs();
  h.tick();
  CHECK(one_listener_push(h.l_push, sN, 2, SID0) && m == VN,
        "RV2: a rebind back to the parked stream keeps its applicant: New "
        "Ready on SID0, no Lv (%zu pushes, code %d)", h.l_push.size(),
        h.l_push.empty() ? -1 : h.l_push[0].code);

  // RV3: an LO applicant (an Empty owed) on SID0 settles on SIDB before tx!:
  // the tx! sends SID0's s, then SIDB's New on the tx! after.
  h.reset();
  m = l_goto(h, LO);
  h.ctl(true, 0, SIDB, DAB, VID0);
  m = app_next(m, eLv, false, true);
  h.inject(true, 1, SIDB, DAB, VID0, 3 /*JoinMt*/, 0, 500);
  h.clear_logs();
  h.tick();
  CHECK(m == LO && h.l_push.size() == 1 && h.l_push[0].code == sE
            && [&] { uint64_t g = 0; for (int i = 0; i < 8; ++i) g = (g << 8) | h.l_push[0].val[i];
                     return g == SID0; }(),
        "RV3: an LO applicant settled on another stream: the tx! sends the "
        "held stream's Empty (%zu pushes, code %d)", h.l_push.size(),
        h.l_push.empty() ? -1 : h.l_push[0].code);
  h.clear_logs();
  h.tick();
  CHECK(one_listener_push(h.l_push, sN, 2, SIDB),
        "RV3: the tx! after it declares SIDB, New Ready (%zu pushes)", h.l_push.size());

  // RV4: parked on SID0 (LA), the next walk is a txLA!: LA goes to LO with
  // no message, and the park stays, so the tx! after it sends SID0's s.
  h.reset();
  m = l_goto(h, QA);
  h.ctl(false, 0, SID0, DA0, VID0);
  m = app_next(m, eLv, false, true);
  h.ctl(true, 0, SIDB, DAB, VID0);
  h.inject(true, 1, SIDB, DAB, VID0, 3 /*JoinMt*/, 0, 500);
  h.la_own();
  h.clear_logs();
  h.tick();
  m = app_next(m, eTxLA, false, true);
  bool rv4a = h.l_push.empty() && m == LO;
  h.clear_logs();
  h.tick();
  CHECK(rv4a && h.l_push.size() == 1 && h.l_push[0].code == sE
            && [&] { uint64_t g = 0; for (int i = 0; i < 8; ++i) g = (g << 8) | h.l_push[0].val[i];
                     return g == SID0; }(),
        "RV4: a txLA! walk keeps the park (LO): the tx! after it sends the held "
        "stream's Empty (txLA quiet %d, %zu pushes, code %d)", rv4a, h.l_push.size(),
        h.l_push.empty() ? -1 : h.l_push[0].code);

  // RV5: an LO applicant parked on SID0 receives a Listener Mt naming the
  // new stream SIDB: not applied while parked, so SID0's s still goes out.
  h.reset();
  m = l_goto(h, LO);
  h.ctl(true, 0, SIDB, DAB, VID0);
  h.inject(true, 3, SIDB, 0, 0, 4 /*Mt*/, 2);
  h.clear_logs();
  h.tick();
  CHECK(h.l_push.size() == 1 && h.l_push[0].code == sE
            && [&] { uint64_t g = 0; for (int i = 0; i < 8; ++i) g = (g << 8) | h.l_push[0].val[i];
                     return g == SID0; }(),
        "RV5: a new stream's Listener value is not applied to the parked "
        "applicant (%zu pushes, code %d)", h.l_push.size(),
        h.l_push.empty() ? -1 : h.l_push[0].code);
}

