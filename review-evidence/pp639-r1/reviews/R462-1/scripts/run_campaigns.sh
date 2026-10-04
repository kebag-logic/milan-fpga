#!/usr/bin/env bash
# Run the processor campaigns that build the top or the listener, from an exported tree.
# usage: run_campaigns.sh TREE OUTROOT RECEIPTS LANE   (LANE = d3 | rest)
# Each driver runs in the foreground of this lane with its own log and rc file.
set -uo pipefail
tree=$1; out=$2; rec=$3; lane=$4
cd "$tree" || exit 1
run() {  # name, then the command
  local name=$1; shift
  local t0=$(date +%s)
  "$@" > "$rec/$name.log" 2>&1
  local rc=$?
  echo "$rc" > "$rec/$name.rc"
  echo "$name rc=$rc seconds=$(( $(date +%s) - t0 ))" >> "$rec/lane-$lane.txt"
}
if [ "$lane" = d3 ]; then
  run d3_mutants python3 tb/pp_top/d3_mutants.py --output "$out/d3" --jobs 3
else
  run ctr_mutants python3 tb/pp_top/ctr_mutants.py --output "$out/ctr"
  run name_wr_mutant python3 tb/pp_top/name_wr_mutant.py --output "$out/name_wr"
  run maap_mutants python3 tb/maap/mutants.py --output "$out/maap" --jobs 1
  run adp_mutants python3 tb/adp_engine/mutants.py --output "$out/adp" --jobs 1
  run gsi_mutants python3 tb/pp_top/gsi_mutants.py --output "$out/gsi"
  run aecp_mutants python3 tb/pp_top/aecp_mutants.py --output "$out/aecp"
  run aecp_dispatch_mutants python3 tb/pp_top/aecp_dispatch_mutants.py --output "$out/aecp_dispatch"
  run notify_mutants python3 tb/pp_top/notify_mutants.py --output "$out/notify" --jobs 1
fi
