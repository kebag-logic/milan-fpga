#!/usr/bin/env python3
"""Re-park probe: a parked sink re-binds again before its owed Lv goes out.

Inserts one probe method into a COPY of tb/srp_stream_fsms/sim_main.cpp.
Sink 1 declares SIDP. Sink 0, alone on SID0 and ticked to QA, re-binds to
SIDP (parks SID0's Lv; its matcher now equals sink 1's), then, before any
tx!, re-binds again to SIDQ (parked again: it must keep its own leave-copy
pairs, which say SID0 is no other sink's stream). The next tx! must send
SID0's Lv once, and sink 1's SIDP declaration must follow its own model.

usage: repark_probe.py <copied sim_main.cpp>
"""
import sys

path = sys.argv[1]
src = open(path).read()

decl = "  void ready_with_asking_failed_declares_ready_failed();\n"
assert src.count(decl) == 1
src = src.replace(decl, decl + "  void probe_repark();\n")

body = r'''
void SrpStreamFsmsSuite::probe_repark() {
  constexpr uint64_t SIDQ = 0x02AABBCCDDEE0003ull;
  constexpr uint64_t DAQ  = 0x91E0F0001236ull;
  h.reset();
  h.ctl(true, 1, SIDP, DAP, VID0);
  h.inject(true, 1, SIDP, DAP, VID0, 3 /*JoinMt*/, 0, 500);
  h.ctl(true, 0, SID0, DA0, VID0);
  h.inject(true, 1, SID0, DA0, VID0, 3 /*JoinMt*/, 0, 500);
  int m0 = app_next(VO, eNew, false, true);
  int m1 = app_next(VO, eNew, false, true);
  for (int k = 0; k < 3; ++k) {
    h.tick();
    m0 = app_next(m0, eTx, false, true);
    m1 = app_next(m1, eTx, false, true);
  }
  h.ctl(true, 0, SIDP, DAP, VID0);      // parks SID0's Lv
  m0 = app_next(m0, eLv, false, true);
  h.ctl(true, 0, SIDQ, DAQ, VID0);      // parked again
  m0 = app_next(m0, eLv, false, true);
  h.clear_logs();
  h.tick();
  const std::string a = listener_words(h.l_push, SID0);
  const std::string p = listener_words(h.l_push, SIDP);
  const std::string wa = model_words(app_msg(m0, false, false), 2);
  const std::string wp = model_words(app_msg(m1, false, false), 2);
  printf("PROBE REPARK: SID0 sent '%s' (model '%s'); SIDP sent '%s' (model '%s'); app %s/%s -> %s\n",
         a.c_str(), wa.c_str(), p.c_str(), wp.c_str(), SN[h.l_app(0)], SN[h.l_app(1)],
         (a == wa && p == wp) ? "MATCH" : "DIFF");
}

'''
anchor = "int SrpStreamFsmsSuite::run() {"
assert src.count(anchor) == 1
src = src.replace(anchor, body + anchor)

call = "  ready_with_asking_failed_declares_ready_failed();\n\n  printf("
assert src.count(call) == 1
src = src.replace(call, "  ready_with_asking_failed_declares_ready_failed();\n"
                  "  probe_repark();\n\n  printf(")
open(path, "w").write(src)
