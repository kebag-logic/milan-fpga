#!/usr/bin/env python3
"""Disposable probe (reviewer R476-1): send-to-send spacing of GET_COUNTERS
rounds for one registered controller at the full timebase (1 ms = 1,000 clocks).

Plants, in an extracted copy of the processor tree given as argv[1], a section
that replaces the fifth build's (PP_TOP_TIM_REAL) section TB: on a fresh
processor with ONE registered controller, a counter change for AVB_INTERFACE 0
is pulsed SHIFT clocks after a ms tick (the window is open, so the round goes
out at once); a second change 100 ms later must wait for the window. The probe
prints the wire gap between the two GET_COUNTERS frames in clocks; at 1,000
clocks per ms a gap below 1,000,000 clocks is a gap below one second.
Never applied to the review clone.
"""
import sys
from pathlib import Path

tree = Path(sys.argv[1])
hpp = tree / "tb/pp_top/notify_phases.hpp"
cpp = tree / "tb/pp_top/sim_main.cpp"

PROBE = r'''
// ==== R476 disposable probe: one controller, spacing at the full timebase ====
struct TickProbePhase : CounterSpacingPhase {
  using CounterSpacingPhase::CounterSpacingPhase;
  void probe_one(long shift) {
    boot_to_idle(true);
    const bool ok = register_controller(ROW_MAC, ROW_EID, seq++);
    run_ms(5);
    const uint32_t ms0 = io.d->dbg_now_ms_o;
    while (io.d->dbg_now_ms_o == ms0) tick();
    for (long c = 0; c < shift; ++c) tick();
    const size_t from = seen.size();
    pulse(3);                               // AVB_INTERFACE 0, window open
    run_ms(100);
    pulse(3);                               // held for the window
    run_ms(1300);
    const auto r = rounds_at(0, 3, from);
    const long gap = r.size() >= 2 ? long(r[1] - r[0]) : -1;
    printf("PROBE-TICK shift=%ld registered=%d rounds=%zu gap_clocks=%ld below_1s=%s\n",
           shift, int(ok), r.size(), gap, (gap >= 0 && gap < 1000L * MS_CYC) ? "YES" : "no");
    CHECK(r.size() == 2 && gap >= 1000L * MS_CYC,
          "PROBE-TICK: shift %ld: two GET_COUNTERS rounds to one controller at least one "
          "second apart on the wire: %ld clocks (%zu rounds), want at least %ld",
          shift, gap, r.size(), 1000L * MS_CYC);
  }
};
[[maybe_unused]] static void run_tick_probe(H& h) {
  for (long s : {0L, 50L, 100L, 250L, 500L, 750L, 900L, 990L}) TickProbePhase{h}.probe_one(s);
}
'''

text = hpp.read_text()
anchor = "// ==== RN. RND: seeded registry"
assert text.count(anchor) == 1
hpp.write_text(text.replace(anchor, PROBE + "\n" + anchor, 1))

text = cpp.read_text()
old = '  run_budgets(h);\n  const char* const build = "timebase";'
assert text.count(old) == 1
cpp.write_text(text.replace(old, '  run_tick_probe(h);\n  const char* const build = "timebase";', 1))
print("planted")
