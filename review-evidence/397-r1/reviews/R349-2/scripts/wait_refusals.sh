#!/bin/sh
# CLI wait-range refusals must fail before any build directory is created.
# Usage: wait_refusals.sh <repo> <scratch-dir>
R=$1; D=$2; cd $R || exit 2
for a in "--device-wait-us -1" "--device-wait-us 3000001" "--program-wait-us -1" "--program-wait-us 5001" "--device-wait-us 3000001 --program-wait-us 5000"; do
  B=$D/refuse-$(echo $a | tr -c 'a-z0-9' '_'); rm -rf $B
  out=$(python3 -B tb/verilator/fw_service_budget/run.py --build-dir $B $a 2>&1 | tail -1); rc=$?
  python3 -B tb/verilator/fw_service_budget/run.py --build-dir $B $a > /dev/null 2>&1; rc=$?
  [ -e $B ] && ex=created || ex=absent
  echo "args=[$a] rc=$rc build_dir=$ex last='$out'"
done
