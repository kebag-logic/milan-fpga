// Reviewer probe (R263-1, #74 item 2): is a non-raced engagement
// bit-identical to the base revision, and is a raced one pulled by at most
// the keep-off? Two closed loops share one frame marker; for every
// engagement phase 0..2083 (in edges after the tick-sampling edge) both are
// reset, engaged on the same frame, and compared cycle by cycle (tick, u,
// err, engaged) for `frames` frame periods.
// usage: equiv <plan|fast> <frames> <jitterW> [phase_lo phase_hi]
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <memory>
#include <algorithm>
#include "Vequiv_wrap.h"
#include "verilated.h"

static constexpr double kClkHz = 100e6;
static constexpr double kNominalHz = 48000.0;
static constexpr double PLAN_A = kClkHz * (391.0 / 1591.0) / 512.0;
static constexpr double kPlanPeriod = kClkHz / PLAN_A;
static constexpr double kFastPeriod = kPlanPeriod * (PLAN_A / kNominalHz) * (PLAN_A / kNominalHz);

int main(int argc, char** argv) {
  if (argc < 4) return 2;
  const bool fast = !strcmp(argv[1], "fast");
  const long frames = atol(argv[2]);
  const int jit = atoi(argv[3]);
  const long lo = argc > 5 ? atol(argv[4]) : 0;
  const long hi = argc > 5 ? atol(argv[5]) : 2083;
  Verilated::commandArgs(argc, argv);
  std::unique_ptr<Vequiv_wrap> d{new Vequiv_wrap};
  const double period = fast ? kFastPeriod : kPlanPeriod;
  uint32_t rng = 0x74A197u;
  long n_ident = 0, n_div = 0, div_lo_max = -1, div_hi_min = 1 << 30;
  long max_first_derr = 0;
  long ident_but_raced = 0;
  for (long lead = lo; lead <= hi; lead++) {
    double acc = 0.0;
    long pend_edge = -1, edge = 0;
    bool tick_q = false;
    auto cyc = [&](bool feed) -> bool {
      bool fev = false;
      if (feed) {
        acc += 1.0;
        if (acc >= period) {
          acc -= period;
          long dly = jit > 0 ? static_cast<long>((rng ^= rng << 13, rng ^= rng >> 17, rng ^= rng << 5) % (jit + 1)) : 0;
          if (dly == 0) fev = true; else pend_edge = edge + dly;
        }
        if (pend_edge == edge) { fev = true; pend_edge = -1; }
      }
      d->frame_ev_i = fev;
      d->clk = 0; d->eval(); d->clk = 1; d->eval();
      tick_q = d->tick_h_o;
      edge++;
      return fev;
    };
    d->rst_n = 0; d->sel_i = 0; d->frame_ev_i = 0;
    for (int i = 0; i < 8; i++) { d->clk = 0; d->eval(); d->clk = 1; d->eval(); }
    d->rst_n = 1;
    for (int i = 0; i < 5000; i++) cyc(false);
    while (!tick_q) cyc(false);
    acc = period - 0.5 - static_cast<double>(lead);
    for (long i = 0; i < lead; i++) cyc(true);
    d->sel_i = 1;
    cyc(true);                                  // the engaging frame
    const long total = static_cast<long>(frames * period);
    long first_div = -1;
    long first_derr = 0;
    bool seen_frame_after = false;
    for (long i = 0; i < total; i++) {
      bool fev = cyc(true);
      if (fev && !seen_frame_after) {
        seen_frame_after = true;
        first_derr = static_cast<int16_t>(d->err_h_o) - static_cast<int16_t>(d->err_b_o);
      }
      if (first_div < 0 && (d->tick_h_o != d->tick_b_o || d->u_h_o != d->u_b_o ||
                            d->err_h_o != d->err_b_o || d->eng_h_o != d->eng_b_o))
        first_div = i;
    }
    const bool raced = (lead < 16) || (lead > 2067);
    if (first_div < 0) {
      n_ident++;
      if (raced) ident_but_raced++;
    } else {
      n_div++;
      if (lead < 1041) div_lo_max = std::max(div_lo_max, lead);
      else div_hi_min = std::min(div_hi_min, lead);
      max_first_derr = std::max(max_first_derr, std::labs(first_derr));
      printf("DIVERGE lead=%ld first_div_edge=%ld first_frame_err_head_minus_base=%ld\n",
             lead, first_div, first_derr);
    }
  }
  printf("SUMMARY rate=%s frames=%ld jit=%d phases=%ld..%ld identical=%ld diverged=%ld "
         "diverged_low_max=%ld diverged_high_min=%ld max_abs_first_err_delta=%ld "
         "identical_but_in_clamp_band=%ld\n",
         fast ? "fast" : "plan", frames, jit, lo, hi, n_ident, n_div, div_lo_max,
         div_hi_min == (1 << 30) ? -1 : div_hi_min, max_first_derr, ident_but_raced);
  d->final();
  return 0;
}
