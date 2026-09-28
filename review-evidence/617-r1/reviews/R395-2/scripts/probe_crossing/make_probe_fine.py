#!/usr/bin/env python3
"""Derive probe_fine.cpp + probe_bench.hpp from probe_main.cpp and the
committed coherence_bench.hpp: adds a sub-step phase control (the TDM
fractional-N accumulator preloaded to K/N of its denominator, which moves
every TDM edge by up to one oscillator step, i.e. below the quarter-cycle hold
granularity) and prints the column index at which the aligner engaged.
Usage: probe_fine PPM LO HI STEP FRAMES SUBS NFRAC  (--probe prefix kept)
"""
import sys
from pathlib import Path
d = Path(sys.argv[1])
hdr = (d / "coherence_bench.hpp").read_text()
def sub(s, old, new):
    assert s.count(old) == 1, old
    return s.replace(old, new)
hdr = sub(hdr, "namespace coherence {", "namespace coherence {\ninline std::uint64_t g_acc_num = 0, g_acc_den = 1;")
hdr = sub(hdr, "        acc_ = 0;\n        hold_ = hold_steps;",
          "        acc_ = static_cast<std::uint64_t>((static_cast<unsigned __int128>(plan.den) * g_acc_num) / g_acc_den);\n        hold_ = hold_steps;")
hdr = sub(hdr, "#ifndef MILAN_TB_CAPTURE_COHERENCE_BENCH_HPP", "#ifndef MILAN_TB_CAPTURE_COHERENCE_PROBE_BENCH_HPP\n#define MILAN_TB_CAPTURE_COHERENCE_PROBE_BENCH_HPP\n#ifndef MILAN_TB_CAPTURE_COHERENCE_BENCH_HPP")
hdr = hdr + "\n#endif\n"
(d / "probe_bench.hpp").write_text(hdr)
src = (d / "probe_main.cpp").read_text()
src = sub(src, '#include "coherence_bench.hpp"', '#include "probe_bench.hpp"')
src = sub(src, "    long run_far_col = 0;       //! the column at which it moved furthest",
          "    long run_far_col = 0;       //! the column at which it moved furthest\n    long engage_col = -1;")
src = sub(src, "        t_.engage_offset = after_tick;\n        t_.engage_seen = true;",
          "        t_.engage_offset = after_tick;\n        t_.engage_seen = true;\n        t_.engage_col = bench_.live() ? bench_.tally().columns : -1;")
src = sub(src, '"%ld skips; last slip col %ld; tail slips %ld\\n"', '"%ld skips; last slip col %ld; tail slips %ld; engage col %ld\\n"')
src = sub(src, "bench_.tally().last_slip_col, bench_.tally().tail_slips);", "bench_.tally().last_slip_col, bench_.tally().tail_slips, t_.engage_col);")
src = sub(src, '''    if (arg == "--probe" && argc == 8) {''', '''    if (arg == "--probe" && argc == 9) {
        g_acc_num = std::strtoull(argv[8], nullptr, 10);
        g_acc_den = 64;
        argc = 8;
    }
    if (arg == "--probe" && argc == 8) {''')
src = sub(src, 'std::snprintf(tag, sizeof tag, "P%+d", ppm);', 'std::snprintf(tag, sizeof tag, "P%+d/%llu", ppm, static_cast<unsigned long long>(g_acc_num));')
(d / "probe_fine.cpp").write_text(src)
