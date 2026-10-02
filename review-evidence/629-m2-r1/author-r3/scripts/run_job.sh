#!/bin/bash
# run_job.sh <workflow> <job> <outname> [extra driver args...]
set -u
R=$VALIDATION_STORAGE/629-a500
wf=$1; job=$2; name=$3; shift 3
cd $LANES/629-m2-impl || exit 2
/usr/bin/python3 "$HOME"/milan-fpga-management/2026-09-23/629-a500/scripts/replay_workflow.py \
  --repo $LANES/629-m2-impl --workflow "$wf" --job "$job" \
  --out "$R/replay/$name" --subst "$HOME"/milan-fpga-management/2026-09-23/629-a500/scripts/replay_subst.json \
  --prefix-path "${VENV:-$R/replay-venv}/bin" --home "${HOMEDIR:-$R/home}" \
  --map /opt/verilator=$VALIDATION_TOOLS/verilator-v5.050 \
  --base-sha cdf49d1a28527562888f0a903de51b6b15b1244f --keep-going "$@" \
  > "$R/replay/$name.log" 2>&1
rc=$?
echo "rc=$rc" >> "$R/replay/$name.log"
exit $rc
