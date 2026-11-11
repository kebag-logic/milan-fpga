#!/usr/bin/env bash
# The campaigns' remaining arms (crflic datapath/TSpec 0-7, gsi 1-14), at most
# 12 at once, each its own log and rc file. usage: launch_rest.sh <repo> <logs> <work>
set -u
repo=$1 logs=$2 work=$3 here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$logs" "$work"
cd "$repo/tb/verilator/milan_dp"
{ for i in 0 1 2 3 4 5 6 7; do echo "crflic_dp $i"; done; for i in $(seq 1 14); do echo "gsi $i"; done; } |
xargs -P 12 -L 1 bash -c '
  if [ "$0" = crflic_dp ]; then python3 -B "'"$here"'/run_crflic_dp_arm.py" "'"$repo"'" "$1" "'"$work"'" > "'"$logs"'/crflic_dp$1.log" 2>&1
  else python3 -B gsi_mutants.py "$1" > "'"$logs"'/gsi_$1.log" 2>&1; fi
  echo $? > "'"$logs"'/${0}_$1.rc"'
echo done > "$logs/ALL.done"
