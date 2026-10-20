#!/usr/bin/env python3
"""Exercise all parser-admitted non-CRF subtypes, both started and stopped.

Run after run-focused.py. Only a disposable harness copy is changed.
"""
import os
from pathlib import Path
import subprocess
import sys

packet = Path(sys.argv[1]).resolve()
work = packet / "scratch" / "focused"
source = work / "source"
suite = source / "tb/verilator/crf_rx"
cpp = (suite / "sim_main.cpp").read_text()
call = "        pin_aaf_pdu_on_the_crf_input();"
assert cpp.count(call) == 1
cpp = cpp.replace(call, """        for (uint8_t subtype = 0; subtype < 8; ++subtype) {
            if (subtype == 4) continue;
            for (bool stopped : {false, true})
                pin_aaf_pdu_on_the_crf_input(subtype, stopped);
        }""")
start = cpp.index("    void pin_aaf_pdu_on_the_crf_input()")
end = cpp.index("    void pin_unbind_scores_one_unlock()", start)
method = cpp[start:end]
method = method.replace("pin_aaf_pdu_on_the_crf_input()", "pin_aaf_pdu_on_the_crf_input(uint8_t subtype, bool stopped)")
method = method.replace('        printf("\\n[FMT]', '        printf("boundary subtype=%u stopped=%u\\n", subtype, stopped);\n        printf("\\n[FMT]')
method = method.replace("        dut->subtype_i = 0x02;", """        dut->stop_i = stopped;
        dut->subtype_i = subtype;
        dut->seq_i = static_cast<uint8_t>(seq + 17);
        const uint32_t interrupts = dut->cnt_intr_o;""")
method = method.replace("        dut->subtype_i = 0x04;", """        dut->stop_i = false;
        dut->subtype_i = 0x04;
        ck("reject never counts a sequence-gap interruption", dut->cnt_intr_o, interrupts);""")
cpp = cpp[:start] + method + cpp[end:]
harness = work / "crf-boundaries.cpp"
harness.write_text(cpp)
mdir = work / "obj_boundaries"
env = os.environ.copy()
env.update(TMPDIR=str(work), MAKEFLAGS="-j16")
with (packet / "crf-boundaries-build.log").open("w") as log:
    rc = subprocess.run(["make", "-j16", "-s", "unit-build", f"VERILATOR={work / 'verilator'}",
                         f"UNIT_CPP={harness}", f"UNIT_MDIR={mdir}"],
                        cwd=suite, env=env, stdout=log, stderr=subprocess.STDOUT).returncode
if rc == 0:
    with (packet / "crf-boundaries.log").open("w") as log:
        rc = subprocess.run([str(mdir / "Vcrf_rx_sim")], cwd=suite,
                            stdout=log, stderr=subprocess.STDOUT).returncode
(packet / "crf-boundaries.rc").write_text(str(rc) + "\n")
print("CRF boundary probe rc", rc)
raise SystemExit(rc)
