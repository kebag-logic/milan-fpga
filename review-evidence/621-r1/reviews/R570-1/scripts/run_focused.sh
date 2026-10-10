#!/usr/bin/env bash
# Reviewer focused campaigns at the exact head. Usage:
#   run_focused.sh <head-copy> <packet-dir> <pinned-verilator>
# Each job writes <packet>/receipts/<job>.log and <job>.rc.
set -u
H=$1; P=$2; V=$3
R=$P/receipts; W=$P/scratch/work; mkdir -p "$R" "$W"
job() { local name=$1; shift; ( "$@" > "$R/$name.log" 2>&1; echo $? > "$R/$name.rc" ) & }
export VERILATOR=$V VERILATOR_JOBS=3 PYTHONDONTWRITEBYTECODE=1
cd "$H"
job phc_head_mutants python3 -B tb/verilator/gptp_plane/phc_step.py --work "$W/phc-head" --mutants
job phc_base_generator python3 -B tb/verilator/gptp_plane/phc_step.py --work "$W/phc-basegen" --generator "$P/scratch/rom/gen_base.py"
for n in liveness-not-marked drop-ratio-at-step step-not-flagged; do
  job "phc_plant_$n" python3 -B tb/verilator/gptp_plane/phc_step.py --work "$W/phc-$n" --generator "$P/scratch/plants/gen_$n.py"
done
job gmstep_head make -C tb/verilator/milan_dp gmstep VERILATOR="$V" VERILATOR_JOBS=4
wait
