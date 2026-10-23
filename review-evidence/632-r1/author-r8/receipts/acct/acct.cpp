// Scratch: the base KL_crf_tx event divider against the TDM8 master's frame grid at the pins.
#include "Vacct_wrap.h"
#include "verilated.h"
#include <cmath>
#include <cstdio>
#include <cstdint>
#include <vector>
#include <algorithm>
int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  auto* d = new Vacct_wrap;
  const double ps = 1e9 / 48000.0;
  double rels[] = {0.0, 0.37, 0.71};   // reset release phase vs the audio clock, fraction of an audio cycle
  for (double rel : rels) {
    const double ha = 0.5e15 / (24.576e6 * (1 - 10.64e-6)), hi = 0.5e15 / 50e6;
    double t = 0, na = ha * (1 + rel), ni = hi;
    d->rst_n = 0; d->clk_i = 0; d->clk_audio_i = 0; d->eval();
    std::vector<double> sync; std::vector<uint8_t> by; int pb = 0; long npts = 0; double mx = -1e9, mn = 1e9;
    while (t < 30e12) {  // 30 ms
      if (ni <= na) { t = ni; ni += hi; d->clk_i ^= 1; if (d->clk_i) d->ptp_now_i = (uint64_t)(t / 1e6) + 1000000000ULL; d->eval();
        if (t > 5e9 && !d->rst_n && d->clk_i) d->rst_n = 1;
        if (d->clk_i && d->tvalid_o) { for (int l = 0; l < 8; l++) by.push_back((d->tdata_o >> (8*l)) & 0xff);
          if (d->tlast_o) { if (by.size() >= 42) { uint64_t ts = 0; for (int k = 34; k < 42; k++) ts = (ts << 8) | by[k];
              double inst = (double)ts - 2e6 - 1e9; double best = 1e18, sgn = 0;
              for (double s : sync) { double r = std::fmod(inst - s, ps); if (r < 0) r += ps; if (r >= ps/2) r -= ps; if (std::fabs(r) < best) { best = std::fabs(r); sgn = r; } }
              npts++; mx = std::max(mx, sgn); mn = std::min(mn, sgn); }
            by.clear(); } } }
      else { t = na; na += ha; d->clk_audio_i ^= 1; d->eval();
        if (d->clk_audio_i) { if (d->bclk_o && !pb && d->fsync_o) sync.push_back(t / 1e6); pb = d->bclk_o; } }
    }
    std::printf("release phase %.2f: %ld old CRF timing points; old CRF event - nearest frame sync rise at the pins: %+.1f .. %+.1f ns (%+.4f .. %+.4f Ps)\n",
                rel, npts, mn, mx, mn / ps, mx / ps);
  }
  delete d; return 0;
}
