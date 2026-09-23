// Reviewer probe (R263-1, issue #74 item 2): closed-loop raced-lock sweep.
//
// Drives the repository's own tb/verilator/media_grid_align wrap (the real
// KL_media_grid_align + KL_media_nco + KL_chan_map_capture) with a physical
// frame grid, engages the loop on a frame placed `lead` edges after the edge
// on which the RTL samples a tick (0 = on the tick), then enables a uniform
// 0..W edge delivery jitter and measures:
//   acquisition counts, lock-window counts, marker-to-tick clearance at lock,
//   and single real slips (held frame, surplus frames at chosen offsets from
//   the tick) injected at that lock.
// Everything is read from RTL outputs (tdm_dup_cnt_o / tdm_skip_cnt_o /
// tick_o / err_cyc_o); no internal signal is read.
//
// usage: lockprobe <lead> <jitterW> <seed> <period: plan|fast> <settle_cyc> <windows>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <climits>
#include <deque>
#include <memory>
#include <algorithm>
#include "Vmedia_grid_align_wrap.h"
#include "verilated.h"

static constexpr double kClkHz = 100e6;
static constexpr double kNominalHz = 48000.0;
static constexpr double PLAN_A = kClkHz * (391.0 / 1591.0) / 512.0;
static constexpr double kPlanPeriod = kClkHz / PLAN_A;
static constexpr double kFastPeriod = kPlanPeriod * (PLAN_A / kNominalHz) * (PLAN_A / kNominalHz);

struct Probe {
  std::unique_ptr<Vmedia_grid_align_wrap> d{new Vmedia_grid_align_wrap};
  long edge = 0;
  double period = 0.0, acc = 0.0;
  int jitW = 0;
  uint32_t rng = 1;
  std::deque<long> sched;         // edges at which a delivered marker fires
  bool surplus = false;
  bool merged = false;
  bool tick_q = false;            // tick_o after the previous edge = tick_i now
  long last_tick_edge = -1000000;
  std::deque<long> since_tick;    // marker edges since the last tick sample
  long clear_min = LONG_MAX;
  bool track = false;
  long nco_gaps = 0;              // tick intervals > 2090 edges (a dropped NCO tick)
  long last_mark_phase = -1;      // phase of the latest marker after a tick sample
  long ftrace_lo = -1, ftrace_hi = -1;   // LP_FTRACE="lo_edge,hi_edge": per-frame dump

  uint32_t rnd() { rng ^= rng << 13; rng ^= rng >> 17; rng ^= rng << 5; return rng; }

  void cyc() {
    bool reg = false;
    if (period > 0.0) {
      acc += 1.0;
      if (acc >= period) {
        acc -= period;
        long dly = jitW > 0 ? static_cast<long>(rnd() % static_cast<uint32_t>(jitW + 1)) : 0;
        sched.push_back(edge + dly);
      }
    }
    while (!sched.empty() && sched.front() <= edge) { sched.pop_front(); reg = true; }
    bool fev = reg || surplus;
    if (reg && surplus) merged = true;
    surplus = false;
    d->frame_ev_i = fev;
    d->clk = 0; d->eval();
    d->clk = 1; d->eval();
    // clearance bookkeeping at this edge: tick_i here is tick_q
    if (tick_q) {
      if (edge - last_tick_edge > 2090 && last_tick_edge > 0) nco_gaps++;
      for (long m : since_tick) {
        long dn = edge - m;
        if (track) clear_min = std::min(clear_min, dn);
      }
      since_tick.clear();
      last_tick_edge = edge;
    }
    if (fev && ftrace_lo >= 0 && edge >= ftrace_lo && edge <= ftrace_hi) {
      printf("FTRACE edge=%ld dp=%ld tick_i=%d err=%d u=%d eng=%d dup=%ld skip=%ld\n",
             edge, edge - (tick_q ? edge : last_tick_edge), tick_q ? 1 : 0,
             static_cast<int16_t>(d->err_cyc_o), static_cast<int16_t>(d->u_o), d->engaged_o,
             static_cast<long>(d->tdm_dup_cnt_o), static_cast<long>(d->tdm_skip_cnt_o));
    }
    if (fev) {
      long dp = edge - last_tick_edge;
      if (track) clear_min = std::min(clear_min, dp);
      if (dp != 0) since_tick.push_back(edge);
      last_mark_phase = dp;
    }
    tick_q = d->tick_o;
    edge++;
  }
  void run(long n) { for (long i = 0; i < n; i++) cyc(); }
  long dups() const { return d->tdm_dup_cnt_o; }
  long skips() const { return d->tdm_skip_cnt_o; }

  void reset() {
    d->rst_n = 0; d->sel_i = 0; d->frame_ev_i = 0;
    for (int i = 0; i < 8; i++) { d->clk = 0; d->eval(); d->clk = 1; d->eval(); }
    d->rst_n = 1;
  }
  // next edge samples tick_i = 1
  void to_tick() { while (!tick_q) cyc(); }
};

int main(int argc, char** argv) {
  if (argc < 7) { fprintf(stderr, "usage\n"); return 2; }
  const long lead = atol(argv[1]);
  const int jit = atoi(argv[2]);
  const uint32_t seed = static_cast<uint32_t>(strtoul(argv[3], nullptr, 0));
  const bool fast = !strcmp(argv[4], "fast");
  const long settle = atol(argv[5]);
  const int windows = atoi(argv[6]);
  Verilated::commandArgs(argc, argv);
  Probe p;
  p.rng = seed ? seed : 1;
  if (const char* ft = getenv("LP_FTRACE")) sscanf(ft, "%ld,%ld", &p.ftrace_lo, &p.ftrace_hi);
  p.reset();
  p.period = fast ? kFastPeriod : kPlanPeriod;
  p.run(3'000'000);                         // fed, deselected
  if (getenv("LP_PASS")) {
    // free-running passage (deselected), [G9]-style but with delivery
    // jitter: the marker starts `lead` edges after a tick-sampling edge and
    // drifts across the next/previous tick; count over `settle` cycles
    p.to_tick();
    p.acc = p.period - 0.5 - static_cast<double>(lead);
    p.jitW = jit;
    long pd0 = p.dups(), ps0 = p.skips();
    p.run(settle);
    printf("PASS lead=%ld jit=%d seed=0x%x rate=%s dups=%ld skips=%ld net=%ld nco_gaps=%ld\n",
           lead, jit, seed, fast ? "fast" : "plan", p.dups() - pd0, p.skips() - ps0,
           (p.dups() - pd0) - (p.skips() - ps0), p.nco_gaps);
    p.d->final();
    return 0;
  }
  // aim: the next frame lands `lead` edges after a tick-sampling edge
  p.to_tick();
  p.acc = p.period - 0.5 - static_cast<double>(lead);
  p.run(lead);
  p.d->sel_i = 1;
  long d0 = p.dups(), s0 = p.skips();
  const long e_eng = p.edge;
  p.cyc();
  const int eng = p.d->engaged_o;
  const long eng_phase = p.edge - 1 - p.last_tick_edge;
  (void)e_eng;
  p.jitW = jit;
  if (getenv("LP_TRACE")) {
    // err / u / counts every 10 ms through the settle interval
    for (long t = 0; t < settle; t += 1'000'000) {
      p.run(1'000'000);
      printf("TRACE t_ms=%ld err=%d u=%d dup=%ld skip=%ld\n", (t + 1'000'000) / 100'000,
             static_cast<int16_t>(p.d->err_cyc_o), static_cast<int16_t>(p.d->u_o),
             p.dups() - d0, p.skips() - s0);
    }
  } else {
    p.run(settle);
  }
  long acq_d = p.dups() - d0, acq_s = p.skips() - s0;
  const long gaps_acq = p.nco_gaps;
  // lock windows
  p.track = true; p.clear_min = LONG_MAX;
  d0 = p.dups(); s0 = p.skips();
  long wmax = 0;
  char wlog[4096]; size_t wl = 0; wlog[0] = 0;
  for (int w = 0; w < windows; w++) {
    long wd = p.dups(), ws = p.skips();
    long wc0 = p.clear_min; p.clear_min = LONG_MAX;
    p.run(20'000'000);
    wmax = std::max(wmax, (p.dups() - wd) + (p.skips() - ws));
    if (wl < sizeof(wlog) - 64)
      wl += snprintf(wlog + wl, sizeof(wlog) - wl, " w%d=%ld/%ld:e%d:c%ld", w, p.dups() - wd,
                     p.skips() - ws, static_cast<int16_t>(p.d->err_cyc_o), p.clear_min);
    p.clear_min = std::min(p.clear_min, wc0);
  }
  long lock_d = p.dups() - d0, lock_s = p.skips() - s0;
  long clr = p.clear_min;
  const long gaps_lock = p.nco_gaps - gaps_acq;
  const long L = p.last_mark_phase;
  int err = static_cast<int16_t>(p.d->err_cyc_o);
  p.track = false;
  // held frame
  d0 = p.dups(); s0 = p.skips();
  p.acc -= p.period;
  p.run(1'000'000);
  long hd = p.dups() - d0, hs = p.skips() - s0;
  // surplus frames at offsets from the tick-sampling edge
  const long offs[] = {0, 1, 2, 8, 12, 20, 520, 1041, 1600, 2060, 2075, 2082};
  printf("RES lead=%ld eng=%d eng_phase=%ld jit=%d seed=0x%x rate=%s acq=%ld/%ld lock=%ld/%ld wmax=%ld clr=%ld err=%d held=%ld/%ld",
         lead, eng, eng_phase, jit, seed, fast ? "fast" : "plan", acq_d, acq_s, lock_d, lock_s, wmax, clr, err, hd, hs);
  printf(" [%s ] nco_gaps acq=%ld lock=%ld lockphase=%ld", wlog, gaps_acq, gaps_lock, L);
  int bad_sur = 0;
  for (long o : offs) {
    d0 = p.dups(); s0 = p.skips();
    p.to_tick();
    p.run(o);
    p.merged = false;
    p.surplus = true;
    p.cyc();
    bool m = p.merged;
    p.run(1'000'000);
    long sd = p.dups() - d0, ss = p.skips() - s0;
    // a surplus marker about half a sample from the lock phase sits on the
    // unwrapper's +/-DIV/2 fold boundary (pre-existing; not this diff)
    long rel = ((o - L) % 2083 + 2083) % 2083;
    bool ambig = std::labs(rel - 1041) < 60;
    printf(" sur@%ld=%ld/%ld%s%s", o, sd, ss, m ? "(merged)" : "", ambig ? "(ambig)" : "");
    if (!m && !ambig && !(sd == 0 && ss == 1)) bad_sur++;
  }
  const bool ok = eng == 1 && lock_d == 0 && lock_s == 0 && clr >= 12 && hd == 1 && hs == 0 && bad_sur == 0;
  printf(" engaged_end=%d VERDICT=%s\n", p.d->engaged_o, ok ? "CLEAN" : "COUNTS");
  p.d->final();
  return 0;
}
