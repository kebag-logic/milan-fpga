// Reviewer probe (PR #631, head c554ae51): does a restart request raised a few
// cycles after a media-clock source change put a second mr toggle on the wire?
// Drives the unmodified hdl/ieee1722/avtp/KL_media_clock_restart.sv with two
// streaming talkers. Each talker starts a PDU every PER cycles (talker 1 is
// offset by PER/2); the PDU carries mr_o sampled at its start and is reported
// LAT cycles later through frame_p_i/frame_mr_i. A wire toggle is a change of
// the reported level between consecutive PDUs of one talker.
#include "VKL_media_clock_restart.h"
#include "verilated.h"
#include <cstdio>
#include <vector>

static const int PER = 1000, LAT = 40, SWITCH_AT = 20'000 + 137;

static int run(const char* name, std::vector<long> restart_at) {
  VKL_media_clock_restart d;
  d.clk_i = 0; d.rst_n = 0; d.restart_p_i = 0; d.clk_src_i = 0;
  d.streaming_i = 3; d.frame_p_i = 0; d.frame_idx_i = 0; d.frame_mr_i = 0;
  int pend_mr[2] = {0, 0}; long pend_done[2] = {-1, -1};
  int last[2] = {-1, -1}, toggles[2] = {0, 0};
  for (long cyc = 0; cyc < 60'000; ++cyc) {
    d.rst_n = cyc >= 4;
    d.clk_src_i = cyc >= SWITCH_AT ? 2 : 0;            // SET_CLOCK_SOURCE 0 -> 2
    d.restart_p_i = 0;
    for (long r : restart_at) if (cyc == SWITCH_AT + r) d.restart_p_i = 1;
    d.frame_p_i = 0;
    for (int t = 0; t < 2; ++t) {
      if (pend_done[t] == cyc) {                       // report the PDU
        d.frame_p_i = 1; d.frame_idx_i = t; d.frame_mr_i = pend_mr[t];
        if (last[t] >= 0 && pend_mr[t] != last[t]) ++toggles[t];
        last[t] = pend_mr[t]; pend_done[t] = -1;
      }
    }
    for (int t = 0; t < 2; ++t)                        // start a PDU
      if (cyc > 10 && (cyc + t * PER / 2) % PER == 0) {
        pend_mr[t] = (d.mr_o >> t) & 1; pend_done[t] = cyc + LAT;
      }
    d.clk_i = 0; d.eval(); d.clk_i = 1; d.eval();
  }
  printf("%-58s toggles talker0=%d talker1=%d\n", name, toggles[0], toggles[1]);
  return toggles[0] + toggles[1];
}

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  int a = run("source change only (the design)", {});
  int b = run("source change + request at +2 cycles", {2});
  int c = run("source change + request at +3 cycles (era-start fall)", {3});
  int e = run("source change + request at +5 cycles", {5});
  int f = run("source change + request at +30 cycles", {30});
  int g = run("source change + request at +600 cycles (late first PDU)", {600});
  int h = run("source change + request at +1,600 cycles", {1600});
  printf("RESULT design=%d early_requests=%d,%d,%d,%d late_requests=%d,%d\n",
         a, b, c, e, f, g, h);
  return 0;
}
