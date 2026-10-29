  // ---- reviewer probes (R729), appended after phase 47 -------------------
  //! A: the port falls between a Pdelay_Resp and its Follow_Up
  void r729_probe_fu_after_fall() {
    pd_mode = PD_NORMAL;
    expect("R729 A: capable first",
           wait_flags(FL_ASCAP, FL_ASCAP, 8000000ull), 1);
    pd_mode = PD_SKIP;
    tx_seen = txf.size();
    size_t ri = 0;
    const bool got = !wait_tx(0x2, 2 * INTERVAL_CYC, &ri).empty();
    for (int k = 0; k < 4000 && got && txns[ri] == 0; k++) tick();
    const uint16_t seq = seq_of(txf[ri]);
    const uint64_t t1 = txns[ri];
    const uint64_t t2 = peer_ns(t1 + 300), t3 = t2 + 20000, t4 = t1 + 21200;
    Frame f = ptp(0x3, seq, 0, 0x0200, 20);
    f.ts(t2); f.u64(OUR_CID); f.u16(1);
    send_frame(f.b, t4);
    run(400);
    const size_t c0 = commit_snaps.size();
    const uint32_t pd0 = dut->pub_pdelay_ns_o;
    dut->port_enabled_i = 0;
    run(4000);
    const size_t c1 = commit_snaps.size();
    expect("R729 A: the fall commits", c1 > c0, 1);
    Frame g = ptp(0xA, seq, 0, 0x0000, 20);
    g.ts(t3 - 200); g.u64(OUR_CID); g.u16(1);   // a pairing publishes ~700
    send_frame(g.b, t4 + 1000);
    run(4000);
    printf("R729 A: pdelay before %u after %u; commits after the FU %zu\n",
           pd0, (unsigned)dut->pub_pdelay_ns_o, commit_snaps.size() - c1);
    expect("R729 A: a Follow_Up heard while disabled commits nothing",
           commit_snaps.size() - c1, 0);
    expect("R729 A: a Follow_Up heard while disabled leaves the delay",
           dut->pub_pdelay_ns_o, pd0);
    run(500ull * MS_CYC);
    dut->port_enabled_i = 1;
    re_earn_in_two_exchanges("R729 A");
  }

  //! B: one- and three-cycle portEnabled glitches inside the cease
  void r729_probe_glitch(unsigned width, const char *tag) {
    char n[112];
    pd_mode = PD_NORMAL;
    const bool capable = wait_flags(FL_ASCAP, FL_ASCAP, 8000000ull);
    pd_mode = PD_DUAL;
    snprintf(n, sizeof n, "%s: the cease", tag);
    expect(n, capable && wait_flags(FL_ASCAP, 0, 16000000ull), 1);
    run_svc(1300ull * MS_CYC);
    pd_mode = PD_OFF;
    const uint64_t r0 = pd_reqs_sent;
    const size_t mark = txf.size();
    const size_t c0 = commit_snaps.size();
    dut->port_enabled_i = 0;
    run(width);
    dut->port_enabled_i = 1;
    const uint64_t rise = cyc;
    const bool one = wait_requests(r0 + 1, INTERVAL_CYC);
    const uint64_t s0 = request_sof(mark, 0);
    printf("%s: request %d at +%llu cycles, commits %zu\n", tag, one,
           (unsigned long long)(s0 - rise), commit_snaps.size() - c0);
    snprintf(n, sizeof n, "%s: a request at once after the glitch", tag);
    expect(n, one && s0 - rise <= 2 * MS_CYC, 1);
    wait_requests(r0 + 3, 3 * INTERVAL_CYC);
    const uint64_t s1 = request_sof(mark, 1), s2 = request_sof(mark, 2);
    snprintf(n, sizeof n, "%s: then one per interval", tag);
    expect(n, s1 - s0 >= INTERVAL_CYC - MS_CYC && s1 - s0 <= INTERVAL_CYC +
              MS_CYC && s2 - s1 >= INTERVAL_CYC - MS_CYC &&
              s2 - s1 <= INTERVAL_CYC + MS_CYC, 1);
    re_earn_in_two_exchanges(tag);
  }

  //! C: the rise lands near the cadence timer's own expiry
  void r729_probe_rise_near_the_beat() {
    pd_mode = PD_NORMAL;
    wait_flags(FL_ASCAP, FL_ASCAP, 8000000ull);
    int doubles = 0, iters = 0, missing = 0;
    tx_seen = txf.size();
    size_t ri = 0;
    wait_tx(0x2, 2 * INTERVAL_CYC, &ri);
    uint64_t s = txsof[ri];
    for (int off = -400; off <= 200; off += 4) {
      iters++;
      run_svc(s + 500ull * MS_CYC - cyc);
      dut->port_enabled_i = 0;
      const int64_t to = (int64_t)(s + INTERVAL_CYC) + off - (int64_t)cyc;
      run_svc(to > 0 ? (uint64_t)to : 1);
      const uint64_t rise = cyc;
      const size_t mark = txf.size();
      dut->port_enabled_i = 1;
      run_svc(400ull * MS_CYC);
      size_t reqs = 0;
      uint64_t first = ~0ull;
      for (size_t i = mark; i < txf.size(); i++)
        if (type_of(txf[i]) == 0x2) {
          if (!reqs) first = txsof[i];
          reqs++;
        }
      if (reqs != 1) {
        printf("R729 C: off %d: %zu requests in 400 ms after the rise\n",
               off, reqs);
        doubles += reqs > 1;
        missing += reqs == 0;
      }
      if (first == ~0ull) break;
      s = first;
    }
    printf("R729 C: %d offsets, %d with two or more requests, %d with none\n",
           iters, doubles, missing);
    expect("R729 C: one request per rise at every offset", doubles + missing,
           0);
  }
