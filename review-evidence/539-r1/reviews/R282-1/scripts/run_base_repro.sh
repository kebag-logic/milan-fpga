#!/bin/sh
# Acceptance 1, independently: the head's silicon-scale harness against the BASE
# servo RTL (26d855a9). Base has no ptp_jump_r, so the probe copy of the harness
# reads it as constant 0 (only the P2 arm checks use it). Runs the 150 us
# reproduction trace, a size sweep, and the full P-suite (expected to FAIL).
set -u
. "$(dirname "$0")/env.sh"
W="$PKT/scratch/base_repro"
rm -rf "$W"; mkdir -p "$W"
git -C "$CLONE" archive "$BASE_SHA" hdl tb/common | tar -x -C "$W"
git -C "$CLONE" archive "$HEAD_SHA" tb/verilator/mmcm_servo | tar -x -C "$W"
T="$W/tb/verilator/mmcm_servo/sim_phc_step.cpp"
sed -i 's#bool ptp_jump() const { return root()->KL_mmcm_drp_servo__DOT__ptp_jump_r != 0; }#bool ptp_jump() const { return false; }  /* base: no detector */#' "$T"
grep -n 'bool ptp_jump' "$T"
make -C "$W/tb/verilator/mmcm_servo" VERILATOR="$VERILATOR" VFLAGS="$VFLAGS_R" phc_step_build >/dev/null || { echo BUILD-FAILED; exit 2; }
B="$W/tb/verilator/mmcm_servo/obj_phc/Vphc_step"
for s in 21000 100000 108000 150000 -150000 300000 524000 525000 1000000 1000000000; do
  "$B" +trace_step_ns=$s
done
echo "=== base: full P-suite (acceptance arms must fail on base) ==="
"$B"; echo "base suite exit=$?"
