#!/usr/bin/env python3
"""Add one reviewer row to a scratch copy of tb/srp_encoder/sim_main.cpp.

Usage: collect_row.py SIM_MAIN  -- the row offers an absent value so that its
search ends on the clock a prepared own round's join tick leaves E_COLLECT,
the same stimulus as PV20 with the prepared round in front of it.
"""
import sys
path = sys.argv[1]
text = open(path).read()
ROW = r'''
void SrpSuite::probe_collect_start() {
  bring_out_of_reset();
  const Ev pending = mk_ev(0, 4, 1, 0, {0x06, 0x03, 0x00, 0x02});
  const Ev offered = mk_ev(0, 4, 1, 0, {0x06, 0x03, 0x00, 0x07});
  d->enc_la_prepare_i = 1;
  for (int i = 0; i < 50; ++i) { h.tick(); if (h.last_prepare_done) break; }
  d->enc_la_prepare_i = 0;
  CHECK(h.last_prepare_done, "PC the own round is prepared");
  CHECK(h.push_enc(pending), "PC a value pending");
  h.offer(offered);
  h.tick();
  d->enc_join_tick_i = 1;
  h.tick();
  d->enc_join_tick_i = 0;
  const bool taken = h.last_enc_ready;
  printf("PC taken on the start clock: %d, pending count %u\n", int(taken), unsigned(d->enc_dbg_cnt_msrp_o));
  CHECK(!taken, "PC the offer waits on the clock the prepared drain starts");
  d->enc_ev_valid_i = !taken;
  const bool frame = h.wait_and_drain(got);
  d->enc_ev_valid_i = 0;
  CHECK(frame, "PC the drain's frame captured");
  check_pdu("PC the prepared drain carries what it counted", got, model_pdu({pending}, true, OWN_MAC));
  const bool next = h.capture_pdu(0, got);
  printf("PC next frame captured: %d, pending count %u\n", int(next), unsigned(d->enc_dbg_cnt_msrp_o));
  CHECK(next, "PC the next frame captured");
  if (next) check_pdu("PC the offer rides the next MRPDU", got, model_pdu({offered}, false, OWN_MAC));
}
'''
text = text.replace("  void hold_a_push_off_its_drain_start();\n",
                    "  void hold_a_push_off_its_drain_start();\n  void probe_collect_start();\n", 1)
text = text.replace("int SrpSuite::run() {\n", ROW + "\nint SrpSuite::run() {\n", 1)
text = text.replace("  hold_a_push_off_its_drain_start();\n\n  printf(",
                    "  hold_a_push_off_its_drain_start();\n  probe_collect_start();\n\n  printf(", 1)
open(path, "w").write(text)
