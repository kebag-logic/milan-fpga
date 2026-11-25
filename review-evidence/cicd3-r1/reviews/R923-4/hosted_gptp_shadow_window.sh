#!/bin/sh
# Read-only: for one hosted run, find the Verilator worker that ran gptp_shadow
# and print that suite's start and result lines. Usage: hosted_gptp_shadow_window.sh RUN_ID OUTDIR
run=$1; out=$2; mkdir -p "$out"
gh api "repos/kebag-logic/milan-fpga/actions/runs/$run/jobs?per_page=100" --paginate \
  -q '.jobs[] | select(.name|test("^Verilator shard")) | "\(.id)\t\(.name)"' |
while IFS="$(printf '\t')" read -r id name; do
  gh run view "$run" -R kebag-logic/milan-fpga --log --job "$id" > "$out/$id.log" 2>/dev/null
  if grep -q "gptp_shadow" "$out/$id.log"; then
    echo "== run $run job $id $name"
    grep -n "gptp_shadow\|^.\{28\}=== \|RESULT\|SUITE\|PASS  \|suite " "$out/$id.log" | grep -i -B1 -A3 "gptp_shadow" | head -20
  fi
done
