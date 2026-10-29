  //! D: a warm reset inside the cease, the port low at release, then a rise
  void r729_probe_warm_reset_port_low(bool low_at_release, const char *tag) {
    char n[128];
    pd_mode = PD_NORMAL;
    const bool capable = wait_flags(FL_ASCAP, FL_ASCAP, 8000000ull);
    pd_mode = PD_DUAL;
    snprintf(n, sizeof n, "%s: the cease", tag);
    expect(n, capable && wait_flags(FL_ASCAP, 0, 16000000ull), 1);
    run_svc(1300ull * MS_CYC);
    dut->rst_n = 0;
    if (low_at_release) dut->port_enabled_i = 0;
    for (int i = 0; i < 8; i++) tick();
    dut->rst_n = 1;
    if (!low_at_release) {
      run_svc(4);
      dut->port_enabled_i = 0;
    }
    pd_mode = PD_NORMAL;
    run_svc(200ull * MS_CYC);
    const uint64_t r0 = pd_reqs_sent;
    const size_t mark = txf.size();
    dut->port_enabled_i = 1;
    const uint64_t rise = cyc;
    const bool ok = wait_requests(r0 + 1, 6 * INTERVAL_CYC);
    const uint64_t s0 = request_sof(mark, 0);
    printf("%s: first request %llu ms after the rise\n", tag,
           ok ? (unsigned long long)((s0 - rise) / MS_CYC) : 999999ull);
    snprintf(n, sizeof n, "%s: the rise ends the cease within one interval",
             tag);
    expect(n, ok && s0 - rise <= INTERVAL_CYC, 1);
    wait_flags(FL_ASCAP, FL_ASCAP, 8000000ull);
  }
