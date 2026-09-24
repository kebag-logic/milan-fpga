// Reviewer-owned probes (R279-2), spliced into a scratch copy of
// tb/acmp_nvm/sim_main.cpp by apply_probes.py. Graded independently of the
// bench's own N8/N9 cases: the walk fails at the LAST sink so that every
// earlier saved sink is STORED in the shadow RAM before the reject (the
// case that discriminates the capture compare's unbound rule).
void Harness::check_r279() {
  const Bind b1{true, false, false, 0x0C01, 0x00D1D1D1D1D10001ull,
                0x00C0C0C0C0C00011ull};
  const Bind b2{true, true, true, 0x0C02, 0x00D2D2D2D2D20002ull,
                0x00C0C0C0C0C00012ull};
  const Bind nb{true, true, false, L_TKC_UID, L_TKC, L_CTLR};
  struct C { const char* tag; unsigned cause; };
  const std::vector<C> cs = {
    {"R279-FW1 torn at the last sink", 1},
    {"R279-FW2 device error at the last sink's header", 2},
    {"R279-FW3 last sink silent, ended 2000 cycles after the abort", 3},
  };
  auto seed4 = [&] { l_seed({{0, L_B0}, {1, b1}, {2, b2}, {L_LAST, L_B7}}); };
  auto fail_at_last = [&](unsigned cause) {
    if (cause == 1) arm_err(OP_READ, REC_BASE + L_LAST, 8, 3, 1);
    if (cause == 2) arm_err(OP_READ, REC_BASE + L_LAST, 0, -1, 1);
    if (cause == 3) { hold_region = REC_BASE + L_LAST; hold_mode = 2; hold_n = 2000; }
  };
  // ---- FW: read-only commands after a failed walk (every stored sink) ----
  for (const C& c : cs) {
    seed4();
    reset();
    fail_at_last(c.cause);
    l_push(M_GETRX_CMD, 1, 0x700, 0);            // held from reset
    go();
    l_finish();
    std::string why;
    bool failed = d->restore_done_o && d->restore_fail_o
               && d->restore_cause_o == c.cause
               && count_ops(OP_READ, REC_BASE + 2) >= 1;
    CHECK(failed, "%s: the walk failed with cause %u after storing sinks 0-2 "
          "(done %u fail %u cause %u)", c.tag, c.cause, unsigned(d->restore_done_o),
          unsigned(d->restore_fail_o), unsigned(d->restore_cause_o));
    disarm_err();
    for (int rep = 0; rep < 2; ++rep)
      for (int k = 0; k < N_SINKS; ++k)
        l_push(M_GETRX_CMD, k, uint16_t(0x710 + 16 * rep + k), cycles);
    l_finish();
    size_t n_get = l_resps(M_GETRX_RSP).size();
    CHECK(n_get == 1 + 2 * N_SINKS, "%s: every GET answered (%zu)", c.tag, n_get);
    CHECK(l_nvm_untouched(why) && d->dbg_dirty_o == 0,
          "%s: 17 read-only GETs after the failed walk write nothing: %s", c.tag,
          why.c_str());
    Bind want[N_SINKS];
    want[0] = L_B0; want[1] = b1; want[2] = b2; want[L_LAST] = L_B7;
    CHECK(l_round_trip(want, why), "%s: a healthy reset restores all four: %s",
          c.tag, why.c_str());
  }
  // ---- FB: a BIND then an UNBIND after a failed walk both persist ----------
  {
    const char* tag = "R279-FB BIND then UNBIND of sink 1 after a failed walk";
    std::string why;
    seed4();
    reset();
    fail_at_last(2);
    go();
    l_finish();
    disarm_err();
    CHECK(d->restore_fail_o && d->restore_cause_o == 2, "%s: walk failed", tag);
    l_push(M_BIND_RX_CMD, 1, 0x720, cycles, L_TKC, L_TKC_UID, 0);
    l_finish();
    CHECK(l_nvm_is(1, nb) && l_nvm_is(0, L_B0) && l_nvm_is(2, b2)
              && l_nvm_is(L_LAST, L_B7),
          "%s: the BIND replaced sink 1's record only", tag);
    l_push(M_UNBIND_CMD, 1, 0x721, cycles);
    l_finish();
    CHECK((store[1][8] & 1) == 0 && count_ops(OP_WRITE, REC_BASE + 1) == 2,
          "%s: the UNBIND of a live-bound sink is persisted, a second write (flags 0x%02x)", tag,
          unsigned(store[1][8]));
    Bind want[N_SINKS];
    want[0] = L_B0; want[2] = b2; want[L_LAST] = L_B7;
    CHECK(l_round_trip(want, why), "%s: reset restores 0, 2, 7 and not 1: %s", tag,
          why.c_str());
  }
  // ---- FU: decision 5, an UNBIND of a stored saved sink after a failed walk -
  {
    const char* tag = "R279-FU UNBIND of saved sink 0 after a failed walk";
    std::string why;
    seed4();
    reset();
    fail_at_last(2);
    go();
    l_finish();
    disarm_err();
    l_push(M_UNBIND_CMD, 0, 0x730, cycles);
    l_finish();
    const auto u = l_resps(M_UNBIND_RSP);
    bool ok_rsp = u.size() == 1
        && u[0].b == acmpdu(M_UNBIND_RSP, 0, L_CTLR, 0, 0, 0, 0, 0x730, 0);
    int writes = count_ops(OP_WRITE) + count_ops(OP_ERASE);
    Bind want[N_SINKS];
    want[0] = L_B0; want[1] = b1; want[2] = b2; want[L_LAST] = L_B7;
    bool back = l_round_trip(want, why);
    printf("OBSERVE %s: UNBIND answered SUCCESS %d; NVM writes+erases %d; "
           "next healthy boot restores sink 0 bound to its old talker %d\n",
           tag, int(ok_rsp), writes, int(back));
  }
  // ---- H: healthy-walk regressions of the compare --------------------------
  {
    const char* tag = "R279-H1 healthy walk, UNBIND of restored sink 0, then GETs";
    std::string why;
    seed4();
    l_boot();
    l_finish();
    CHECK(d->restore_done_o && !d->restore_fail_o, "%s: healthy walk", tag);
    l_push(M_UNBIND_CMD, 0, 0x740, cycles);
    l_push(M_GETRX_CMD, 0, 0x741, cycles);
    l_push(M_GETRX_CMD, 0, 0x742, cycles);
    l_finish();
    CHECK(!l_nvm_is(0, L_B0) && count_ops(OP_WRITE, REC_BASE + 0) == 1
              && count_ops(OP_WRITE, REC_BASE + 1) == 0,
          "%s: the UNBIND is written once, the GETs add nothing (writes %d)", tag,
          count_ops(OP_WRITE, REC_BASE + 0));
    Bind want[N_SINKS];
    want[1] = b1; want[2] = b2; want[L_LAST] = L_B7;
    CHECK(l_round_trip(want, why), "%s: reset restores 1, 2, 7, not 0: %s", tag,
          why.c_str());
  }
  {
    const char* tag = "R279-H2 healthy walk, BIND of unbound sink 3 persists";
    std::string why;
    seed4();
    l_boot();
    l_finish();
    l_push(M_BIND_RX_CMD, 3, 0x750, cycles, L_TKC, L_TKC_UID, 0);
    l_finish();
    CHECK(l_nvm_is(3, nb), "%s: sink 3 written bound", tag);
    Bind want[N_SINKS];
    want[0] = L_B0; want[1] = b1; want[2] = b2; want[3] = nb; want[L_LAST] = L_B7;
    CHECK(l_round_trip(want, why), "%s: reset restores five: %s", tag, why.c_str());
  }
}
