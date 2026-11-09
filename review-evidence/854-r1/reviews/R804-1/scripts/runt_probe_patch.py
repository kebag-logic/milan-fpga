#!/usr/bin/env python3
"""Disposable probe: replace the --drops-only path of a COPY of
tb/verilator/pp_shadow/sim_main.cpp with a runt-at-full-FIFO grading, for a
build with -GRXFILT_P=0 (rx_mac_filter pruned, so one-beat runts reach the tap).
usage: runt_probe_patch.py <copy-of-sim_main.cpp>"""
import sys
from pathlib import Path
p = Path(sys.argv[1]); s = p.read_text()
old = "            grade_control_frames_lost_to_a_full_fifo_are_counted();\n        } else if (first_probe_only) {"
assert s.count(old) == 1, "anchor"
s = s.replace(old, "            probe_runts_at_a_full_fifo();\n        } else if (first_probe_only) {")
anchor = "    void grade_control_frames_lost_to_a_full_fifo_are_counted() {\n"
assert s.count(anchor) == 1
probe = r'''    void probe_runts_at_a_full_fifo() {
        printf("[PROBE-RUNT] runts at a full FIFO (RXFILT_P=0 build)\n");
        run_idle(kDrainCycles);
        ck("PR the drop count reads 0 while nothing was lost", drop_count(), 0);
        std::vector<std::vector<uint8_t>> mixed, mixed_kept;
        for (unsigned n = 0; n < 100; n++) {
            mixed_kept.push_back(drop_adp(64, static_cast<uint8_t>(n)));
            mixed.push_back(mixed_kept.back());
        }
        unsigned runts = 0;
        for (unsigned n = 0; n < 100; n++) {
            mixed_kept.push_back(drop_adp(16, static_cast<uint8_t>(0x80 + n)));
            mixed.push_back(mixed_kept.back());
            mixed.push_back(drop_adp(8, static_cast<uint8_t>(0xC0 + (n & 0x3F))));  // one-beat runt
            runts++;
        }
        TapTally b = inject_burst(mixed, kDrainCycles);
        const uint32_t lost_b = static_cast<uint32_t>(mixed_kept.size() - b.handed.size());
        const uint32_t count_b = drop_count();
        char det[160];
        snprintf(det, sizeof det, "%u runts offered, %zu kept offered, %zu handed, %u kept lost, count %u, %u FIFO overflows",
                 runts, mixed_kept.size(), b.handed.size(), lost_b, count_b, b.overflows);
        printf("  PR runt burst: %s\n", det);
        ck_true("PR kept frames were lost", lost_b > 0, det);
        ck_true("PR runts met the full FIFO (overflows exceed kept lost)", b.overflows > lost_b, det);
        ck("PR runts are not counted: the kept frames lost equal the count", count_b, lost_b);
        ck_true("PR the kept frames handed out whole and in order", handed_in_order(b, mixed_kept), det);
    }

'''
s = s.replace(anchor, probe + anchor)
p.write_text(s)
print("patched", p)
