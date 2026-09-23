#!/usr/bin/env python3
"""Write sim_nxn_probe.cpp beside sim_nxn.cpp in a DISPOSABLE checkout copy.

The probe keeps every existing check and adds one after [NOTIFY-CRF]'s
release: with no further CRF change, the row must not push a third time in
the next ~1.2 processor seconds. Usage: make_probe_harness.py <suite_dir>
"""
import os
import sys

d = sys.argv[1]
src = open(os.path.join(d, "sim_nxn.cpp")).read()
anchor = ('        ck("[NOTIFY-CRF] ...no earlier than one second after the first",\n'
          '           static_cast<long>(t1 >= 0 && t2 - t1 >= 990L * kMsCycTb), 1);\n'
          '        crf_lever(false);\n')
assert src.count(anchor) == 1, "anchor"
probe = ('        ck("[NOTIFY-CRF] ...no earlier than one second after the first",\n'
         '           static_cast<long>(t1 >= 0 && t2 - t1 >= 990L * kMsCycTb), 1);\n'
         '        //! reviewer probe: no third push without a third change\n'
         '        while (uns_log_cycle - t1 < 3300L * kMsCycTb) drain_tx(10 * kMsCycTb);\n'
         '        ck("[R268-PROBE] no further CRF push without a further change",\n'
         '           notify_count(0x0029, &CTL_B, 0x0005, ix), 2);\n'
         '        crf_lever(false);\n')
open(os.path.join(d, "sim_nxn_probe.cpp"), "w").write(src.replace(anchor, probe))
print("wrote", os.path.join(d, "sim_nxn_probe.cpp"))
