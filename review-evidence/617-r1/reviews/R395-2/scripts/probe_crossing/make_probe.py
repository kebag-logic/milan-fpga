#!/usr/bin/env python3
"""Derive probe_main.cpp from the committed sim_main.cpp (exact head bytes).

Adds a `--probe PPM LO HI STEP FRAMES SUBS` mode: a placed CRF sweep on the
PPM plan (0 = the true 391/1591 plan), engagements from LO to HI cycles of
the crossing STEP apart, each also shifted by 0..SUBS-1 quarter-cycle
oscillator steps, FRAMES columns each; and prints, per scenario, the column
of the last slip. No check is weakened; the committed grading runs as is.
"""
import sys
from pathlib import Path

src = Path(sys.argv[1]).read_text()
out = Path(sys.argv[2])

def sub(old, new):
    global src
    assert src.count(old) == 1, old
    src = src.replace(old, new)

# print the last slip column beside the existing per-scenario line
sub('''                "%ld skips\\n", sc.name.c_str(), landed, t_.run_min, t_.run_max, t_.run_far_col, t_.lock_phase_ref,
                t_.lock_phase_min, t_.lock_phase_max, spread, bench_.tally().dups, bench_.tally().skips);''',
    '''                "%ld skips; last slip col %ld; tail slips %ld\\n", sc.name.c_str(), landed, t_.run_min, t_.run_max, t_.run_far_col, t_.lock_phase_ref,
                t_.lock_phase_min, t_.lock_phase_max, spread, bench_.tally().dups, bench_.tally().skips,
                bench_.tally().last_slip_col, bench_.tally().tail_slips);''')
# a probe sweep with quarter-cycle sub-placements
sub('''    void run_sweep(const Sweep& sw);
    int report()''', '''    void run_sweep(const Sweep& sw);
    void run_probe(const Sweep& sw, int subs);
    int report()''')
sub('''//! The sweep's engagements must have covered its window (coherence_bench's''',
'''void JunctionHarness::run_probe(const Sweep& sw, int subs) {
    const long unheld = calibrate(sw.plan);
    std::printf("\\n[%s] PROBE CRF, %s, every %ld cycles from %+ld to %+ld, %d quarter-cycle sub-placements, %ld columns\\n",
                sw.tag.c_str(), sw.plan.name.c_str(), sw.step, sw.lo, sw.hi, subs, sw.frames);
    for (long off = sw.lo; off <= sw.hi; off += sw.step) {
        for (int s = 0; s < subs; s++) {
            char name[48];
            std::snprintf(name, sizeof name, "%s%+ld.%d", sw.tag.c_str(), off, s);
            run({name, sw.plan, true, delay_for(unheld, off) + s, sw.frames, false, true, off});
        }
    }
}

//! The sweep's engagements must have covered its window (coherence_bench's''')
sub('''    const std::string arg = argc > 1 ? argv[1] : "";''',
'''    const std::string arg = argc > 1 ? argv[1] : "";
    if (arg == "--probe" && argc == 8) {
        const int ppm = std::atoi(argv[2]);
        const ClockPlan plan = ppm == 0 ? true_plan() : ppm_plan(ppm);
        char tag[32];
        std::snprintf(tag, sizeof tag, "P%+d", ppm);
        harness.run_probe({tag, plan, std::atol(argv[3]), std::atol(argv[4]), std::atol(argv[5]), std::atol(argv[6])},
                          std::atoi(argv[7]));
        return harness.report();
    }''')
out.write_text(src)
