#!/usr/bin/env python3
"""Role-shift probe: the walk sends the last declarer's Lv, then a rider of
the stream ahead of the walk declares before the walk reaches it.

Inserts one probe method into a COPY of tb/srp_stream_fsms/sim_main.cpp.
Sink 1 (VID0) and sink 6 (VLAN 3) settled on SID0; sink 1's talker registers,
sink 1 declares alone and is ticked to QA, then its A8 (the last declarer:
Lv!, LA). A tx! walk starts; at clock `at` sink 6's talker registers, so sink
6 declares SID0. The one-applicant model: the walk's tx! sends the Lv, the
New! after it waits for the next tx!. Prints what the walk and the next two
ticks send for SID0 beside the model.

usage: role_shift_probe.py <copied sim_main.cpp>
"""
import sys

path = sys.argv[1]
src = open(path).read()
decl = "  void ready_with_asking_failed_declares_ready_failed();\n"
assert src.count(decl) == 1
src = src.replace(decl, decl + "  void probe_role_shift(int at);\n")
body = r'''
void SrpStreamFsmsSuite::probe_role_shift(int at) {
  constexpr uint16_t VID1 = 3;
  h.reset();
  h.ctl(true, 1, SID0, DA0, VID0);
  h.ctl(true, 6, SID0, DA0, VID1);
  h.inject(true, 1, SID0, DA0, VID0, 3 /*JoinMt*/, 0, 500);
  int m = app_next(VO, eNew, false, true);
  for (int k = 0; k < 3; ++k) { h.tick(); m = app_next(m, eTx, false, true); }
  h.ctl(false, 1, SID0, DA0, VID0);
  m = app_next(m, eLv, false, true);
  h.clear_logs();
  d->join_tick_i = 1;
  bool done = false;
  bool injected = false;
  for (int i = 0; i < kTxopPollSteps && !done; ++i) {
    if (i == at) {
      d->evt_valid_i = 1; d->evt_msrp_i = 1; d->evt_attr_type_i = 1;
      d->evt_stream_id_i = SID0; d->evt_da_i = DA0; d->evt_vid_i = VID1;
      d->evt_mrp_event_i = 3; d->evt_fourpacked_i = 0;
      d->evt_acc_latency_i = 500; d->evt_failure_system_id_i = 0;
      d->evt_failure_code_i = 0;
      injected = true;
    }
    h.step();
    done = d->l_txop_done_o != 0;
  }
  if (!injected) h.inject(true, 1, SID0, DA0, VID1, 3, 0, 500);
  h.idle(2);
  const std::string w = listener_words(h.l_push, SID0);
  const std::string want = model_words(app_msg(m, false, false), 2);
  m = app_next(app_next(m, eTx, false, true), eNew, false, true);
  std::string nx[2], nw[2];
  for (int k = 0; k < 2; ++k) {
    h.clear_logs();
    h.tick();
    nx[k] = listener_words(h.l_push, SID0);
    nw[k] = model_words(app_msg(m, false, false), 2);
    m = app_next(m, eTx, false, true);
  }
  printf("PROBE ROLE inject@%d: walk sent '%s' (model '%s'); next '%s' '%s' (model '%s' '%s'); "
         "app1 %s app6 %s decl6 %d -> %s\n", at, w.c_str(), want.c_str(), nx[0].c_str(),
         nx[1].c_str(), nw[0].c_str(), nw[1].c_str(), SN[h.l_app(1)], SN[h.l_app(6)],
         h.l_decl(6), (w == want && nx[0] == nw[0] && nx[1] == nw[1]) ? "MATCH" : "DIFF");
}

'''
anchor = "int SrpStreamFsmsSuite::run() {"
assert src.count(anchor) == 1
src = src.replace(anchor, body + anchor)
call = "  ready_with_asking_failed_declares_ready_failed();\n\n  printf("
assert src.count(call) == 1
calls = "".join(f"  probe_role_shift({at});\n" for at in list(range(0, 16)) + [9999])
src = src.replace(call, "  ready_with_asking_failed_declares_ready_failed();\n" + calls + "\n  printf(")
open(path, "w").write(src)
