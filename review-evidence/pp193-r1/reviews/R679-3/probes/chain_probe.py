#!/usr/bin/env python3
"""Chain probe: two handovers behind the walk, swept over their clocks.

Inserts one probe method into a COPY of tb/srp_stream_fsms/sim_main.cpp.
Sinks 0 (VLAN 3), 3 (VLAN 4) and 7 (VLAN 2) settle on one stream_id; only
sink 7's talker registers, so sink 7 declares alone. It is ticked to QA
(txLA! walk) or AN (plain tx! walk). During the walk, at clock A sink 3's
talker registers (sink 3 becomes the owner and takes the applicant from
sink 7) and at clock B sink 0's talker registers (sink 0 becomes the owner
and takes it from whichever sink holds it). A and B are swept over clocks
that land before, inside and after the first pass and any second pass of
the walk (-1 = never). Every row must show: the walk ended, the walk sent
exactly what ONE Table 10-3 applicant sends at that opportunity, the next
two plain ticks follow the same model, and the lowest registered sink holds
the applicant while the others are VO.

usage: chain_probe.py <copied sim_main.cpp>
"""
import sys

path = sys.argv[1]
src = open(path).read()

decl = "  void ready_with_asking_failed_declares_ready_failed();\n"
assert src.count(decl) == 1
src = src.replace(decl, decl + "  int probe_chain(bool txla, int a, int b);\n")

body = r'''
int SrpStreamFsmsSuite::probe_chain(bool txla, int a, int b) {
  constexpr uint16_t VA = 3;   // sink 0's VLAN
  constexpr uint16_t VB = 4;   // sink 3's VLAN
  h.reset();
  h.ctl(true, 0, SID0, DA0, VA);
  h.ctl(true, 3, SID0, DA0, VB);
  h.ctl(true, 7, SID0, DA0, VID0);
  h.inject(true, 1, SID0, DA0, VID0, 3 /*JoinMt*/, 0, 500);
  int m = app_next(VO, eNew, false, true);
  const int pre_ticks = txla ? 3 : 1;
  for (int k = 0; k < pre_ticks; ++k) { h.tick(); m = app_next(m, eTx, false, true); }
  if (txla) h.la_own();
  h.clear_logs();
  d->join_tick_i = 1;
  bool done = false;
  int clocks = 0;
  for (int i = 0; i < kTxopPollSteps && !done; ++i) {
    const int vid = (i == a) ? VB : (i == b) ? VA : -1;
    if (vid >= 0) {
      d->evt_valid_i = 1; d->evt_msrp_i = 1; d->evt_attr_type_i = 1;
      d->evt_stream_id_i = SID0; d->evt_da_i = DA0; d->evt_vid_i = vid;
      d->evt_mrp_event_i = 3; d->evt_fourpacked_i = 0;
      d->evt_acc_latency_i = 500; d->evt_failure_system_id_i = 0;
      d->evt_failure_code_i = 0;
    }
    h.step();
    done = d->l_txop_done_o != 0;
    clocks = i + 1;
  }
  // inputs that fall after the walk ended still arrive, outside the walk
  for (int i = clocks; i <= a || i <= b; ++i) {
    const int vid = (i == a) ? VB : (i == b) ? VA : -1;
    if (vid >= 0) {
      d->evt_valid_i = 1; d->evt_msrp_i = 1; d->evt_attr_type_i = 1;
      d->evt_stream_id_i = SID0; d->evt_da_i = DA0; d->evt_vid_i = vid;
      d->evt_mrp_event_i = 3; d->evt_fourpacked_i = 0;
      d->evt_acc_latency_i = 500; d->evt_failure_system_id_i = 0;
      d->evt_failure_code_i = 0;
    }
    h.step();
  }
  h.idle(4);
  const std::string w = listener_words(h.l_push, SID0);
  const std::string want = model_words(app_msg(m, txla, false), 2);
  m = app_next(m, txla ? eTxLA : eTx, false, true);
  std::string nx[2];
  std::string nwant[2];
  for (int k = 0; k < 2; ++k) {
    h.clear_logs();
    h.tick();
    nx[k] = listener_words(h.l_push, SID0);
    nwant[k] = model_words(app_msg(m, false, false), 2);
    m = app_next(m, eTx, false, true);
  }
  const int owner = (b >= 0) ? 0 : (a >= 0) ? 3 : 7;
  bool own_ok = h.l_app(owner) == m;
  for (int s : {0, 3, 7}) if (s != owner) own_ok = own_ok && h.l_app(s) == VO;
  const bool ok = done && w == want && nx[0] == nwant[0] && nx[1] == nwant[1] && own_ok;
  printf("PROBE CHAIN walk=%s A=%d B=%d: ended %d after %d clocks; walk '%s' (model '%s'); "
         "next '%s' '%s' (model '%s' '%s'); apps %s/%s/%s owner %d -> %s\n",
         txla ? "txLA!" : "tx!", a, b, done, clocks, w.c_str(), want.c_str(),
         nx[0].c_str(), nx[1].c_str(), nwant[0].c_str(), nwant[1].c_str(),
         SN[h.l_app(0)], SN[h.l_app(3)], SN[h.l_app(7)], owner, ok ? "MATCH" : "DIFF");
  return ok ? 0 : 1;
}

'''
anchor = "int SrpStreamFsmsSuite::run() {"
assert src.count(anchor) == 1
src = src.replace(anchor, body + anchor)

call = "  ready_with_asking_failed_declares_ready_failed();\n\n  printf("
assert src.count(call) == 1
calls = (
    "  {\n    int diffs = 0, rows = 0;\n"
    "    for (int tl = 0; tl < 2; ++tl)\n"
    "      for (int a = -1; a <= 12; ++a)\n"
    "        for (int b = -1; b <= 24; ++b) {\n"
    "          if (a == 0 || b == 0 || (a == b && a >= 0)) continue;\n"
    "          diffs += probe_chain(tl != 0, a, b); ++rows;\n"
    "        }\n"
    "    printf(\"PROBE CHAIN SUMMARY rows %d DIFF %d\\n\", rows, diffs);\n  }\n")
src = src.replace(call, "  ready_with_asking_failed_declares_ready_failed();\n" + calls
                  + "\n  printf(")
open(path, "w").write(src)
