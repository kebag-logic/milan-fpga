#!/bin/bash
# run_job.sh <workflow> <job> <outname> [extra driver args...]
# One hosted job replayed at the lane head under GNU make 4.3 (round 4).
# The pull_request event's recorded base oid is PR #634's, frozen at open
# (cdf49d1a); steps that need the live base derive it from origin/dev.
set -u
R=$VALIDATION_STORAGE/629-a512
O=$HOME/milan-fpga-management/2026-09-23/629-a512/scripts
wf=$1; job=$2; name=$3; shift 3
cd $LANES/629-m2-impl || exit 2
/usr/bin/python3 "$O/replay_workflow.py" \
  --repo $LANES/629-m2-impl --workflow "$wf" --job "$job" \
  --out "$R/replay/$name" --subst "$O/replay_subst.json" \
  --prefix-path "${VENV:-$R/replay-venv}/bin" --home "${HOMEDIR:-$R/home}" \
  --map /opt/verilator=$VALIDATION_TOOLS/verilator-v5.050 \
  --base-sha cdf49d1a28527562888f0a903de51b6b15b1244f --keep-going "$@" \
  > "$R/replay/$name.log" 2>&1
rc=$?
echo "rc=$rc" >> "$R/replay/$name.log"
exit $rc
