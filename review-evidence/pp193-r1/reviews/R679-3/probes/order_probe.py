#!/usr/bin/env python3
"""Order probe: does any Listener push follow the walk's done strobe?

Inserts one probe method into a COPY of tb/srp_stream_fsms/sim_main.cpp.
KL_srp_top drains the encoder on the two txop_done strobes, and the encoder
snapshots its pending count when the drain starts, so a push after the
strobe misses that cadence's MRPDU (port comment of txop_done_o: "tick walk
finished, pushes accepted"). A taker (sink 0, 2 or 4, VLAN 3, its talker
silent) and holder 7 (VLAN 2) settle on one stream_id; holder 7 declares
alone and is ticked to QA (txLA! walk) or AN (tx! walk). At clock `at` of
the walk the taker's talker registers: the taker becomes the owner and takes
the applicant over, behind the walk when the walk has passed it. The probe
steps 60 clocks past the first done strobe with no other input and counts
Listener pushes after it. Every row must report late 0.

usage: order_probe.py <copied sim_main.cpp>
"""
import sys

path = sys.argv[1]
src = open(path).read()

decl = "  void ready_with_asking_failed_declares_ready_failed();\n"
assert src.count(decl) == 1
src = src.replace(decl, decl + "  int probe_order(int taker, bool txla, int at);\n")

body = r'''
int SrpStreamFsmsSuite::probe_order(int taker, bool txla, int at) {
  constexpr uint16_t VT = 3;
  h.reset();
  h.ctl(true, taker, SID0, DA0, VT);
  h.ctl(true, 7, SID0, DA0, VID0);
  h.inject(true, 1, SID0, DA0, VID0, 3 /*JoinMt*/, 0, 500);
  for (int k = 0; k < (txla ? 3 : 1); ++k) h.tick();
  if (txla) h.la_own();
  h.clear_logs();
  d->join_tick_i = 1;
  int done_at = -1;
  size_t pushes_at_done = 0;
  for (int i = 0; i < kTxopPollSteps; ++i) {
    if (i == at) {
      d->evt_valid_i = 1; d->evt_msrp_i = 1; d->evt_attr_type_i = 1;
      d->evt_stream_id_i = SID0; d->evt_da_i = DA0; d->evt_vid_i = VT;
      d->evt_mrp_event_i = 3; d->evt_fourpacked_i = 0;
      d->evt_acc_latency_i = 500; d->evt_failure_system_id_i = 0;
      d->evt_failure_code_i = 0;
    }
    h.step();
    if (done_at < 0 && d->l_txop_done_o) { done_at = i; pushes_at_done = h.l_push.size(); }
    if (done_at >= 0 && i >= done_at + 60 && i > at) break;
  }
  const size_t late = h.l_push.size() - pushes_at_done;
  printf("PROBE ORDER taker=%d walk=%s inject@%d: done at clock %d, pushes before %zu, "
         "after %zu, owner app %s -> %s\n", taker, txla ? "txLA!" : "tx!", at, done_at,
         pushes_at_done, late, SN[h.l_app(taker)],
         (done_at >= 0 && late == 0) ? "OK" : "LATE");
  return (done_at >= 0 && late == 0) ? 0 : 1;
}

'''
anchor = "int SrpStreamFsmsSuite::run() {"
assert src.count(anchor) == 1
src = src.replace(anchor, body + anchor)

call = "  ready_with_asking_failed_declares_ready_failed();\n\n  printf("
assert src.count(call) == 1
calls = (
    "  {\n    int late = 0, rows = 0;\n"
    "    for (int taker : {0, 2, 4})\n"
    "      for (int tl = 0; tl < 2; ++tl)\n"
    "        for (int at = 1; at <= 12; ++at) { late += probe_order(taker, tl != 0, at); ++rows; }\n"
    "    printf(\"PROBE ORDER SUMMARY rows %d LATE %d\\n\", rows, late);\n  }\n")
src = src.replace(call, "  ready_with_asking_failed_declares_ready_failed();\n" + calls
                  + "\n  printf(")
open(path, "w").write(src)
