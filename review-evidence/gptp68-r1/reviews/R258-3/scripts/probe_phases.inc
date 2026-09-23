  // ===== reviewer probe phases (R258-3), inserted into a disposable copy of
  // the head's sim_main.cpp right after phase 21. Every pair goes through
  // the suite's own expect_policy_pair, so the exact-integer mirror stays
  // in step with the plane. Names start with "PROBE" so the receipt can
  // separate them from the suite's own checks.
  uint16_t probe_aseq = 0x0900;
  uint16_t probe_sseq = 0x0900;
  uint64_t probe_t = 0;

  void probe_become_gm(const char *tag) {
    char n[128];
    // the parent re-announces a vector worse than ours: a parent update,
    // our vector wins, and the plane takes the grandmaster role at once
    announce(probe_aseq++, 250, 0xAABBCCFFFE010203ull, 0, PEER_CID);
    snprintf(n, sizeof n, "PROBE %s: plane is grandmaster", tag);
    expect(n, dut->pub_flags_o & 3, FL_PRESENT | FL_AMGM);
  }

  void probe_readopt(const char *tag) {
    char n[128];
    announce(probe_aseq++, 100, GMID, 0, PEER_CID);
    snprintf(n, sizeof n, "PROBE %s: GMID re-adopted as slave", tag);
    expect(n, (dut->pub_flags_o & 3) == FL_PRESENT &&
                  dut->pub_gm_id_o == GMID, 1);
  }

  void probe_pair(const char *tag, int64_t off, bool linkup, bool step,
                  int verdict_before = -1) {
    probe_t += 1000000000ull;
    expect_policy_pair(tag, probe_sseq++, probe_t, off, linkup, step,
                       PEER_CID, verdict_before);
  }

  void reviewer_probes() {
    char n[128];
    probe_t = TRX6 + 20000000000ull;
    // PX1: asCapable falls through allowedLostResponses (802.1AS-2011
    // 11.2.12.4), not through the delay threshold, then re-earns: the
    // first pair after the rise is a link-up (25 us steps), the next is
    // locked (50 us slews)
    {
      pd_mode = PD_OFF;
      bool fell = false;
      for (int i = 0; i < 12 && !fell; i++) {
        keep_the_gm_elected(probe_aseq++);
        fell = wait_flags(FL_ASCAP, 0, 2000000ull);
      }
      expect("PROBE PX1: asCapable fell by lost responses", fell, 1);
      expect("PROBE PX1: still slave while uncapable",
             dut->pub_flags_o & 3, FL_PRESENT);
      pd_mode = PD_NORMAL;
      keep_the_gm_elected(probe_aseq++);
      expect("PROBE PX1: asCapable re-earned",
             wait_flags(FL_ASCAP, FL_ASCAP, 8000000ull), 1);
      keep_the_gm_elected(probe_aseq++);
      probe_pair("PROBE PX1 lost-response bounce, +25 us (link-up)", 25000,
                 true, true);
      probe_pair("PROBE PX1 next pair, +50 us (locked)", 50000, false, false);
    }
    // PX2: asCapable falls and rises WHILE this plane is grandmaster; the
    // return to slave is the first synchronization after that rise, so a
    // link-up: 25 us steps
    {
      probe_become_gm("PX2");
      pd_mode = PD_FAR;
      const int base = pdm.count;
      expect("PROBE PX2: far exchange ran",
             wait_exchanges(base + 1, 4000000ull), 1);
      run(4000);
      expect("PROBE PX2: asCapable fell while grandmaster",
             dut->pub_flags_o & FL_ASCAP, 0);
      pd_mode = PD_NORMAL;
      expect("PROBE PX2: asCapable re-earned while grandmaster",
             wait_flags(FL_ASCAP, FL_ASCAP, 8000000ull), 1);
      expect("PROBE PX2: still grandmaster", dut->pub_flags_o & 3,
             FL_PRESENT | FL_AMGM);
      probe_readopt("PX2");
      probe_pair("PROBE PX2 return after a bounce while GM, +25 us (link-up)",
                 25000, true, true, 0);
    }
    // PX3: asCapable bounces as slave, and before any pair is consumed the
    // plane takes and then returns from mastership: still the first
    // synchronization after the rise, so a link-up (25 us steps)
    {
      expect("PROBE PX3: asCapable falls and rises",
             bounce_ascapable(probe_aseq), 1);
      probe_aseq = static_cast<uint16_t>(probe_aseq + 3);
      probe_become_gm("PX3");
      probe_readopt("PX3");
      probe_pair("PROBE PX3 rise, mastership, return, +25 us (link-up)",
                 25000, true, true, 0);
    }
    // PX4: the return from mastership with asCapable held, at the locked
    // threshold's edges: exactly 100 us slews, 100 us + 1 ns steps
    {
      probe_become_gm("PX4a");
      probe_readopt("PX4a");
      probe_pair("PROBE PX4 return from mastership, exactly +100 us "
                 "(locked)", 100000, false, false, 0);
      probe_become_gm("PX4b");
      probe_readopt("PX4b");
      probe_pair("PROBE PX4 return from mastership, -100 us - 1 ns "
                 "(locked)", -100001, false, true, 0);
    }
    // PX5: a receipt timeout followed by a grandmaster identity change at
    // the locked threshold's edge (the failover shape at the boundary):
    // exactly -100 us slews
    {
      const uint64_t GM_F = 0x00F0F0FFFE00000Full;
      keep_the_gm_elected(probe_aseq++);
      expect("PROBE PX5: receipt timeout",
             wait_flags(FL_SYNCOK, 0, 900000ull), 1);
      expect("PROBE PX5: asCapable held", dut->pub_flags_o & FL_ASCAP,
             FL_ASCAP);
      announce(probe_aseq++, 100, GM_F, 0, PEER_CID);
      expect("PROBE PX5: new identity adopted", dut->pub_gm_id_o, GM_F);
      probe_pair("PROBE PX5 timeout then GM change, exactly -100 us "
                 "(locked)", -100000, false, false, 0);
      probe_readopt("PX5 back");
    }
    // PX6: the same grandmaster after a Sync gap longer than the 375 ms
    // receipt timeout, asCapable held, at +90 us: locked, so it slews
    // (PX5's re-adoption above cleared sync-ok; one pair re-locks first)
    {
      keep_the_gm_elected(probe_aseq++);
      probe_pair("PROBE PX6 re-lock pair, +3 us (locked)", 3000, false, false,
                 0);
      keep_the_gm_elected(probe_aseq++);
      expect("PROBE PX6: receipt timeout, same GM",
             wait_flags(FL_SYNCOK, 0, 900000ull), 1);
      expect("PROBE PX6: asCapable held", dut->pub_flags_o & FL_ASCAP,
             FL_ASCAP);
      expect("PROBE PX6: same grandmaster", dut->pub_gm_id_o, GMID);
      probe_pair("PROBE PX6 Sync gap, same GM, +90 us (locked)", 90000, false,
                 false, 0);
    }
    snprintf(n, sizeof n, "PROBE all probe phases ran");
    expect(n, 1, 1);
  }
