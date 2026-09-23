#!/usr/bin/env bash
# Run reviewer mutants through milan_dp legs, at most PAR at once, one C++ job each.
# usage: campaign.sh TREE MUTDIR LOGDIR PAR < list
#   each list line: "<mutant-id> <leg>"; the id "base" runs the unmutated tree.
# Needs VERILATOR in the environment. Logs: LOGDIR/<id>.<leg>.log (+ .build).
set -euo pipefail
tree=$1 mutdir=$2 logdir=$3 par=$4
here=$(cd "$(dirname "$0")" && pwd)
objroot=$(dirname "$mutdir")/obj
mkdir -p "$logdir" "$objroot"
run_one() {
  local id=$1 leg=$2 dp=()
  [ "$id" != base ] && dp=(--dp-src "$mutdir/$id/milan_datapath.sv")
  python3 "$here/leg.py" "$tree" "$leg" "$objroot/$id.$leg" "$logdir/$id.$leg.log" \
    "${dp[@]}" --jobs 1 || true
  printf '%s %s %s\n' "$id" "$leg" "$(grep -E '^(run_exit|build_exit)=' "$logdir/$id.$leg.log" | tail -1)"
}
export -f run_one
export tree mutdir logdir objroot here
xargs -P "$par" -L 1 bash -c 'run_one "$0" "$1"'
