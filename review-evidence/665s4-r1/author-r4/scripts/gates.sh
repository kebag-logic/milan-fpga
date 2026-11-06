#!/bin/sh
# Lane S4 round 4's gate runs: gates.sh short|long OUT_NAME, or gates.sh rest OUT_NAME GATE... "long" runs the
# firmware, builder, coverage, co-simulation, census and boundary gates; "short" runs every other gate of
# gates_s4.py; "rest" runs only the named gates (the long gates a host reset cut off, at the same head).
. $MANAGEMENT/2026-09-23/665s4-a698d/scripts/env.sh
LONG="builder_require_rv32 ctrl_nvm ctrl_firmware fw_coverage_selftest fw_coverage nvm_cosim nvm_cosim_lint publication_census firmware_boundary firmware_boundary_verilator ctrl_memory"
kind=$1; name=$2; out=$SCRATCH/$2
shift 2
mkdir -p "$SCRATCH/gate-scratch-$name"
cd $LANES/665-s4-f1-target || exit 2
R=$MANAGEMENT/2026-09-23/665s4-a698d/scripts/gates_s4.py
if [ "$kind" = long ]; then
  python3 "$R" "$PWD" "$MD_PY" "$out" "$SCRATCH/gate-scratch-$name" $LONG > "$out.log" 2>&1
elif [ "$kind" = rest ]; then
  python3 "$R" "$PWD" "$MD_PY" "$out" "$SCRATCH/gate-scratch-$name" "$@" > "$out.log" 2>&1
else
  GATE_SKIP="$LONG" python3 "$R" "$PWD" "$MD_PY" "$out" "$SCRATCH/gate-scratch-$name" > "$out.log" 2>&1
fi
echo $? > "$out.rc"
