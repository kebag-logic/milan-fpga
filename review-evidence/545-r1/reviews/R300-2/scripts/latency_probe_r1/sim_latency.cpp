// Engine-side sequence as KL_gptp_engine.sv at the pin: the level rises on
// its own write before the slew addend; completion clears it on the same
// edge as the replacement addend pulse. Nominal 8 ns/cycle; the slew
// addend is +4 ns so every slewed advance is 12 ns in integer ns.
#include "Vlatency_wrap.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  Vlatency_wrap d;
  auto edge = [&]() { d.clk = 0; d.eval(); d.clk = 1; d.eval(); };
  d.rst_n = 0; d.eng_we_i = 0; d.eng_val_i = 0; d.eng_level_i = 0;
  for (int i = 0; i < 8; ++i) edge();
  d.rst_n = 1;
  for (int i = 0; i < 8; ++i) edge();
  unsigned errors = 0, slewed = 0, slack = 0, trials = 0;
  for (int gap = 1; gap <= 6; ++gap) {           // cycles between level rise and addend write
    for (int hold = 1; hold <= 40; hold += 13) {  // cycles the slew addend is applied at the engine
      ++trials;
      uint64_t prev = d.ptp_q_o; int cyc = 0;
      // schedule: level rises at t=0, slew addend at t=gap, completion (level
      // low + integral-only addend 0) at t=gap+hold, then 20 quiet cycles
      for (int t = 0; t < gap + hold + 20; ++t) {
        d.eng_we_i = 0;
        if (t == 0) d.eng_level_i = 1;
        if (t == gap) { d.eng_we_i = 1; d.eng_val_i = 0x04000000u; }
        if (t == gap + hold) { d.eng_we_i = 1; d.eng_val_i = 0; d.eng_level_i = 0; }
        edge(); ++cyc;
        const uint64_t now = d.ptp_q_o; const uint64_t adv = now - prev; prev = now;
        const bool lvl = d.slew_q_o;
        if (adv != 8) { ++slewed; if (!lvl) { ++errors; std::printf("UNCOVERED gap=%d hold=%d t=%d adv=%llu\n", gap, hold, t, (unsigned long long)adv); } }
        else if (lvl && t > gap + hold) ++slack;  // conservative staged-high samples after the last slewed advance
      }
    }
  }
  std::printf("trials=%u slewed_samples=%u uncovered=%u clean_samples_staged_high_after_release=%u\n", trials, slewed, errors, slack);
  std::printf("RESULT: %s\n", errors == 0 && slewed > 0 ? "PASS" : "FAIL");
  return errors == 0 && slewed > 0 ? 0 : 1;
}
