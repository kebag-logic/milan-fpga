// [R474P] reviewer probes for R474-2-F1 at the settle hold (inserted into a
// disposable copy of tb/verilator/chmap_capture/sim_main.cpp by r474_probe.py)
void ChanMapCaptureHarness::r474_probes() {
  printf("\n[R474P] reviewer probes: held walks on still-empty pairs\n");
  const int S = kLrcStream;
  // PR1: eight channels, four pairs; a walk after the decision beat finds
  // pairs 1..3 empty. Pulsed: 0 dups (declared hold). Unpulsed: 3 dups.
  lb_set_chans(S, 8);
  for (int pulse = 0; pulse < 2; ++pulse) {
    lrc_wipe(); lrc_align();
    drv_lb_pdu(S, 8, 6, 1);
    for (int i = 0; i < 6; i++) a_tick();
    if (pulse) lrc_pulse();
    std::vector<uint32_t> smp;
    for (int e = 0; e < 6; e++) for (int c = 0; c < 8; c++) smp.push_back(LBV(S, c, 7 + e));
    const long dA = dut->a_dup_cnt_o, kA = dut->a_skip_cnt_o;
    dut->lb_tuser_i = S;
    for (size_t i = 0; i < smp.size(); i += 2) {
      dut->lb_tdata_i = lb_beat(smp[i], smp[i + 1]); dut->lb_tvalid_i = 1;
      dut->lb_tlast_i = (i + 2 >= smp.size()); cyc();
      if (i == 0) { dut->lb_tvalid_i = 0; dut->lb_tdata_i = 0; cyc(2); a_tick(); }
    }
    dut->lb_tvalid_i = 0; dut->lb_tlast_i = 0; dut->lb_tdata_i = 0; cyc(2);
    const long walk = static_cast<long>(dut->a_dup_cnt_o) - dA;
    printf("R474P PR1 pulse=%d early_walk_dups=%ld\n", pulse, walk);
    ck(pulse ? "R474P PR1: 8ch pulsed early walk counts no dup"
             : "R474P PR1: 8ch unpulsed early walk counts three dups", walk, pulse ? 0 : 3);
    if (pulse) {
      for (int i = 0; i < 5; i++) a_tick();
      const long d = static_cast<long>(dut->a_dup_cnt_o) - dA;
      const long k = static_cast<long>(dut->a_skip_cnt_o) - kA;
      printf("R474P PR1 through_hold dups=%ld skips=%ld\n", d, k);
      ck("R474P PR1: no dup through the five holds", d, 0);
      ck("R474P PR1: no skip through the five holds", k, 0);
    }
  }
  // PR2: the fix must not over-suppress. Four channels, none left, pulse,
  // then only the decision beat arrives (pair 0's e7). Five held walks
  // count nothing; walk 6 pops e7 on pair 0 and starves pair 1 (+1);
  // walk 7 starves both (+2): cumulative {0,0,0,0,0,1,3}.
  lb_set_chans(S, 4);
  lrc_wipe(); lrc_align();
  drv_lb_pdu(S, 4, 6, 1);
  for (int i = 0; i < 6; i++) a_tick();
  lrc_pulse();
  const long dB = dut->a_dup_cnt_o, kB = dut->a_skip_cnt_o;
  dut->lb_tuser_i = S; dut->lb_tdata_i = lb_beat(LBV(S, 0, 7), LBV(S, 1, 7));
  dut->lb_tvalid_i = 1; dut->lb_tlast_i = 0; cyc();
  dut->lb_tvalid_i = 0; dut->lb_tdata_i = 0; cyc(2);
  const long want[7] = {0, 0, 0, 0, 0, 1, 3};
  long ok = 1;
  printf("R474P PR2 cumulative dups per walk:");
  for (int w = 0; w < 7; ++w) {
    a_tick();
    const long d = static_cast<long>(dut->a_dup_cnt_o) - dB;
    printf(" %ld", d);
    if (d != want[w]) ok = 0;
  }
  printf("\n");
  ck("R474P PR2: holds count nothing, starvation after the hold counts again", ok, 1);
  ck("R474P PR2: no skip", static_cast<long>(dut->a_skip_cnt_o) - kB, 0);
  // close the open PDU so lb_sof_r is restored, then wipe
  dut->lb_tdata_i = lb_beat(LBV(S, 2, 7), LBV(S, 3, 7)); dut->lb_tvalid_i = 1; dut->lb_tlast_i = 1; cyc();
  dut->lb_tvalid_i = 0; dut->lb_tlast_i = 0; dut->lb_tdata_i = 0; cyc(2);
  lrc_wipe();
}
