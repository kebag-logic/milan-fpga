#!/usr/bin/env python3
"""Add one reviewer row to a scratch sim_main.cpp: an offer whose search ends on
the clock la_prepare_i arrives in E_IDLE, then the prepared round's frame."""
import sys
path = sys.argv[1]
text = open(path).read()
ROW = r'''
void SrpSuite::probe_prepare_start() {
  bring_out_of_reset();
  const Ev pending = mk_ev(0, 4, 1, 0, {0x06, 0x03, 0x00, 0x02});
  const Ev offered = mk_ev(0, 4, 1, 0, {0x06, 0x03, 0x00, 0x07});
  CHECK(h.push_enc(pending), "PQ a value pending");
  h.offer(offered);
  h.tick();
  d->enc_la_prepare_i = 1;
  h.tick();
  const bool taken = h.last_enc_ready;
  printf("PQ taken on the prepare clock: %d, pending count %u\n", int(taken), unsigned(d->enc_dbg_cnt_msrp_o));
  if (taken) d->enc_ev_valid_i = 0;
  for (int i = 0; i < 50; ++i) { if (h.last_prepare_done) break; h.tick(); }
  d->enc_la_prepare_i = 0;
  CHECK(h.last_prepare_done, "PQ the own round is prepared");
  for (int i = 0; i < 40 && d->enc_ev_valid_i; ++i) { h.tick(); if (h.last_enc_ready) d->enc_ev_valid_i = 0; }
  CHECK(d->enc_dbg_cnt_msrp_o == 2, "PQ both values pending (%u)", unsigned(d->enc_dbg_cnt_msrp_o));
  CHECK(h.capture_pdu(0, got), "PQ the prepared frame captured");
  check_pdu("PQ the prepared frame carries both values", got, model_pdu({pending, offered}, true, OWN_MAC));
}
'''
text = text.replace("  void hold_a_push_off_its_drain_start();\n",
                    "  void hold_a_push_off_its_drain_start();\n  void probe_prepare_start();\n", 1)
text = text.replace("int SrpSuite::run() {\n", ROW + "\nint SrpSuite::run() {\n", 1)
text = text.replace("  hold_a_push_off_its_drain_start();\n\n  printf(",
                    "  hold_a_push_off_its_drain_start();\n  probe_prepare_start();\n\n  printf(", 1)
open(path, "w").write(text)
