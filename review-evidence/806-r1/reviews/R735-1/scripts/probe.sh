#!/usr/bin/env bash
# Build and run the milan_dp gptp leg (or another target) on a disposable
# copy of the reviewed clone with one probe applied.
# Usage: probe.sh <clone> <packet> <probe-id> [make-target] [verilator-jobs]
set -u
clone=$1 packet=$2 id=$3 target=${4:-gptp} vj=${5:-4}
vl=${PROBE_VERILATOR:-verilator}
tree=$packet/scratch/trees/$id
log=$packet/receipts/probes/$id.log
rcf=$packet/receipts/probes/$id.rc
mkdir -p "$packet/scratch/trees" "$packet/receipts/probes"
rm -rf "$tree"
{
  cp -a "$clone" "$tree" &&
  python3 -I "$packet/scripts/mutate.py" "$tree" "$id" &&
  echo "head $(git -C "$tree" rev-parse HEAD)" &&
  git -C "$tree" status --short &&
  git -C "$tree/gptp-processor" status --short &&
  /usr/bin/time -v make -C "$tree/tb/verilator/milan_dp" \
    VERILATOR="$vl" VERILATOR_JOBS="$vj" "$target"
} >"$log" 2>&1
echo $? >"$rcf"
