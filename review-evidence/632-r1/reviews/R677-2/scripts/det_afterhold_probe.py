#!/usr/bin/env python3
"""Add a disposable detector case `afterhold` to a COPY of sim_det.cpp.

usage: det_afterhold_probe.py <copy-of-tb/verilator/media_phase/sim_det.cpp>

The case settles the detector on +/-100 ns samples (the tracking reference
then sits near 0), then raises an mr restart (a hold) mid-window and, from
that cycle on, feeds samples alternating +10,416 / -10,416 ns, either side
of +/-Ps/2 (the reviewer's balanced population, here arriving after an event
that moved the phase onto the fold). Three windows after the spoiled one it
requires the window phase to read the half-period phase, as the balanced
case does from reset. Run with: Vdet +case=afterhold.
"""
import sys
from pathlib import Path

p = Path(sys.argv[1])
t = p.read_text()
d_anchor = "    void case_cross() {\n"
r_anchor = '    else if (name == "snap") case_snap();\n'
for a in (d_anchor, r_anchor):
    if t.count(a) != 1:
        sys.exit(f"anchor found {t.count(a)} times: {a!r}")
case = r'''    void case_afterhold() {
        bool ever = false;
        bool half = false;
        run_samples([&half](long k) -> int64_t {
            return half ? ((k & 1) ? -10416 : 10416) : ((k & 1) ? -100 : 100); }, 6, &ever);
        const int before = theta();
        for (int i = 0; i < kWinCyc / 2; i++) step_cycle();
        d_->ref_restart_p_i = 1;
        half = true;                  // the event moved the phase onto the fold
        step_cycle();
        d_->ref_restart_p_i = 0;
        while (!(R(tick_p_w) && R(win_valid_r) && R(tick_cnt_r) == 511)) step_cycle();
        step_cycle();                 // the spoiled window closes
        windows(3);
        std::printf("  info: [det afterhold] theta settled %d, three windows after the hold %d\n",
                    before, theta());
        char what[200];
        std::snprintf(what, sizeof what,
                      "[det afterhold] after a hold, samples either side of +/-Ps/2 read the half-period phase "
                      "(theta %d, |theta| >= %d)", theta(), kHalfU - kBandU);
        c_.that(what, engaged() && std::abs(theta()) >= kHalfU - kBandU);
    }

'''
t = t.replace(d_anchor, case + d_anchor)
t = t.replace(r_anchor, r_anchor + '    else if (name == "afterhold") case_afterhold();\n')
p.write_text(t)
print("afterhold case inserted")
