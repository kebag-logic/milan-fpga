// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe, round 3 (not part of the suite); run with --probe-r3.
// Needs the harness knobs and debug outputs that run_probe_r3.sh adds to a
// disposable copy of the bench (sim_main.cpp, pp_top_wrap.sv). Printed,
// never graded.
//
// E1: the aggregate's first fired clock on the binding walk's issue clock.
// The binding walk registers its READ strobe (nvm_req_o), so the strobe is
// out in the first H_RS_STREAM cycle, the cycle the arbiter takes it
// (own_r still O_NONE). The aggregate's agg_o is a registered level too.
// When agg_o first reads 1 in exactly that cycle, the walk's rs_tmo_w fires
// in H_RS_STREAM (no byte can be in hand yet) and presents nvm_abort_o in
// the arbiter's issue cycle. The probe steers the binding walk so the Nth
// binding READ strobe lands on that clock (every payload byte `g` cycles
// apart, the previous record's closing done held `delta` cycles), and runs
// the aligned boot and the boots one clock either side.
struct ProbeR3 : D3RestorePhase {
  using D3RestorePhase::D3RestorePhase;

  struct Log {
    std::vector<long> strobe;   //! loop index c of each binding READ strobe
    std::vector<long> done_at;  //! loop index c of each binding payload done
    long agg_first = -1;        //! first c with agg_o = 1
    long abort_at_agg = -1;     //! m0_abort in that cycle
    long own_at_agg = -1;       //! the arbiter's owner in that cycle
    long strobe_at_agg = -1;    //! the binding strobe in that cycle
    long hs_at_agg = -1;
    long drain_cycles = 0;      //! cycles the arbiter drained
    long done = -1, closed = -1;
    unsigned rs_cause = 9, bind_cause = 9, bind_fail = 9;
    unsigned own_end = 9, port_end = 99, hs_end = 99;
  };

  //! one boot with its per-cycle log: payload bytes `g` apart, the headers
  //! fast; the payload READ of binding region `hold_rid` ends `delta` cycles
  //! late (boot_with's loop, repeated so the log sees the cycle index)
  Log run_boot(int g, int hold_rid, long delta, long cycles) {
    fresh();
    seed_every_record();
    seed_every_binding();
    x.d->entity_enable_i = 1;
    x.d->link_up_i = 1;
    x.nv_hdr_every = 0;
    x.nv_byte_every = g;
    x.nv_hold_rid = hold_rid;
    x.nv_hold_left = delta;
    Log L;
    size_t nops = x.nvm_ops.size();
    x.d->restore_go_i = 1;
    for (long c = 0; c < cycles; ++c) {
      if (c == 5) x.d->restore_go_i = 0;
      x.step();
      const auto* d = x.d;
      if (d->dbg_r3_m0_req_o) L.strobe.push_back(c);
      while (nops < x.nvm_ops.size()) {
        const auto& o = x.nvm_ops[nops++];
        if (o.op == 0 && o.region >= 0x20 && o.region < 0x28 && o.off != 0)
          L.done_at.push_back(c);
      }
      if (L.agg_first < 0 && d->dbg_d3_agg_fired_o) {
        L.agg_first = c;
        L.abort_at_agg = d->dbg_r3_m0_abort_o;
        L.own_at_agg = d->dbg_r3_own_o;
        L.strobe_at_agg = d->dbg_r3_m0_req_o;
        L.hs_at_agg = d->dbg_r3_hs_o;
      }
      L.drain_cycles += d->dbg_nvm_drain_o ? 1 : 0;
      if (L.done < 0 && d->restore_done_o) L.done = c;
      if (L.closed < 0 && d->restore_closed_o) L.closed = c;
      if ((L.done >= 0 || L.closed >= 0) && c > std::max(L.done, L.closed) + 3000) break;
    }
    x.d->restore_go_i = 0;
    const auto* d = x.d;
    L.rs_cause = d->rs_cause_o;
    L.bind_cause = d->restore_cause_o;
    L.bind_fail = d->restore_fail_o;
    L.own_end = d->dbg_r3_own_o;
    L.port_end = d->dbg_r3_port_st_o;
    L.hs_end = d->dbg_r3_hs_o;
    x.nv_hold_rid = -1;
    x.nv_hold_left = 0;
    return L;
  }

  void print(const char* tag, int g, long delta, const Log& L) {
    printf("PROBE E1 %s: g %d, hold %ld; strobes", tag, g, delta);
    for (long s : L.strobe) printf(" %ld", s);
    printf("; payload dones");
    for (long s : L.done_at) printf(" %ld", s);
    printf("\n  agg_o first at c %ld: strobe %ld, m0_abort %ld, arbiter owner %ld "
           "(0 none, 1 binding, 2 D3), binding state %ld\n",
           L.agg_first, L.strobe_at_agg, L.abort_at_agg, L.own_at_agg, L.hs_at_agg);
    printf("  terminal: done c %ld, closed c %ld, rs_cause %u, binding fail %u cause %u; "
           "drain cycles %ld; at end owner %u, port state %u, binding state %u\n",
           L.done, L.closed, L.rs_cause, L.bind_fail, L.bind_cause, L.drain_cycles,
           L.own_end, L.port_end, L.hs_end);
  }

  //! after the boot, as D3R14: the device fast again, a READ_DESCRIPTOR,
  //! one per-wait deadline, a SET, two debounce windows: does it persist?
  void after(const char* tag) {
    x.nv_hdr_every = 0;
    x.nv_byte_every = 0;
    x.q_aecp.clear();
    x.feed(d3_read_entity_cmd(0xE1E1));
    const auto got = x.wait_any(x.q_aecp, 50);
    for (long k = 0; k < RS_TMO; ++k) x.step();
    const size_t ops1 = x.nvm_ops.size();
    const bool set = ok(AEM_SET_STREAM_INFO, D3ServicePhase::pl_ptof(0, 4747474));
    long busy = 0;
    for (long k = 0; k < 2 * WINDOW; ++k) {
      x.step();
      busy += x.d->dbg_r3_port_st_o != 0 ? 1 : 0;
    }
    int writes = 0, any = 0;
    for (size_t i = ops1; i < x.nvm_ops.size(); i++) {
      ++any;
      writes += x.nvm_ops[i].op == 1 && x.nvm_ops[i].region == 0x50;
    }
    const bool persisted = std::equal(x.nv_mem[0x50].begin(), x.nv_mem[0x50].begin() + 12,
                                      d3_record(0x50, 4747474, 4).begin());
    printf("  after %s: READ_DESCRIPTOR answered %d, AECP owned %u, ADP enable %u, SET ok %d; "
           "then %ld of %ld cycles with the port not idle, %d device ops, %d WRITEs of 0x50, "
           "record persisted %d, d3_unflushed %u, nvm_alarm %u, owner %u, port state %u\n",
           tag, got == d3_read_entity_rsp(0xE1E1) ? 1 : 0, unsigned(x.d->dbg_d3_own_o),
           unsigned(x.d->dbg_adp_enable_o), set ? 1 : 0, busy, 2 * WINDOW, any, writes,
           persisted ? 1 : 0, unsigned(x.d->d3_unflushed_o), unsigned(x.d->nvm_alarm_o),
           unsigned(x.d->dbg_r3_own_o), unsigned(x.d->dbg_r3_port_st_o));
  }

  void e1() {
    const long cyc = AGG + 3 * RS_TMO;
    const int K = 4;                       //! the binding READ to align (0-based)
    int g = 12000;
    //! calibrate the payload gap so READ K's strobe falls a few thousand
    //! cycles before agg_o, from the period of the earlier records
    Log L = run_boot(g, -1, 0, cyc);
    print("calibrate-1", g, 0, L);
    if (L.strobe.size() < 3 || L.agg_first < 0) { printf("PROBE E1: calibration failed\n"); return; }
    long P = L.strobe[2] - L.strobe[1];
    long sK = L.strobe[1] + (K - 1) * P;
    g += int((L.agg_first - 6000 - sK) / (20L * K));
    L = run_boot(g, -1, 0, cyc);
    print("calibrate-2", g, 0, L);
    if (L.strobe.size() < size_t(K) || L.done_at.size() < size_t(K)) {
      printf("PROBE E1: calibration 2 failed\n");
      return;
    }
    //! the strobe follows the previous payload done by a fixed lag
    const long lag = L.strobe[K - 1] - L.done_at[K - 2];
    const long pred = L.done_at[K - 1] + lag;
    long delta = L.agg_first - pred;
    printf("PROBE E1: lag done->next strobe %ld, predicted strobe %d at %ld, delta %ld "
           "(per-wait %ld)\n", lag, K, pred, delta, RS_TMO);
    const int hold_rid = 0x20 + (K - 1);
    for (int attempt = 0; attempt < 4; ++attempt) {
      Log A = run_boot(g, hold_rid, delta, cyc);
      const long s = A.strobe.size() > size_t(K) ? A.strobe[K] : -1;
      print("aligned?", g, delta, A);
      if (s == A.agg_first) {
        printf("PROBE E1 ALIGNED: binding READ %d strobe on agg_o's first clock %ld\n", K, s);
        after("aligned");
        for (long dd : {-1L, +1L}) {
          Log B = run_boot(g, hold_rid, delta + dd, cyc);
          const char* tag = dd < 0 ? "strobe one clock BEFORE agg_o" : "strobe one clock AFTER agg_o";
          print(tag, g, delta + dd, B);
          after(tag);
        }
        return;
      }
      if (s < 0) {
        //! the walk failed before issuing READ K: the strobe was late
        const long sd = A.done_at.size() >= size_t(K) ? A.done_at[K - 1] + lag : -1;
        printf("PROBE E1: READ %d not issued; its done %ld, predicted strobe %ld\n", K,
               A.done_at.size() >= size_t(K) ? A.done_at[K - 1] : -1, sd);
        delta -= (sd >= 0 ? sd - A.agg_first : 1);
      } else {
        delta += A.agg_first - s;
      }
    }
    printf("PROBE E1: could not align\n");
  }


  // ---- E2: the bound inside the image proof, and on the proof's own clock --
  //! A late image (loaded after the store's reset walk, as D3O4) makes the
  //! D3 walk prove it with a LOCATE that walks the store again, thousands of
  //! clocks. The binding walk (every sink saved, payload bytes `g` apart, the
  //! last record's done held) is steered so the proof lands `off` clocks
  //! after the bound's own clock: off > 0 puts the bound inside the LOCATE,
  //! 0 on the proof's own clock, -1 one clock before it.
  struct Log2 {
    long release = -1, bound = -1, proof = -1, done = -1, closed = -1;
    long agg_fired_at_proof = -1;
    int d3_reads = 0;
    unsigned rs_cause = 9, rb = 9, img = 9, own = 9, adp = 9, bind_cause = 9;
  };
  Log2 run_boot2(int g, long delta, long cycles) {
    x.dram = std::vector<uint8_t>{};
    x.erase_nvm();
    power_cycle();
    x.idle(2000);
    x.dram = image;                              //! loaded after the reset walk
    seed_every_record();
    seed_every_binding();
    x.d->entity_enable_i = 1;
    x.d->link_up_i = 1;
    x.nv_hdr_every = 0;
    x.nv_byte_every = g;
    x.nv_hold_rid = 0x27;
    x.nv_hold_left = delta;
    Log2 L;
    size_t ops0 = 0;
    x.d->restore_go_i = 1;
    for (long c = 0; c < cycles; ++c) {
      if (c == 5) x.d->restore_go_i = 0;
      x.step();
      const auto* d = x.d;
      if (L.release < 0 && d->dbg_lsn_released_o) { L.release = c; ops0 = x.nvm_ops.size(); }
      if (L.bound < 0 && d->dbg_d3_agg_o == uint32_t(AGG - 1)) L.bound = c;
      if (L.proof < 0 && d->dbg_r3_proof_o) {
        L.proof = c;
        L.agg_fired_at_proof = d->dbg_d3_agg_fired_o;
      }
      if (L.done < 0 && d->restore_done_o) L.done = c;
      if (L.closed < 0 && d->restore_closed_o) L.closed = c;
      if ((L.done >= 0 || L.closed >= 0) && c > std::max(L.done, L.closed) + 3000) break;
    }
    x.d->restore_go_i = 0;
    x.nv_byte_every = 0;
    x.nv_hold_rid = -1;
    x.nv_hold_left = 0;
    for (long k = 0; k < 2 * RS_TMO; ++k) x.step();
    if (L.release >= 0) L.d3_reads = d3_reads_of(ops0);
    const auto* d = x.d;
    L.rs_cause = d->rs_cause_o;
    L.rb = d->restore_rb_o;
    L.img = d->dbg_img_valid_o;
    L.own = d->dbg_d3_own_o;
    L.adp = d->dbg_adp_enable_o;
    L.bind_cause = d->restore_cause_o;
    return L;
  }
  void print2(const char* tag, int g, long delta, const Log2& L) {
    printf("PROBE E2 %s: g %d, hold %ld; release c %ld, bound c %ld, proof c %ld "
           "(proof - bound %ld, agg_o at the proof %ld); done c %ld, closed c %ld; "
           "rs_cause %u, rolled back %u, image valid %u, AECP owned %u, ADP enable %u, "
           "binding cause %u; D3 record READs after the release %d\n",
           tag, g, delta, L.release, L.bound, L.proof,
           (L.proof >= 0 && L.bound >= 0) ? L.proof - L.bound : -999999,
           L.agg_fired_at_proof, L.done, L.closed, L.rs_cause, L.rb, L.img, L.own, L.adp,
           L.bind_cause, L.d3_reads);
  }
  void e2() {
    const long cyc = AGG + 3 * RS_TMO;
    int g = 5800;
    Log2 L = run_boot2(g, 0, cyc);
    print2("calibrate-1", g, 0, L);
    if (L.release < 0 || L.proof < 0 || L.bound < 0) { printf("PROBE E2: calibration failed\n"); return; }
    const long loc = L.proof - L.release;         //! the proof's length from the release
    //! put the release about 8,000 clocks plus the proof before the bound, then hold
    g += int((L.bound - loc - 8000 - L.release) / (8L * 20));
    L = run_boot2(g, 0, cyc);
    print2("calibrate-2", g, 0, L);
    if (L.proof < 0 || L.bound < 0) { printf("PROBE E2: calibration 2 failed\n"); return; }
    for (long off : {std::max(2L, loc / 2), 0L, -1L}) {
      long delta = L.bound + off - L.proof;
      for (int attempt = 0; attempt < 4 && delta >= 0 && delta < RS_TMO - 200; ++attempt) {
        Log2 A = run_boot2(g, delta, cyc);
        const long got = A.proof - A.bound;
        if (got == off) {
          char tag[64];
          snprintf(tag, sizeof tag, "proof - bound = %ld", off);
          print2(tag, g, delta, A);
          break;
        }
        print2("steering", g, delta, A);
        delta += off - got;
      }
    }
  }

  void run() {
    setvbuf(stdout, nullptr, _IONBF, 0);
    if (std::getenv("PROBE_E2_ONLY") == nullptr) e1();
    e2();
  }
};
