#!/usr/bin/env python3
"""Per-reset-segment liveness probe for tb/verilator/gptp_tables.

Copies a pristine head tree, adds a print of the wrapper's cumulative
counters before each warm reset and before grading (harness-only change; no
RTL is touched), runs `make -s run`, and writes the log.

Usage: segment_probe.py PRISTINE_TREE WORK_DIR LOG_FILE VERILATOR_BIN
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

pristine, work, log, vbin = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
if work.exists():
    shutil.rmtree(work)
shutil.copytree(pristine, work, symlinks=True)
sim = work / "tb/verilator/gptp_tables/sim_main.cpp"
text = sim.read_text(encoding="utf-8")
seg = ('  void seg(const char* l) {\n'
       '    std::printf("SEG %s cyc=%llu prog=%u res_cmp=%u tmr_cmp=%u led_cmp=%u tx_frames=%u flags=0x%x\\n", l,\n'
       '                static_cast<unsigned long long>(cyc), dut->dbg_prog_run_o, dut->res_cmp_o,\n'
       '                dut->tmr_cmp_o, dut->led_cmp_o, dut->tx_frames_o, dut->pub_flags_o);\n'
       '  }\n')
anchor = "  // ---- grading ---------------------------------------------------------\n"
assert text.count(anchor) == 1
text = text.replace(anchor, seg + anchor, 1)
calls = text.count("    warm_reset_in_traffic();\n")
assert calls == 2, calls
parts = text.split("    warm_reset_in_traffic();\n")
text = (parts[0] + '    seg("before-reset-1");\n    warm_reset_in_traffic();\n    seg("after-reset-1");\n'
        + parts[1] + '    seg("before-reset-2");\n    warm_reset_in_traffic();\n    seg("after-reset-2");\n' + parts[2])
anchor2 = "    drain(500000);\n    grade();\n"
assert text.count(anchor2) == 1
text = text.replace(anchor2, '    seg("before-drain");\n    drain(500000);\n    seg("end");\n    grade();\n', 1)
sim.write_text(text, encoding="utf-8")
env = dict(os.environ)
env["PATH"] = str(Path(vbin).parent) + os.pathsep + env.get("PATH", "")
env["VERILATOR"] = vbin
p = subprocess.run(["make", "-s", "run"], cwd=work / "tb/verilator/gptp_tables", env=env,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False)
log.write_text(p.stdout, encoding="utf-8")
print(f"make rc {p.returncode}")
