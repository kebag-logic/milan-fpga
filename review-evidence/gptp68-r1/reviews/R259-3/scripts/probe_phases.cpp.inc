  // ==== R259-3 reviewer probes, appended after the suite in a scratch copy.
  // Each starts from a warm reset, so the suite's own state only matters
  // through scratch, which survives it exactly as the ROM expects.
  static constexpr uint64_t R_PGM = 0x00D068FFFE000068ull;
  uint16_t r_aseq = 0x6800;
  uint16_t r_sseq = 0x6800;
  uint64_t r_t = 90000000000ull;

  void r_announce() { announce(r_aseq++, 0, R_PGM, 0, PEER_CID); }

  void r_pair(const char *tag, int64_t off, bool linkup, bool steps,
              int verdict_before = -1) {
    r_t += 1000000000ull;
    expect_policy_pair(tag, r_sseq++, r_t, off, linkup, steps, PEER_CID,
                       verdict_before);
  }

  //! warm reset, asCapable back, PGM adopted, one link-up slew, then one
  //! locked +30 us slew: the servo is known locked on return
  void r_start_locked(const char *tag) {
    char n[96];
    warm_reset();
    pd_mode = PD_NORMAL;
    snprintf(n, sizeof n, "%s: capable after the warm reset", tag);
    expect(n, wait_flags(FL_ASCAP, FL_ASCAP, 8000000ull), 1);
    r_announce();
    snprintf(n, sizeof n, "%s: PGM adopted", tag);
    expect(n, dut->pub_gm_id_o, R_PGM);
    snprintf(n, sizeof n, "%s: first pair, 3 us", tag);
    r_pair(n, 3000, true, false);
    snprintf(n, sizeof n, "%s: locked +30 us slews", tag);
    r_pair(n, 30000, false, false);
  }

  // P1: asCapable falls on the fourth lost response (not the delay
  // threshold the suite uses), then rises: the next pair is a link-up
  void r_probe_lost_response_fall_rearms() {
    r_start_locked("P1");
    pd_mode = PD_OFF;
    expect("P1: lost responses clear asCapable",
           wait_flags(FL_ASCAP, 0, 12000000ull), 1);
    pd_mode = PD_NORMAL;
    expect("P1: asCapable rises again",
           wait_flags(FL_ASCAP, FL_ASCAP, 8000000ull), 1);
    r_announce();
    expect("P1: still slave of PGM", dut->pub_gm_id_o, R_PGM);
    r_pair("P1: link-up after a lost-response fall, +50 us steps", 50000,
           true, true);
    r_pair("P1: then locked, +50 us slews", 50000, false, false);
  }

  // P2: the Milan 4.2.6.2.5 cease clears asCapable; after the resume the
  // ladder re-earns it: the next pair is a link-up
  void r_probe_cease_resume_rearms() {
    r_start_locked("P2");
    pd_mode = PD_DUAL;
    expect("P2: the storm ceases (asCapable falls)",
           wait_flags(FL_ASCAP, 0, 16000000ull), 1);
    pd_mode = PD_NORMAL;
    expect("P2: resumed and capable again",
           wait_flags(FL_ASCAP, FL_ASCAP, 24000000ull), 1);
    r_announce();
    expect("P2: still slave of PGM", dut->pub_gm_id_o, R_PGM);
    r_pair("P2: link-up after cease and resume, +50 us steps", 50000, true,
           true);
  }

  // P3: asCapable rises, NO pair is consumed, the plane becomes
  // grandmaster (Announce receipt timeout) and then adopts PGM with
  // asCapable held. The docs define a link-up pair as the first after
  // asCapable rises and say every consumed pair locks the servo, so this
  // first pair is still a link-up: +50 us steps
  void r_probe_rise_then_mastership_before_any_pair() {
    warm_reset();
    pd_mode = PD_NORMAL;
    expect("P3: capable after the warm reset",
           wait_flags(FL_ASCAP, FL_ASCAP, 8000000ull), 1);
    expect("P3: becomes grandmaster with no Announce",
           wait_flags(FL_AMGM, FL_AMGM, 16000000ull), 1);
    expect("P3: asCapable held while grandmaster",
           dut->pub_flags_o & FL_ASCAP, FL_ASCAP);
    r_announce();
    expect("P3: PGM adopted", dut->pub_gm_id_o, R_PGM);
    expect("P3: slave again", dut->pub_flags_o & 3, FL_PRESENT);
    r_pair("P3: first pair since the rise, after mastership, +50 us steps",
           50000, true, true);
    r_pair("P3: then locked, +50 us slews", 50000, false, false);
  }

  // P4: a lost Follow_Up (the 125 ms Follow_Up receipt timeout fires, the
  // Sync receipt timeout does not): the servo stays locked, so +50 us slews
  void r_probe_lost_follow_up_keeps_the_lock() {
    r_start_locked("P4");
    r_t += 1000000000ull;
    Frame f = ptp(0x0, r_sseq++, 0, 0x0208, 10, PEER_CID);
    f.ts(0);
    send_frame(f.b, r_t);
    run_svc(300000);                             // 150 ms: FU watch expires
    expect("P4: sync-ok still high (no Sync receipt timeout)",
           dut->pub_flags_o & FL_SYNCOK, FL_SYNCOK);
    r_pair("P4: after a lost Follow_Up, locked +50 us slews", 50000, false,
           false);
  }

  // P5: after a Sync gap (receipt timeout, asCapable held) the threshold is
  // exactly 100 us: +100 us slews, -(100 us + 1 ns) steps; and after a gap
  // plus a new grandmaster through the same parent, -100 us slews
  void r_probe_locked_boundary_after_a_gap() {
    static constexpr uint64_t R_PGM2 = 0x00D069FFFE000069ull;
    r_start_locked("P5");
    r_announce();
    expect("P5: gap 1, receipt timeout", wait_flags(FL_SYNCOK, 0, 900000ull), 1);
    expect("P5: gap 1, asCapable held", dut->pub_flags_o & FL_ASCAP, FL_ASCAP);
    r_pair("P5: after a gap, +100 us slews", 100000, false, false, 0);
    r_announce();
    expect("P5: gap 2, receipt timeout", wait_flags(FL_SYNCOK, 0, 900000ull), 1);
    r_pair("P5: after a gap, -(100 us + 1 ns) steps", -100001, false, true, 0);
    r_announce();
    expect("P5: gap 3, receipt timeout", wait_flags(FL_SYNCOK, 0, 900000ull), 1);
    announce(r_aseq++, 0, R_PGM2, 0, PEER_CID);
    expect("P5: gap 3, new grandmaster adopted", dut->pub_gm_id_o, R_PGM2);
    r_pair("P5: after a gap and a GM change, -100 us slews", -100000, false,
           false, 0);
  }
