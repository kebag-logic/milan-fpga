#!/usr/bin/env python3
"""Build a disposable PROBE copy of tb/verilator/media_grid_align from the
exact-head export. Nothing here is committed or run from the clone.

Instrumentation added (the RTL and every original arm are untouched; probe
arms run AFTER [G9], so G0-G9 see exactly the head stimulus):

  P1  net-count law, every edge from the first frame on, all arms:
      I = (dups - skips) - (ticks - markers) - pend, with dups/skips/pend read
      from the REAL KL_chan_map_capture (pend via its public_flat_rd), ticks
      and markers counted at the junction's own inputs. The rewritten
      SLIP_TDM paragraph claims dups - skips follows ticks - markers to within
      the one pending marker; that is I == 0 at every edge.
  P2  dither census of the [G9] passages (no delivery jitter): the signed
      offset of every marker from its nearest tick, as the junction pairs
      them, and the largest step back against the passage direction
      (1 = the marker dithers between two adjacent cycles).
  P3  the same passages with one edge of delivery jitter, eight seeds per
      direction: dups, skips, net, and the step back.
  P4  (build-time -DPROBE_KEEPOFF=N) the wrap overrides LOCK_KEEPOFF_CYC_P.

Usage: 30_make_probe.py <export-root>
"""
import pathlib
import re
import shutil
import sys

root = pathlib.Path(sys.argv[1])
src = root / "tb/verilator/media_grid_align"
dst = root / "tb/verilator/media_grid_align_probe"
if dst.exists():
    shutil.rmtree(dst)
dst.mkdir()


def sub1(text, old, new):
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"probe patch anchor found {n} times: {old[:60]!r}")
    return text.replace(old, new)


# ---- wrap: optional keep-off override --------------------------------------
wrap = (src / "media_grid_align_wrap.sv").read_text()
wrap = sub1(wrap, "`ifdef MGA_MUT_NO_KEEPOFF\n    , .LOCK_KEEPOFF_CYC_P (0)\n`endif",
            "`ifdef MGA_MUT_NO_KEEPOFF\n    , .LOCK_KEEPOFF_CYC_P (0)\n`endif\n"
            "`ifdef PROBE_KEEPOFF\n    , .LOCK_KEEPOFF_CYC_P (`PROBE_KEEPOFF)\n`endif")
(dst / "media_grid_align_wrap.sv").write_text(wrap)

# ---- harness ---------------------------------------------------------------
cpp = (src / "sim_main.cpp").read_text()
cpp = sub1(cpp, '#include "Vmedia_grid_align_wrap.h"\n',
           '#include "Vmedia_grid_align_wrap.h"\n#include "Vmedia_grid_align_wrap___024root.h"\n#include <vector>\n#include <map>\n')

# P1: the invariant, evaluated after every edge
cpp = sub1(cpp, "        bool tk = dut->tick_o;\n",
           "        bool tk = dut->tick_o;\n"
           "        probe_invariant(fev);\n")

# P2/P3: per-marker offsets in track_clearance
cpp = sub1(cpp, """        if (tick_q) {
            if (mark_phase > 0)""",
           """        if (tick_q) {
            if (probe_log) {
                for (long n : probe_phases) {
                    const long m = edges_since_tick + 1 - n;
                    probe_offset(n <= m ? n : -m);
                }
            }
            probe_phases.clear();
            if (mark_phase > 0)""")
cpp = sub1(cpp, """        if (fev) {
            mark_phase = tick_q ? 0 : edges_since_tick;""",
           """        if (fev && probe_log) {
            if (tick_q) probe_offset(0);
            else probe_phases.push_back(edges_since_tick);
        }
        if (fev) {
            mark_phase = tick_q ? 0 : edges_since_tick;""")

# G9: census its two passages (stimulus unchanged: logging only)
cpp = sub1(cpp, """        anchor_grid(kPlanPeriod, 2063);
        long d0 = rtl_dups(), s0 = rtl_skips();
        run_cycles(10'000'000);""",
           """        anchor_grid(kPlanPeriod, 2063);
        long d0 = rtl_dups(), s0 = rtl_skips();
        probe_begin(+1);
        run_cycles(10'000'000);
        probe_end("P2 G9 slow passage, no jitter", d0, s0);""")
cpp = sub1(cpp, """        anchor_grid(kFastPeriod, 20);
        d0 = rtl_dups(); s0 = rtl_skips();
        run_cycles(10'000'000);""",
           """        anchor_grid(kFastPeriod, 20);
        d0 = rtl_dups(); s0 = rtl_skips();
        probe_begin(-1);
        run_cycles(10'000'000);
        probe_end("P2 G9 fast passage, no jitter", d0, s0);""")

# probe arms after G9
cpp = sub1(cpp, "        prove_a_free_running_passage_counts_one_slip();\n\n        return report();",
           "        prove_a_free_running_passage_counts_one_slip();\n"
           "        probe_jittered_passages();\n"
           "        probe_report();\n\n        return report();")

probe_members = r'''
    // ======================= PROBE (disposable, never committed) ============
    bool  inv_on = false;
    long  inv_T = 0, inv_M = 0, inv_edges = 0, inv_viol = 0;
    long  inv_dev_min = LONG_MAX, inv_dev_max = LONG_MIN;
    void probe_invariant(bool fev) {
        auto* r = dut->rootp;
        const bool fed  = r->media_grid_align_wrap__DOT__u_junction__DOT__tdm_fed_r;
        const bool pnd  = r->media_grid_align_wrap__DOT__u_junction__DOT__tdm_frame_pend_r;
        if (!fed) return;
        inv_on = true;
        if (tick_q) inv_T++;
        if (fev)    inv_M++;
        inv_edges++;
        const long dev = (rtl_dups() - rtl_skips()) - (inv_T - inv_M);
        inv_dev_min = std::min(inv_dev_min, dev);
        inv_dev_max = std::max(inv_dev_max, dev);
        const long I = dev - (pnd ? 1 : 0);
        if (I != 0 && ++inv_viol <= 5)
            printf("  [probe] P1 VIOLATION I=%ld at edge %ld\n", I, inv_edges);
        if (rtl_dups() >= 0xFFFF || rtl_skips() >= 0xFFFF)
            printf("  [probe] P1 counter saturated at edge %ld\n", inv_edges);
    }

    bool  probe_log = false;
    int   probe_dir = 0;
    std::vector<long> probe_phases;
    std::map<long, long> probe_hist;
    long  probe_run_ext = 0, probe_back = 0, probe_n = 0;
    void probe_offset(long o) {
        probe_n++;
        if (o >= -6 && o <= 6) probe_hist[o]++;
        // step back against the passage direction, near the crossing only
        if (o < -200 || o > 200) return;
        const long v = probe_dir * o;               // increasing along the passage
        if (v > probe_run_ext) probe_run_ext = v;
        probe_back = std::max(probe_back, probe_run_ext - v);
    }
    void probe_begin(int dir) {
        probe_log = true; probe_dir = dir; probe_phases.clear(); probe_hist.clear();
        probe_run_ext = LONG_MIN / 2; probe_back = 0; probe_n = 0;
    }
    void probe_end(const char* what, long d0, long s0) {
        probe_log = false;
        const long d = rtl_dups() - d0, s = rtl_skips() - s0;
        printf("  [probe] %s: dups %ld, skips %ld, net %+ld, markers logged %ld, "
               "largest step back %ld\n", what, d, s, d - s, probe_n, probe_back);
        printf("  [probe]   offsets -6..6 (marker edge minus nearest tick edge):");
        for (auto& kv : probe_hist) printf(" %ld:%ld", kv.first, kv.second);
        printf("\n");
    }
    int p3_fail = 0;
    void probe_jittered_passages() {
        printf("\n[P3] probe: [G9]'s passages with one edge of delivery jitter\n");
        for (uint32_t seed = 1; seed <= 8; seed++) {
            for (int dir : {+1, -1}) {
                anchor_grid(dir > 0 ? kPlanPeriod : kFastPeriod, dir > 0 ? 2063 : 20);
                marker_jitter = true;
                rng = 0x9E3779B9u * seed;
                const long d0 = rtl_dups(), s0 = rtl_skips();
                probe_begin(dir);
                run_cycles(10'000'000);
                char what[96];
                snprintf(what, sizeof what, "P3 seed %u %s passage, 1-edge jitter",
                         seed, dir > 0 ? "slow" : "fast");
                probe_end(what, d0, s0);
                const long net = (rtl_dups() - d0) - (rtl_skips() - s0);
                if (net != dir) { p3_fail++; printf("  [probe] P3 NET MISMATCH\n"); }
                marker_jitter = false;
            }
        }
    }
    void probe_report() {
        printf("\n[P1] probe: net-count law over every edge from the first frame on\n");
        printf("  [probe] P1 edges checked %ld, ticks %ld, markers %ld, violations %ld, "
               "(dups-skips)-(ticks-markers) in [%ld, %ld]\n",
               inv_edges, inv_T, inv_M, inv_viol, inv_dev_min, inv_dev_max);
        printf("  [probe] P1 %s\n", (inv_on && inv_viol == 0) ? "HOLDS" : "BROKEN");
        printf("  [probe] P3 net mismatches %d\n", p3_fail);
    }
'''
cpp = sub1(cpp, "    long     clear_min     = LONG_MAX;\n};",
           "    long     clear_min     = LONG_MAX;\n" + probe_members + "};")
(dst / "sim_main.cpp").write_text(cpp)

# ---- probe Makefile: same flags as the suite, no mutant legs ----------------
mk = (src / "Makefile").read_text()
m = re.search(r"^VFLAGS = .*?(?=\n\n)", mk, re.S | re.M)
vflags = m.group(0).replace("--build -j 0", "--build -j 8")
(dst / "Makefile").write_text(f"""# DISPOSABLE PROBE - not part of the repository
VERILATOR ?= verilator
RTL_DIR    = ../../../hdl
TOP        = media_grid_align_wrap
{vflags}
AL  ?= $(RTL_DIR)/ieee1722/crf/KL_media_grid_align.sv
CAP ?= $(RTL_DIR)/ieee1722/aaf/KL_chan_map_capture.sv
DEFS ?=
MDIR ?= obj_probe
SRCS = media_grid_align_wrap.sv $(AL) $(RTL_DIR)/ieee1722/crf/KL_media_nco.sv $(CAP)
build:
\t$(VERILATOR) $(VFLAGS) --Mdir $(MDIR) $(DEFS) $(SRCS) sim_main.cpp -o Vprobe
""")
print(f"probe written to {dst}")
