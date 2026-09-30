#!/usr/bin/env python3
"""Reviewer probe (disposable copy only): stall the MAC's tx_ready for STALL ms right
after the first IDENTIFY_NOTIFICATION frame of a burst and print the wire gaps.
Usage: probe_bunch.py COPY_ROOT   (COPY_ROOT holds hdl/, tb/common, tb/pp_top of the head)
Grades nothing itself: it prints the measured clocks (100 clocks = 1 ms in this bench).
"""
import sys
from pathlib import Path
root = Path(sys.argv[1])
hpp = root / "tb/pp_top/notify_phases.hpp"
text = hpp.read_text()
probe = r'''
  // ---- reviewer probe: a MAC stall between frames of one burst ----------
  void reviewer_probe_mid_burst_stall(long stall_ms) {
    boot_to_idle(true);
    const size_t from = seen.size();
    press(true);
    for (long c = 0; c < 50L * MS_CYC && idents(from).empty(); ++c) tick();
    press(false);
    io.mac_tx_ready = false;                    // MAC back-pressure
    run_ms(stall_ms);
    io.mac_tx_ready = true;
    run_ms(1500);
    const auto v = idents(from);
    printf("  [probe] stall %ld ms after frame 1: %zu identify frames\n", stall_ms, v.size());
    for (size_t k = 1; k < v.size(); ++k)
      printf("  [probe] stall %ld ms: gap frame %zu->%zu = %ld clocks (%ld ms)\n", stall_ms,
             k, k + 1, long(v[k].t - v[k - 1].t), long(v[k].t - v[k - 1].t) / MS_CYC);
  }
'''
anchor = "  void run() {\n    boot_to_idle(true);\n    one_press_sends_one_burst();\n"
assert text.count(anchor) == 1
text = text.replace(anchor, probe + "  void run() {\n    reviewer_probe_mid_burst_stall(100);\n"
                    "    reviewer_probe_mid_burst_stall(250);\n    reviewer_probe_mid_burst_stall(400);\n"
                    "    boot_to_idle(true);\n    one_press_sends_one_burst();\n", 1)
hpp.write_text(text)
print("planted probe into", hpp)
