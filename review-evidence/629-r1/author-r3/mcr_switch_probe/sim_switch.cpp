// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// #629 design round 3, switch-test probe. Drives the unmodified
// hdl/ieee1722/avtp/KL_media_clock_restart.sv (head c554ae51) with
// N_TALKERS_P = 2:
//   talker 0 = an AAF output, one PDU launched every A cycles;
//   talker 1 = the CRF output, one PDU launched every C = 16 A cycles.
// A PDU latches mr_o at launch and is reported LAT cycles later on the
// transmitted-PDU feed (frame_p_i / frame_idx_i / frame_mr_i); an AAF report
// wins a same-cycle conflict and the CRF report waits one cycle, as the
// root's muxed feed does (milan_datapath.sv:3189-3197). A wire toggle is a
// change of the reported level between consecutive PDUs of one talker.
//
// Trial: reset, settle 4 C, change clk_src_i at t0 = settle + phase, pulse
// restart_p_i at t0 + d for the cases that model a second request, and
// count wire toggles per talker over 24 C after t0 (two 8-PDU CRF holds).
//
// Cases:
//   design      the switch alone (the design's one request per switch)
//   late        the no-re-seed mutant under the pinned stimulus: the new
//               input's talker starts L cycles after the switch at the
//               opposite mr level, so the stale seed's echo lands at t0 + L
//   first_pdu   the no-re-seed mutant with the new talker already streaming:
//               the echo lands at its first PDU, t0 + d for d in [0, A)
//   era_fall    the era-start disruption mutant: the lock fall the switch
//               itself causes requests a restart at t0 + d, d in 1..4
//   disruption  no source change; one restart_p_i at t0 (a followed stream's
//               loss): one toggle per output
//
// Usage: sim_switch A LAT L phase_step dstep case [case ...]
#include "VKL_media_clock_restart.h"
#include "verilated.h"
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>

static long A, C, LAT, L;

struct Res { int t0, t1; };

static Res trial(long phase, long d, bool src_change, bool restart) {
  VKL_media_clock_restart* m = new VKL_media_clock_restart;
  m->clk_i = 0; m->rst_n = 0; m->restart_p_i = 0; m->clk_src_i = 0;
  m->streaming_i = 3; m->frame_p_i = 0; m->frame_idx_i = 0; m->frame_mr_i = 0;
  for (int i = 0; i < 4; ++i) { m->clk_i = 0; m->eval(); m->clk_i = 1; m->eval(); }
  m->rst_n = 1;
  const long t0 = 4 * C + phase;
  const long end = t0 + 24 * C;
  long due[2] = {-1, -1};
  int lvl[2] = {0, 0}, last[2] = {-1, -1};
  int tog[2] = {0, 0};
  for (long t = 0; t < end; ++t) {
    m->restart_p_i = 0;
    m->frame_p_i = 0;
    if (src_change && t == t0) m->clk_src_i = 2;      // SET_CLOCK_SOURCE
    if (restart && t == t0 + d) m->restart_p_i = 1;   // the second request
    // report: AAF first; a same-cycle CRF report waits one cycle
    int rep = -1;
    if (due[0] >= 0 && due[0] <= t) rep = 0;
    else if (due[1] >= 0 && due[1] <= t) rep = 1;
    if (rep >= 0) {
      m->frame_p_i = 1; m->frame_idx_i = rep; m->frame_mr_i = lvl[rep];
      if (t >= t0 && last[rep] >= 0 && lvl[rep] != last[rep]) ++tog[rep];
      last[rep] = lvl[rep];
      due[rep] = -1;
    }
    // launch: AAF every A cycles, CRF every C cycles (offset 53)
    if (t > 8 && t % A == 0) { lvl[0] = m->mr_o & 1; due[0] = t + LAT; }
    if (t > 8 && t % C == 53) { lvl[1] = (m->mr_o >> 1) & 1; due[1] = t + LAT; }
    m->clk_i = 0; m->eval();
    m->clk_i = 1; m->eval();
  }
  delete m;
  return {tog[0], tog[1]};
}

static void report(const char* name, long n, long one, long aaf2, long crf2,
                   long any2, long zero) {
  printf("%-11s A=%ld C=%ld LAT=%ld L=%ld: trials %ld; exactly one toggle on "
         "both outputs %ld; AAF >=2 %ld; CRF >=2 %ld; any output >=2 %ld; "
         "any output 0 %ld\n", name, A, C, LAT, L, n, one, aaf2, crf2, any2,
         zero);
  fflush(stdout);
}

int main(int argc, char** argv) {
  Verilated::commandArgs(argc, argv);
  if (argc < 7) { fprintf(stderr, "usage\n"); return 2; }
  A = atol(argv[1]); C = 16 * A; LAT = atol(argv[2]); L = atol(argv[3]);
  const long pstep = atol(argv[4]), dstep = atol(argv[5]);
  for (int a = 6; a < argc; ++a) {
    const std::string k = argv[a];
    long n = 0, one = 0, aaf2 = 0, crf2 = 0, any2 = 0, zero = 0;
    for (long ph = 0; ph < C; ph += pstep) {
      long dlo = 0, dhi = 0, ds = 1;
      bool sc = true, rq = false;
      if (k == "late") { dlo = dhi = L; rq = true; }
      else if (k == "first_pdu") { dlo = 0; dhi = A - 1; ds = dstep; rq = true; }
      else if (k == "era_fall") { dlo = 1; dhi = 4; rq = true; }
      else if (k == "disruption") { sc = false; rq = true; }
      for (long d = dlo; d <= dhi; d += ds) {
        Res r = trial(ph, d, sc, rq);
        ++n;
        if (r.t0 == 1 && r.t1 == 1) ++one;
        if (r.t0 >= 2) ++aaf2;
        if (r.t1 >= 2) ++crf2;
        if (r.t0 >= 2 || r.t1 >= 2) ++any2;
        if (r.t0 == 0 || r.t1 == 0) ++zero;
      }
    }
    report(k.c_str(), n, one, aaf2, crf2, any2, zero);
  }
  return 0;
}
