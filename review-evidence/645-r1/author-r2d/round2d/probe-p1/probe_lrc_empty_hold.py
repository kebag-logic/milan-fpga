#!/usr/bin/env python3
"""R474-2 probe P1: a settle-recentre HOLD whose walk visits a pair that is
still empty (the walk lands between the PDU's first beat and that pair's first
commit, with nothing left of the previous PDU). The declaration says neither
SLIP_LB counter moves for the action. Patches a COPY of chmap_capture's
sim_main.cpp (argv[1]) in place: appends a case to the [LRC] block that
(a) drains the queue to zero left, (b) pulses, (c) drives ONLY the first beat
(pair 0's event), (d) runs a walk, (e) completes the PDU, and reports the dup
counter delta. A control variant without the pulse shows the same walk is a
genuine dup when no action is declared."""
import sys
from pathlib import Path
p = Path(sys.argv[1])
s = p.read_text()
anchor = '  ck("LRC: no recentre moved the dup counter"'
probe = r'''
  {
    const int S = kLrcStream;
    for (int variant = 0; variant < 2; ++variant) {
      lrc_wipe();
      lrc_align();
      drv_lb_pdu(S, 4, 6, 1);                 // primes, fill 6
      for (int i = 0; i < 6; i++) a_tick();   // e1..e6 out: nothing left
      const long dA = dut->a_dup_cnt_o;
      const long kA = dut->a_skip_cnt_o;
      if (variant == 1) lrc_pulse();          // the settle recentre arms
      dut->lb_tuser_i = S;                    // first beat only: pair 0's event
      dut->lb_tdata_i = lb_beat(LBV(S, 0, 7), LBV(S, 1, 7));
      dut->lb_tvalid_i = 1; dut->lb_tlast_i = 0; cyc();
      dut->lb_tvalid_i = 0; dut->lb_tdata_i = 0; cyc(2);
      a_tick();                               // a walk before pair 1's first commit
      std::vector<uint32_t> smp;
      for (int e = 0; e < 6; e++) for (int c = 0; c < 4; c++) smp.push_back(LBV(S, c, 7 + e));
      for (size_t i = 2; i < smp.size(); i += 2) {
        dut->lb_tdata_i = lb_beat(smp[i], smp[i + 1]);
        dut->lb_tvalid_i = 1; dut->lb_tlast_i = (i + 2 >= smp.size()); cyc(); }
      dut->lb_tvalid_i = 0; dut->lb_tlast_i = 0; dut->lb_tdata_i = 0; cyc(2);
      for (int i = 0; i < 6; i++) a_tick();
      printf("  PROBE-P1 variant %s: dup delta %ld skip delta %ld\n",
             variant ? "PULSED(hold declared)" : "CONTROL(no pulse)",
             static_cast<long>(dut->a_dup_cnt_o) - dA, static_cast<long>(dut->a_skip_cnt_o) - kA);
    }
    lrc_wipe();
  }
'''
assert s.count(anchor) == 1
s = s.replace(anchor, probe + anchor)
p.write_text(s)
print("patched", p)
