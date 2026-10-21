#!/usr/bin/env python3
"""S2 probe: a handover into a slot the tx! walk has already passed.

Inserts one probe method into a COPY of tb/srp_stream_fsms/sim_main.cpp.
Two sinks on one stream_id (sink 0 on another VLAN, so each registers on its
own Talker Advertise). The holder (a higher index) declares alone and is
ticked to QA. A walk starts (plain tx!, or txLA! after an own LeaveAll);
a few clocks in (inject@N), after the walk has passed sink 0, sink 0's talker
registers (inject@-1: before the walk, a control; inject@9999: never, a control):
sink 0 becomes the owner and takes the applicant (QA) over. The probe prints
what the walk sends for the stream and what each of the next plain ticks
sends, beside the one-applicant model's expectation.

usage: s2_probe.py <copied sim_main.cpp>
"""
import sys

path = sys.argv[1]
src = open(path).read()

decl = "  void ready_with_asking_failed_declares_ready_failed();\n"
assert src.count(decl) == 1
src = src.replace(decl, decl + "  void probe_s2(int holder, bool txla, int at);\n")

body = r'''
void SrpStreamFsmsSuite::probe_s2(int holder, bool txla, int at) {
  constexpr uint16_t VID1 = 3;
  h.reset();
  h.ctl(true, 0, SID0, DA0, VID1);
  h.ctl(true, holder, SID0, DA0, VID0);
  h.inject(true, 1, SID0, DA0, VID0, 3 /*JoinMt*/, 0, 500);
  int m = app_next(VO, eNew, false, true);
  for (int k = 0; k < 3; ++k) { h.tick(); m = app_next(m, eTx, false, true); }
  const int pre = h.l_app(holder);
  if (at < 0) h.inject(true, 1, SID0, DA0, VID1, 3 /*JoinMt*/, 0, 500);
  if (txla) h.la_own();
  h.clear_logs();
  d->join_tick_i = 1;
  bool done = false;
  for (int i = 0; i < kTxopPollSteps && !done; ++i) {
    if (i == at) {
      d->evt_valid_i = 1; d->evt_msrp_i = 1; d->evt_attr_type_i = 1;
      d->evt_stream_id_i = SID0; d->evt_da_i = DA0; d->evt_vid_i = VID1;
      d->evt_mrp_event_i = 3; d->evt_fourpacked_i = 0;
      d->evt_acc_latency_i = 500; d->evt_failure_system_id_i = 0;
      d->evt_failure_code_i = 0;
    }
    h.step();
    done = d->l_txop_done_o != 0;
  }
  h.idle(2);
  const std::string w = listener_words(h.l_push, SID0);
  const std::string want = model_words(app_msg(m, txla, false), 2);
  m = app_next(m, txla ? eTxLA : eTx, false, true);
  std::string nx[3];
  std::string nwant[3];
  for (int k = 0; k < 3; ++k) {
    h.clear_logs();
    h.tick();
    nx[k] = listener_words(h.l_push, SID0);
    nwant[k] = model_words(app_msg(m, false, false), 2);
    m = app_next(m, eTx, false, true);
  }
  // the next periodic! (QA -> AA) and its tick
  h.ptick();
  m = app_next(m, ePer, false, true);
  h.clear_logs();
  h.tick();
  const std::string pw = listener_words(h.l_push, SID0);
  const std::string pwant = model_words(app_msg(m, false, false), 2);
  printf("PROBE S2 holder=%d walk=%s inject@%d: after periodic! the tick sent '%s' (model '%s')\n",
         holder, txla ? "txLA!" : "tx!", at, pw.c_str(), pwant.c_str());
  const bool ok = (w == want) && nx[0] == nwant[0] && nx[1] == nwant[1]
                  && nx[2] == nwant[2];
  printf("PROBE S2 holder=%d walk=%s inject@%d pre=%s: walk sent '%s' (model '%s'); "
         "next ticks '%s' '%s' '%s' (model '%s' '%s' '%s'); app %s/%s decl %d/%d -> %s\n",
         holder, txla ? "txLA!" : "tx!", at, SN[pre], w.c_str(), want.c_str(),
         nx[0].c_str(), nx[1].c_str(), nx[2].c_str(), nwant[0].c_str(),
         nwant[1].c_str(), nwant[2].c_str(), SN[h.l_app(0)], SN[h.l_app(holder)],
         h.l_decl(0), h.l_decl(holder), ok ? "MATCH" : "DIFF");
}

'''
anchor = "int SrpStreamFsmsSuite::run() {"
assert src.count(anchor) == 1
src = src.replace(anchor, body + anchor)

call = "  ready_with_asking_failed_declares_ready_failed();\n\n  printf("
assert src.count(call) == 1
calls = "".join(
    f"  probe_s2({hd}, {tl}, {at});\n"
    for hd in (5, 7) for tl in ("false", "true") for at in (-1, 1, 2, 3, 9999))
src = src.replace(call, "  ready_with_asking_failed_declares_ready_failed();\n" + calls
                  + "\n  printf(")
open(path, "w").write(src)
