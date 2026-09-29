// ===== R401-1 reviewer probes (appended to a scratch copy of tb/maap) =====
// Tags start with "P" so they never collide with the suite's U-numbers.
// Each probe prints OBS lines (observations) and CHECKs the behaviour the
// engine documents (docs/architecture/11_maap_engine.md section 6 and the
// KL_pp_maap.sv banner), so a FAIL here is a documented-behaviour mismatch.
void MaapAnnexBSuite::r401_probes() {
  [[maybe_unused]] const uint16_t SEED = 0x2000;
  [[maybe_unused]] const uint64_t SEED_BASE = POOL_HI | SEED;
  h.addr_script.clear();
  d->cfg_count_i = COUNT;
  d->cfg_en_i = 1;
  h.confl_auto = true;
  size_t n0 = h.tx.size();

#ifndef R401_SKIP_P1  // base RTL wedges here (the defect this PR fixes)
  // ---- P1: seed re-arm after a Release! landing in generate_address ----
  // seeded walk -> conflict yield (Restart!, seed consumed) -> Release!
  // while the fresh kind-7 draw loop runs -> PortOperational!
  d->link_up_i = 0; h.idle(30);                       // Release! (from W_IDLE)
  d->cfg_seed_offset_i = SEED; d->cfg_seed_valid_i = 1;
  n0 = h.tx.size();
  d->link_up_i = 1;
  CHECK(h.wait_frames(n0 + 1, kProbeBudgetMs) && d->addr_o == SEED_BASE,
        "P1: precondition - the seeded walk probes the seed first");
  h.addr_script = {uint16_t(POOL_SIZE - 1)};          // keep the redraw loop running
  h.addr_draws = 0;
  h.rx(1, LOSE_MAC, SEED_BASE, COUNT);                // rProbe! in PROBE, we lose
  for (int g = 0; g < 400 && h.addr_draws < 2; ++g) h.step();
  printf("OBS: P1 after yield: state=%u conflicts=%u kind7-draws=%zu\n",
         unsigned(d->state_o), unsigned(d->conflicts_o), h.addr_draws);
  CHECK(h.addr_draws >= 2 && d->state_o == 0,
        "P1: precondition - yielded, generate_address redrawing");
  d->link_up_i = 0; h.idle(30);                       // Release! inside W_ADDR
  h.addr_script.clear();
  n0 = h.tx.size();
  d->link_up_i = 1;                                   // PortOperational!
  CHECK(h.wait_frames(n0 + 1, kProbeBudgetMs), "P1: the walk restarts (the fix)");
  const uint64_t p1_first = d->addr_o;
  printf("OBS: P1 first PROBE after Release! in W_ADDR: %012llx (seed %012llx)\n",
         static_cast<unsigned long long>(p1_first),
         static_cast<unsigned long long>(SEED_BASE));
  CHECK(p1_first == SEED_BASE,
        "P1: DOC11-6 'seed re-armed for the next engage' after Release! in "
        "generate_address (first PROBE %012llx, seed %012llx)",
        static_cast<unsigned long long>(p1_first),
        static_cast<unsigned long long>(SEED_BASE));

  // ---- P1c: the same sequence with the Release! landing in W_IDLE ------
  d->link_up_i = 0; h.idle(30);
  n0 = h.tx.size();
  d->link_up_i = 1;
  CHECK(h.wait_frames(n0 + 1, kProbeBudgetMs), "P1c: walk starts");
  printf("OBS: P1c first PROBE after a W_IDLE Release!: %012llx\n",
         static_cast<unsigned long long>(d->addr_o));
  h.rx(1, LOSE_MAC, d->addr_o, COUNT);                // yield (seed consumed or not)
  n0 = h.tx.size();
  CHECK(h.wait_frames(n0 + 1, kProbeBudgetMs), "P1c: fresh range probed after the yield");
  printf("OBS: P1c fresh range after the yield: %012llx\n",
         static_cast<unsigned long long>(d->addr_o));
  h.run_ms(50);                                       // steady in W_IDLE, PROBE state
  d->link_up_i = 0; h.idle(30);                       // Release! from W_IDLE
  n0 = h.tx.size();
  d->link_up_i = 1;
  CHECK(h.wait_frames(n0 + 1, kProbeBudgetMs), "P1c: walk restarts");
  printf("OBS: P1c first PROBE after yield + W_IDLE Release!: %012llx\n",
         static_cast<unsigned long long>(d->addr_o));
  CHECK(d->addr_o == SEED_BASE,
        "P1c: control - a W_IDLE Release! re-arms the seed (first PROBE %012llx)",
        static_cast<unsigned long long>(d->addr_o));
  d->cfg_seed_valid_i = 0;

#endif

  // ---- P2: a short engage fall seen in W_IDLE (link bounce of N cycles) ----
  for (int N = 1; N <= 4; ++N) {
    d->link_up_i = 0; h.idle(30);                     // clean restart
    d->link_up_i = 1;
    n0 = h.tx.size();
    CHECK(h.wait_frames(n0 + 1, kProbeBudgetMs), "P2: N=%d precondition walk", N);
    h.run_ms(20);                                     // walker parked in W_IDLE
    d->link_up_i = 0; h.idle(N);                      // Release! for N cycles
    d->link_up_i = 1;                                 // PortOperational!
    n0 = h.tx.size();
    const bool probed = h.wait_frames(n0 + 1, 2 * kProbeBudgetMs);
    printf("OBS: P2 link low for %d cycle(s) seen in W_IDLE: re-probe=%d state=%u\n",
           N, int(probed), unsigned(d->state_o));
    CHECK(probed, "P2: link low %d cycle(s): the next PortOperational! reaches "
          "ReserveAddress! (DOC11-6 'a later link rise restarts the walk')", N);
  }

  // ---- P3: Release! (cfg_en fall) while a PROBE is being built ----------
  d->link_up_i = 0; h.idle(30);
  d->cfg_en_i = 0; h.idle(10);
  d->link_up_i = 1; h.idle(5);
  n0 = h.tx.size();
  d->cfg_en_i = 1;                                    // Begin!
  h.idle(12);                                         // generate_address + interval draw
  d->cfg_en_i = 0;                                    // Release! (footnote c: no PDU)
  const uint32_t fall_ms = h.now();
  h.run_ms(50);
  printf("OBS: P3 frames after a cfg_en fall 12 cycles into the walk: %zu (fall at %u ms)\n",
         h.tx.size() - n0, unsigned(fall_ms));
  CHECK(h.tx.size() == n0,
        "P3: DOC11-6 'Release! ... no PDU': %zu frame(s) left after the engage fell",
        h.tx.size() - n0);
  d->cfg_en_i = 1;
  h.confl_auto = false;
}
