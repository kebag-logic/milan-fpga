#!/usr/bin/env bash
# Grade case files through gate 1b's own assert_boot_contract() at dev and at
# the head, with the pinned SDK and with every cross compiler hidden.
# usage: run_probes.sh <packet-dir> <lane> <sdk> <job>...   job = name:rev:mode:cases
set -u
packet=$1 lane=$2 sdk=$3; shift 3
export R273_LANE=$lane
export PATH=${R273_TOOL_BIN:?set R273_TOOL_BIN to the scoped Verilator 5.050 directory}:$PATH
cd "$packet/scratch"
for job in "$@"; do
  IFS=: read -r name rev mode cases <<<"$job"
  args=(--cases "$packet/cases/$cases" --out "$packet/receipts/$name.json")
  [ "$rev" != head ] && args+=(--rev "$rev")
  if [ "$mode" = sdk ]; then args+=(--sdk "$sdk"); else args+=(--absent); fi
  ( python3 -B "$packet/probes/probe.py" "${args[@]}" > "$packet/receipts/$name.log" 2>&1
    echo "$name rc=$?" ) &
done
wait
