#!/bin/bash
# The CPU budget harness's controls from a checkout, one after another, each its own build and log, rc last.
# usage: controls.sh CHECKOUT
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683m/scripts/env.sh
C=$1
B=$VALIDATION_STORAGE/665s2b-a683m/builds/ctl
L=$VALIDATION_STORAGE/665s2b-a683m/logs/ctl
mkdir -p "$B" "$L"
one() {
  local name=$1; shift
  local start=$(date +%s)
  echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=no | wc -l)" > "$L/$name.log"
  echo "\$ run.py --point 1x1 $*" >> "$L/$name.log"
  python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point 1x1 --build-dir "$B/$name" --jobs 4 "$@" >> "$L/$name.log" 2>&1
  local rc=$?
  echo "elapsed=$(( $(date +%s) - start ))s" >> "$L/$name.log"
  echo "rc=$rc" >> "$L/$name.log"
}
one slow-adp-rx --fetch-l1 none --mutation slow-adp-rx
one slow-adp-shutdown --fetch-l1 none --variant shutdown-entry --mutation slow-adp-shutdown
one as-built --fetch-l1 none --cpu-regions as-built
one as-built-cached --cpu-regions as-built
