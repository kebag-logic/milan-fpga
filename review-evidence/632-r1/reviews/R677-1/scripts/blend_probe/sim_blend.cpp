// Review probe driver: per stamped frame (domain event), the I2S frame instant
// (LRCK falling edge: left channel, MSB one SCLK later) of the I2S pair the
// merged frame carries at slot 0 (the newest I2S pair strobed before the
// close), and the TDM frame instant (fsync sampled high at a bclk rise: the
// slot-0 MSB is one bit later), each against the stamp. Several reset phases.
#include "Vblend_wrap.h"
#include "verilated.h"
#include <cmath>
#include <cstdio>
#include <vector>
int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  const double ps_ns = 1e9 / 48000.0;
  for (int k = 0; k < 6; k++) {
    Vblend_wrap* d = new Vblend_wrap;
    const double hi = 10.0, ha = 1e9 / 24.576e6 / 2.0;   // half periods, ns
    double t = 0, ni = hi, na = ha + k * 7.3;             // audio phase vs clk_i
    d->clk_i = 0; d->clk_audio_i = 0; d->rst_n = 0; d->ptp_now_i = 0; d->eval();
    double last_lrck_fall = -1, last_i2s_pv_lrck = -1, last_fsync = -1;
    int lrck_prev = 0, bclk_prev = 0;
    std::vector<double> e_i2s, e_tdm, e_solo;
    const double reset_at = 2000.0 + k * 1013.0;
    while (t < 3e6) {
      if (ni <= na) {
        t = ni; ni += hi; d->clk_i ^= 1;
        if (d->clk_i) { d->ptp_now_i = (uint64_t)std::llround(t); d->rst_n = t > reset_at; }
        d->eval();
        if (d->clk_i) {
          // an I2S pair strobe on the merged stream: remember its frame
          // KL_aaf_capture_i2s writes the pair when the right half ENDS, at the
          // LRCK fall that starts the next frame: the pair's own frame began
          // one sample period before that fall
          if (d->pv_o && d->slot_o == 0) last_i2s_pv_lrck = last_lrck_fall - ps_ns;
          // the I2S-only binding: its event against the frame it closes,
          // which began one period before the latest LRCK fall
          if (d->i2s_ev_p_o && t > 1e6 && last_lrck_fall > 0)
            e_solo.push_back((last_lrck_fall - ps_ns) - (double)d->i2s_ev_ns_o);
          if (d->ev_p_o && t > 1e6 && last_i2s_pv_lrck > 0 && last_fsync > 0) {
            const double stamp = (double)d->ev_ns_o;
            e_i2s.push_back(last_i2s_pv_lrck - stamp);
            // the TDM frame instant nearest the stamp
            e_tdm.push_back(std::remainder(last_fsync - stamp, ps_ns));
          }
        }
      } else {
        t = na; na += ha; d->clk_audio_i ^= 1; d->eval();
        if (lrck_prev && !d->i2s_lrck_o) last_lrck_fall = t;
        lrck_prev = d->i2s_lrck_o;
        if (!bclk_prev && d->tdm_bclk_o && d->tdm_fsync_o) last_fsync = t;
        bclk_prev = d->tdm_bclk_o;
      }
    }
    double mn = 1e18, mx = -1e18, tmn = 1e18, tmx = -1e18;
    for (double v : e_i2s) { mn = std::fmin(mn, v); mx = std::fmax(mx, v); }
    for (double v : e_tdm) { tmn = std::fmin(tmn, v); tmx = std::fmax(tmx, v); }
    double smn = 1e18, smx = -1e18;
    for (double v : e_solo) { smn = std::fmin(smn, v); smx = std::fmax(smx, v); }
    std::printf("reset phase %d: I2S-only binding, frame instant - its domain event: %.1f .. %.1f ns over %zu frames\n",
                k, smn, smx, e_solo.size());
    std::printf("reset phase %d: %zu frames; I2S slot-0 instant - stamp: %.1f .. %.1f ns (%.4f .. %.4f Ps, folded %.1f .. %.1f ns); "
                "TDM fsync-at-bclk-rise - stamp (folded): %.1f .. %.1f ns\n",
                k, e_i2s.size(), mn, mx, mn / ps_ns, mx / ps_ns,
                std::remainder(mn, ps_ns), std::remainder(mx, ps_ns), tmn, tmx);
    delete d;
  }
  return 0;
}
