  void independent_port_probes() {
    bring_the_engine_out_of_reset();
    settle_as_capable_master("probe setup");
    boot_watch = false;

    // A complete built frame stalled before SOF must not start disabled.
    pd_mode = PD_SKIP;
    dut->tx_ready_i = 0;
    for (unsigned n = 0; n < 4000000 && !dut->tx_valid_o; ++n) tick();
    expect("probe stalled frame is waiting before SOF",
           dut->tx_valid_o && dut->tx_sof_o, 1);
    const uint64_t fall = cyc;
    dut->port_enabled_i = 0;
    run(8000);
    printf("OBS stalled fall=%llu now=%llu flags=%x valid=%u sof=%u\n",
           (unsigned long long)fall, (unsigned long long)cyc,
           dut->pub_flags_o, dut->tx_valid_o, dut->tx_sof_o);
    expect("probe disabled stalled port clears asCapable within 4ms",
           dut->pub_flags_o & FL_ASCAP, 0);
    const size_t before_release = txf.size();
    dut->tx_ready_i = 1;
    run(8000);
    printf("OBS completed frames after disabled ready release=%zu\n",
           txf.size() - before_release);
    expect("probe no frame starts after disabled ready release",
           frames_started_between(fall + 16, cyc), 0);
    dut->port_enabled_i = 1;
    settle_as_capable_master("probe after stall");

    // A one-clock low pulse is shorter than any protocol beat.
    pd_mode = PD_DUAL;
    expect("probe short toggle enters cease",
           wait_flags(FL_ASCAP, 0, 16000000), 1);
    run_svc(300 * MS_CYC);
    pd_mode = PD_OFF;
    const uint64_t requests = pd_reqs_sent;
    dut->port_enabled_i = 0;
    tick();
    dut->port_enabled_i = 1;
    const uint64_t rise = cyc;
    const size_t mark = txf.size();
    expect("probe one-clock toggle resumes within 2ms",
           wait_requests(requests + 1, 2 * MS_CYC), 1);
    printf("OBS short toggle rise=%llu first_request=%llu\n",
           (unsigned long long)rise,
           (unsigned long long)request_sof(mark, 0));
    settle_as_capable_master("probe after short toggle");

    // Arm a response while enabled, deliver its Follow_Up after NOT_ENABLED.
    pd_mode = PD_SKIP;
    pd_seen = txf.size();
    tx_seen = txf.size();
    size_t idx = 0;
    auto_txts = true;
    const auto req = wait_tx(0x2, 2 * INTERVAL_CYC, &idx);
    expect("probe outstanding request exists", !req.empty(), 1);
    run(2000);
    if (!req.empty()) {
      const uint16_t seq = seq_of(req);
      const uint64_t t1 = txns[idx];
      const uint64_t t2 = peer_ns(t1 + 300);
      const uint64_t t4 = t1 + 21200;
      send_peer_response(seq, t2, t4);
      run(2000);
      dut->port_enabled_i = 0;
      run(8000);
      expect("probe unblocked fall clears asCapable",
             dut->pub_flags_o & FL_ASCAP, 0);
      const uint32_t old_delay = dut->pub_pdelay_ns_o;
      const size_t old_commits = commit_snaps.size();
      send_peer_follow_up(seq, t2 + 19800, t4 + 1000);
      run(8000);
      printf("OBS late Follow_Up seq=%u delay_before=%u delay_after=%u commits=%zu flags=%x\n",
             seq, old_delay, dut->pub_pdelay_ns_o,
             commit_snaps.size() - old_commits, dut->pub_flags_o);
      expect("probe disabled outstanding exchange cannot publish delay",
             dut->pub_pdelay_ns_o, old_delay);
      expect("probe disabled outstanding exchange cannot commit",
             commit_snaps.size(), old_commits);
    }

    // The public reset contract retains scratch, including an active cease.
    dut->port_enabled_i = 1;
    settle_as_capable_master("probe before reset");
    pd_mode = PD_DUAL;
    expect("probe reset case enters cease",
           wait_flags(FL_ASCAP, 0, 16000000), 1);
    pd_mode = PD_OFF;
    dut->port_enabled_i = 0;
    dut->rst_n = 0;
    run(8);
    dut->rst_n = 1;
    run(1300 * MS_CYC);
    const uint64_t reset_requests = pd_reqs_sent;
    dut->port_enabled_i = 1;
    const uint64_t reset_rise = cyc;
    const size_t reset_mark = txf.size();
    expect("probe first rise after disabled warm reset ends cease within interval",
           wait_requests(reset_requests + 1, INTERVAL_CYC), 1);
    printf("OBS reset rise=%llu requests_after_one_interval=%llu\n",
           (unsigned long long)reset_rise,
           (unsigned long long)(pd_reqs_sent - reset_requests));
    wait_requests(reset_requests + 1, 6 * INTERVAL_CYC);
    printf("OBS reset first_request=%llu elapsed=%llu\n",
           (unsigned long long)request_sof(reset_mark, 0),
           (unsigned long long)(request_sof(reset_mark, 0) - reset_rise));
  }
