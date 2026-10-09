#!/bin/sh
# Usage: probe_longwait.sh <scratch-copy-of-clone> <receipt-dir> <shim-bin-dir>
# Disposable probe: the #657 epoch-only dwell removed AND the post-selection
# wait in phase_crf lengthened from 12 M to 80 M axis cycles (800 ms, beyond
# the #386 trigger's 32768-tick ceiling of about 683 ms). Shows whether the
# no-dwell leg's zero recentres were a short wait or a lost trigger. The
# CRF phase's injection record is lengthened from 2400 to 9000 PDUs so the
# feed outlasts the longer wait.
set -u
copy=$1; out=$2; bin=$3
export PATH="$bin:$PATH" VERILATOR="$bin/verilator" VERILATOR_JOBS=4
cd "$copy/tb/verilator/milan_dp_render" || exit 99
H=sim_tdm8_render.cpp
python3 -I - "$H" <<'PY'
import sys
p = sys.argv[1]; t = open(p).read()
for old, new in [("    if (epoch_only) run_fed(kBootPullInCycles);\n", ""),
                 ("    build_injection_record(2400);\n", "    build_injection_record(9000);\n"),
                 ("    run_fed(12000000);\n    check.dec(\"T30 CRF: the selection",
                  "    run_fed(80000000);\n"
                  "    std::printf(\"  [i]    PROBE: src pulses %ld render pulses %ld stage %u\\n\",\n"
                  "                src_recentre_pulses - src0, recentre_pulses - pulses0,\n"
                  "                dut->rootp->milan_datapath__DOT__rsp_recentres_w - rc0);\n"
                  "    check.dec(\"T30 CRF: the selection")]:
    assert t.count(old) == 1, old
    t = t.replace(old, new)
open(p, "w").write(t)
PY
taskset -c 6-11 make --no-print-directory -s tdm8render-build TDM8R_MDIR=obj_p_longwait > "$out/probe_longwait_build.log" 2>&1
echo "build rc=$?" > "$out/probe_longwait.rc"
git checkout -- "$H"; git diff --quiet -- "$H" || echo "HARNESS NOT RESTORED" >> "$out/probe_longwait.rc"
s=$(date +%s)
taskset -c 6-11 ./obj_p_longwait/Vmilan_dp_tdm8r --epoch-only > "$out/probe_longwait_epoch.log" 2>&1
echo "run rc=$? elapsed=$(( $(date +%s) - s ))" >> "$out/probe_longwait.rc"
