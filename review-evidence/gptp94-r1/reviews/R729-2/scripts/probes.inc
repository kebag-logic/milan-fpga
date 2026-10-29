  // ---- independent reviewer probes (inserted after phase 51) -------------
  // Q1  Pdelay_Resp and its Follow_Up both heard while the port is disabled
  //     publish and commit nothing; Q1c is the same exchange with the port
  //     enabled, the positive control that the stimulus would pair.
  // Q2  a port disabled at a warm reset's release (no cease): nothing starts
  //     while disabled; the rise sends at once and the cadence then runs at
  //     one interval (Figure 11-8 pdelayIntervalTimer restarted at the send).
  // Q3  a one-cycle portEnabled glitch inside a cease ends it.
  // Q4  a warm reset inside a cease with the port ENABLED at release keeps
  //     the cease (accepted round-1 behaviour: no toggle, no exit).
  // Q5  a reply SEND issued while disabled, ready high, starts no frame.
  // Q6  a rise while a started frame is stalled: the frame completes whole,
  //     the rise's request follows it, nothing torn.
  void probe_q1(bool enabled, const char *tag) {
    char n[160];
    pd_mode = PD_NORMAL;
    snprintf(n, sizeof n, "PROBE %s: capable first", tag);
    expect(n, wait_flags(FL_ASCAP, FL_ASCAP, 8000000ull), 1);
    pd_mode = PD_SKIP;
    tx_seen = txf.size();
    size_t ri = 0;
    const bool got = !wait_tx(0x2, 2 * INTERVAL_CYC, &ri).empty();
    const uint16_t seq = got ? seq_of(txf[ri]) : 0;
    for (int k = 0; k < 4000 && txns[ri] == 0; k++) tick();
    const uint64_t t1 = txns[ri];
    const uint32_t pd0 = dut->pub_pdelay_ns_o;
    if (!enabled) dut->port_enabled_i = 0;
    run(2 * MS_CYC);
    const size_t c1 = commit_snaps.size();
    const uint64_t t2 = peer_ns(t1 + 300);
    const uint64_t t4 = t1 + 21200;
    const uint64_t t3 = t2 + 19800;
    send_peer_response(seq, t2, t4);
    send_peer_follow_up(seq, t3, t4 + 1000);
    run(4000);
    printf("PROBE %s: commits %zu, pdelay %u -> %u\n", tag,
           commit_snaps.size() - c1, pd0, (unsigned)dut->pub_pdelay_ns_o);
    if (enabled) {
      snprintf(n, sizeof n, "PROBE %s: the enabled exchange commits", tag);
      expect(n, commit_snaps.size() - c1 > 0, 1);
      snprintf(n, sizeof n, "PROBE %s: the enabled exchange moves the delay",
               tag);
      expect(n, dut->pub_pdelay_ns_o != pd0, 1);
      pd_mode = PD_NORMAL;
      run_svc(2000ull * MS_CYC);
      return;
    }
    snprintf(n, sizeof n, "PROBE %s: nothing commits while disabled", tag);
    expect(n, commit_snaps.size() - c1, 0);
    snprintf(n, sizeof n, "PROBE %s: the delay holds", tag);
    expect(n, dut->pub_pdelay_ns_o, pd0);
    run_svc(500ull * MS_CYC);
    dut->port_enabled_i = 1;
    re_earn_in_two_exchanges(tag);
  }

  void probe_q2() {
    char n[160];
    pd_mode = PD_NORMAL;
    expect("PROBE Q2: capable first",
           wait_flags(FL_ASCAP, FL_ASCAP, 8000000ull), 1);
    dut->port_enabled_i = 0;
    dut->rst_n = 0;
    for (int i = 0; i < 8; i++) tick();
    dut->rst_n = 1;
    const uint64_t rel = cyc;
    run_svc(2500ull * MS_CYC);
    expect("PROBE Q2: nothing starts while disabled after the release",
           pr_starts_between(rel, cyc), 0);
    const size_t mark = txf.size();
    const uint64_t rise = cyc;
    dut->port_enabled_i = 1;
    run_svc(4300ull * MS_CYC);
    uint64_t s[5];
    for (size_t k = 0; k < 5; k++) s[k] = request_sof(mark, k);
    printf("PROBE Q2: first request %lld cycles after the rise\n",
           (long long)(s[0] - rise));
    expect("PROBE Q2: the rise sends at once",
           s[0] != ~0ull && s[0] - rise <= 2 * MS_CYC, 1);
    for (int k = 1; k < 5; k++) {
      const long long gap = (long long)(s[k] - s[k - 1]);
      printf("PROBE Q2: request gap %d = %lld cycles (%.3f ms)\n", k, gap,
             gap / (double)MS_CYC);
      snprintf(n, sizeof n, "PROBE Q2: request gap %d is one interval", k);
      expect(n, s[k] != ~0ull && gap >= (long long)(INTERVAL_CYC - 2 * MS_CYC)
                    && gap <= (long long)(INTERVAL_CYC + 2 * MS_CYC), 1);
    }
  }

  void probe_q3() {
    pd_mode = PD_NORMAL;
    const bool capable = wait_flags(FL_ASCAP, FL_ASCAP, 8000000ull);
    pd_mode = PD_DUAL;
    expect("PROBE Q3: cease entered",
           capable && wait_flags(FL_ASCAP, 0, 16000000ull), 1);
    run_svc(1300ull * MS_CYC);
    const uint64_t r0 = pd_reqs_sent;
    pd_mode = PD_OFF;
    const uint64_t g = cyc;
    dut->port_enabled_i = 0;
    tick();
    dut->port_enabled_i = 1;
    const bool sent = wait_requests(r0 + 1, 4 * MS_CYC);
    printf("PROBE Q3: request %s, %lld cycles after the glitch\n",
           sent ? "sent" : "NOT sent", (long long)(cyc - g));
    expect("PROBE Q3: a one-cycle glitch ends the cease", sent, 1);
    re_earn_in_two_exchanges("PROBE Q3");
  }

  void probe_q4() {
    pd_mode = PD_NORMAL;
    const bool capable = wait_flags(FL_ASCAP, FL_ASCAP, 8000000ull);
    pd_mode = PD_DUAL;
    expect("PROBE Q4: cease entered",
           capable && wait_flags(FL_ASCAP, 0, 16000000ull), 1);
    run_svc(1300ull * MS_CYC);
    pd_mode = PD_OFF;
    const uint64_t r0 = pd_reqs_sent;
    dut->rst_n = 0;
    for (int i = 0; i < 8; i++) tick();
    dut->rst_n = 1;
    run_svc(1200ull * MS_CYC);
    printf("PROBE Q4: requests in 1.2 s after an enabled release: %llu\n",
           (unsigned long long)(pd_reqs_sent - r0));
    expect("PROBE Q4: an enabled release keeps the retained cease",
           pd_reqs_sent - r0, 0);
    expect("PROBE Q4: the countdown still ends it",
           wait_requests(r0 + 1, 6000ull * MS_CYC), 1);
    re_earn_in_two_exchanges("PROBE Q4");
  }

  void probe_q5() {
    pd_mode = PD_NORMAL;
    expect("PROBE Q5: capable first",
           wait_flags(FL_ASCAP, FL_ASCAP, 8000000ull), 1);
    dut->port_enabled_i = 0;
    run(2 * MS_CYC);
    const uint64_t from = cyc;
    send_peer_request(0x9705, phc() + 1000);
    run_svc(50ull * MS_CYC);
    expect("PROBE Q5: a reply SEND while disabled starts no frame",
           pr_starts_between(from, cyc), 0);
    expect("PROBE Q5: valid stays low", dut->tx_valid_o, 0);
    dut->port_enabled_i = 1;
    re_earn_in_two_exchanges("PROBE Q5");
  }

  void probe_q6() {
    pd_mode = PD_NORMAL;
    expect("PROBE Q6: capable first",
           wait_flags(FL_ASCAP, FL_ASCAP, 8000000ull), 1);
    pd_mode = PD_SKIP;
    drain_automatic_results();
    for (int j = 0; j < 40000 && (dut->dbg_busy_o || dut->tx_valid_o); j++)
      tick();
    const size_t mark = txf.size();
    const uint64_t mark_cyc = cyc;
    dut->tx_ready_i = 0;
    send_peer_request(0x9706, phc() + 1000);
    for (int j = 0; j < 200000 && !(dut->tx_valid_o && dut->tx_sof_o); j++)
      tick();
    for (int b = 0; b < 10; b++) {       // ten bytes out, then held
      dut->tx_ready_i = 1;
      tick();
      dut->tx_ready_i = 0;
    }
    dut->port_enabled_i = 0;
    run(2 * MS_CYC);
    dut->port_enabled_i = 1;
    run(5 * MS_CYC);
    const uint64_t back = cyc;
    expect("PROBE Q6: the started frame still holds the face",
           dut->tx_valid_o, 1);
    dut->tx_ready_i = 1;
    run_svc(10ull * MS_CYC);
    const int resp = find_tx(mark, 0x3, 0x9706);
    expect("PROBE Q6: the started frame completes whole",
           resp >= 0 && txf[resp].size() == 68, 1);
    const uint64_t s0 = request_sof(mark, 0);
    printf("PROBE Q6: request %lld cycles after ready returned\n",
           (long long)(s0 - back));
    expect("PROBE Q6: the rise's request follows it at once",
           s0 != ~0ull && s0 >= back && s0 - back <= 2 * MS_CYC, 1);
    expect("PROBE Q6: every started frame ended (no torn frame)",
           pr_starts_between(mark_cyc, cyc), txf.size() - mark);
    re_earn_in_two_exchanges("PROBE Q6");
  }

  //! every accepted first byte in [from, to), counted from the harness's
  //! own per-byte view, whatever the sim_main.cpp revision
  size_t pr_starts_between(uint64_t from, uint64_t to) {
    size_t k = 0;
    for (const uint64_t c : pr_starts) k += c >= from && c < to;
    return k;
  }

  void run_reviewer_probes() {
    probe_q1(true, "Q1c enabled control");
    probe_q1(false, "Q1 Resp and Follow_Up while disabled");
    probe_q2();
    probe_q3();
    probe_q4();
    probe_q5();
    probe_q6();
  }
