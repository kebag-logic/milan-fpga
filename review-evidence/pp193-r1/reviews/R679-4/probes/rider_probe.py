#!/usr/bin/env python3
"""Rider probe: what a rider above the owner does after a received LeaveAll.

Inserts one probe method into a COPY of tb/srp_stream_fsms/sim_main.cpp.
Sinks 0 (owner) and 1 (rider) settle on one stream_id and both declare
(the suite's shared_stream_goes_quiet(2) setup). A received LeaveAll, then
eight plain ticks: each row prints the owner's and the rider's applicant
state and what the tick sent for the stream, beside the one-applicant model.
Then the rider's A8 (the rider unbinds while the owner declares) and three
ticks, the same rows. At the head the rider must stay VO and every tick must
send what the model sends.

usage: rider_probe.py <copied sim_main.cpp>
"""
import sys

path = sys.argv[1]
src = open(path).read()

decl = "  void ready_with_asking_failed_declares_ready_failed();\n"
assert src.count(decl) == 1
src = src.replace(decl, decl + "  void probe_rider();\n")

body = r'''
void SrpStreamFsmsSuite::probe_rider() {
  int m = shared_stream_goes_quiet(2, "PROBE-RIDER-SETUP");
  h.la_rx();
  m = app_next(m, eRLA, false, true);
  int diff = 0, notvo = 0;
  for (int k = 0; k < 8; ++k) {
    const std::string want = model_words(app_msg(m, false, false), 2);
    h.clear_logs();
    h.tick();
    m = app_next(m, eTx, false, true);
    const std::string got = listener_words(h.l_push, SID0);
    diff += (got != want) || h.l_push.size() != (want.empty() ? 0u : 1u);
    notvo += h.l_app(1) != VO;
    printf("PROBE RIDER rla tick %d: owner %s rider %s sent '%s' (%zu pushes) model '%s'\n",
           k, SN[h.l_app(0)], SN[h.l_app(1)], got.c_str(), h.l_push.size(), want.c_str());
  }
  h.ctl(false, 1, SID0, DA0, VID0);
  for (int k = 0; k < 3; ++k) {
    const std::string want = model_words(app_msg(m, false, false), 2);
    h.clear_logs();
    h.tick();
    m = app_next(m, eTx, false, true);
    const std::string got = listener_words(h.l_push, SID0);
    diff += (got != want) || h.l_push.size() != (want.empty() ? 0u : 1u);
    printf("PROBE RIDER after rider A8 tick %d: owner %s slot1 %s sent '%s' (%zu pushes) model '%s'\n",
           k, SN[h.l_app(0)], SN[h.l_app(1)], got.c_str(), h.l_push.size(), want.c_str());
  }
  printf("PROBE RIDER SUMMARY wire-diffs %d rider-not-VO-ticks %d\n", diff, notvo);
}

'''
anchor = "int SrpStreamFsmsSuite::run() {"
assert src.count(anchor) == 1
src = src.replace(anchor, body + anchor)
call = "  ready_with_asking_failed_declares_ready_failed();\n\n  printf("
assert src.count(call) == 1
src = src.replace(call, "  ready_with_asking_failed_declares_ready_failed();\n  probe_rider();\n"
                  + "\n  printf(")
open(path, "w").write(src)
