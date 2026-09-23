// Reviewer probe (R263-1, #74 item 2): junction counter law.
// A shared random stream of slot writes (slot 0 = frame marker, others are
// not markers) and ticks, with forced same-cycle coincidences, drives the
// head and base KL_chan_map_capture. Checked every cycle:
//  (1) head == an independent reference model of the documented head law
//      (tick consumes the pending marker, a coincidence changes nothing,
//       counts gate on "fed" = first slot-0 write, saturate at 0xFFFF);
//  (2) the net invariant at head: dup - skip == ticks - markers + pend - pend0
//      counted from the first fed marker (exact bookkeeping of ticks vs markers);
//  (3) the same invariant evaluated on base (expected to break at a
//      coincidence over a pending marker).
// usage: law <cycles> <seed> <p_marker_permille> <p_tick_permille> <p_coincide_permille>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <memory>
#include "Vlaw_wrap.h"
#include "verilated.h"

int main(int argc, char** argv) {
  if (argc < 6) return 2;
  const long cycles = atol(argv[1]);
  uint32_t rng = static_cast<uint32_t>(strtoul(argv[2], nullptr, 0));
  const uint32_t pm = atoi(argv[3]), pt = atoi(argv[4]), pc = atoi(argv[5]);
  Verilated::commandArgs(argc, argv);
  std::unique_ptr<Vlaw_wrap> d{new Vlaw_wrap};
  auto rnd = [&]() { rng ^= rng << 13; rng ^= rng >> 17; rng ^= rng << 5; return rng; };
  d->rst_n = 0; d->pv_i = 0; d->slot_i = 0; d->tick_i = 0;
  for (int i = 0; i < 4; i++) { d->clk = 0; d->eval(); d->clk = 1; d->eval(); }
  d->rst_n = 1;
  // reference model (head law)
  bool fed = false, pend = false;
  long rdup = 0, rskip = 0;
  // invariant bookkeeping from the first fed marker
  long ticks = 0, markers = 0;
  bool pend0 = false, inv_on = false;
  long head_model_mismatch = 0, head_inv_viol = 0, base_inv_viol = 0;
  long coinc = 0, coinc_pend = 0, nonzero_slot = 0;
  long base_net_err_max = 0;
  for (long c = 0; c < cycles; c++) {
    const uint32_t r = rnd() % 1000;
    bool mk = false, tk = false; unsigned slot = 0; bool pv = false;
    if (r < pc) { mk = true; tk = true; }
    else {
      mk = (rnd() % 1000) < pm;
      tk = (rnd() % 1000) < pt;
    }
    if (mk) { pv = true; slot = 0; }
    else if ((rnd() % 1000) < 20) { pv = true; slot = 1 + rnd() % 3; nonzero_slot++; }
    d->pv_i = pv; d->slot_i = slot; d->tick_i = tk;
    // model, evaluated on the pre-edge state
    const bool ev = pv && slot == 0;
    if (ev && tk) { coinc++; if (pend) coinc_pend++; fed = true; }
    else if (ev) { fed = true; if (pend && rskip != 0xFFFF) rskip++; pend = true; }
    else if (tk) { if (fed && !pend && rdup != 0xFFFF) rdup++; pend = false; }
    d->clk = 0; d->eval(); d->clk = 1; d->eval();
    if (!inv_on && ev) { inv_on = true; pend0 = false; ticks = 0; markers = 0; }
    if (inv_on) {
      // count from the edge that fed the lane (its own marker/tick included)
      if (ev) markers++;
      if (tk) ticks++;
    }
    if (d->dup_h_o != rdup || d->skip_h_o != rskip) head_model_mismatch++;
    if (inv_on && rdup < 0xFFFF && rskip < 0xFFFF) {
      const long lhs_h = static_cast<long>(d->dup_h_o) - d->skip_h_o;
      const long rhs = (ticks - markers) + (pend ? 1 : 0) - (pend0 ? 1 : 0);
      if (lhs_h != rhs) head_inv_viol++;
      const long lhs_b = static_cast<long>(d->dup_b_o) - d->skip_b_o;
      if (lhs_b != rhs) base_inv_viol++;
      base_net_err_max = std::max(base_net_err_max, std::labs(lhs_b - rhs));
    }
  }
  printf("LAW cycles=%ld pm=%u pt=%u pc=%u coincidences=%ld coincidences_over_pending=%ld "
         "nonzero_slot_writes=%ld head{dup=%u skip=%u} base{dup=%u skip=%u} "
         "head_vs_model_mismatch_cycles=%ld head_net_invariant_violations=%ld "
         "base_net_invariant_violations=%ld base_max_net_error=%ld\n",
         cycles, pm, pt, pc, coinc, coinc_pend, nonzero_slot, d->dup_h_o, d->skip_h_o,
         d->dup_b_o, d->skip_b_o, head_model_mismatch, head_inv_viol, base_inv_viol,
         base_net_err_max);
  d->final();
  return 0;
}
