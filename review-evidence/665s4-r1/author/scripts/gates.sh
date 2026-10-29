#!/bin/sh
# Lane S4 round 2's gate runs: gates.sh short|long OUT_NAME. "long" runs the firmware, builder, coverage,
# co-simulation, census and boundary gates; "short" runs every other gate of gates_s4.py.
. $MANAGEMENT/2026-09-23/665s4-a698b/scripts/env.sh
LONG="builder_require_rv32 ctrl_nvm ctrl_firmware fw_coverage_selftest fw_coverage nvm_cosim nvm_cosim_lint publication_census firmware_boundary firmware_boundary_verilator ctrl_memory"
kind=$1; out=$SCRATCH/$2
mkdir -p "$SCRATCH/gate-scratch-$2"
cd $LANES/665-s4-f1-target || exit 2
R=$MANAGEMENT/2026-09-23/665s4-a698b/scripts/gates_s4.py
if [ "$kind" = long ]; then
  python3 "$R" "$PWD" "$MD_PY" "$out" "$SCRATCH/gate-scratch-$2" $LONG > "$out.log" 2>&1
else
  GATE_SKIP="$LONG" python3 "$R" "$PWD" "$MD_PY" "$out" "$SCRATCH/gate-scratch-$2" > "$out.log" 2>&1
fi
echo $? > "$out.rc"
