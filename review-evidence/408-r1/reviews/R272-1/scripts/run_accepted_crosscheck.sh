#!/usr/bin/env bash
# Grade the retired-rule accepted cases at head (both environments), then the
# same texts at base (both environments); and, beside the head runs, show that
# disconnecting the resolver function fails the exempted-helper blindness
# control that carries #409 acceptance 4.
# Usage: run_accepted_crosscheck.sh <packet> <head-tree> <base-tree> <sdk-dir>
set -u
packet=$1 head=$2 base=$3 sdk=$4
out="$packet/receipts/accepted"
mkdir -p "$out"
# Scoped Verilator 5.050 for the RTL mutant elaboration; override with R272_VERILATOR_BIN.
export PATH="${R272_VERILATOR_BIN:-$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin}:$PATH"
probe() {  # tag tree dump mode...
  local tag=$1 tree=$2 dump=$3; shift 3
  R272_ACCEPTED_DUMP=$dump python3 -B "$packet/scripts/probe_gate1b.py" \
    --tree "$tree" --cases "$packet/scripts/cases_accepted.py" \
    --out "$out/$tag.json" "$@" > "$out/$tag.log" 2>&1
  echo "exit=$?" >> "$out/$tag.log"
}
dump="$packet/scratch/retired_rule_cases.json"
probe head-sdk "$head" "$dump" --sdk "$sdk" &
probe head-absent "$head" "$packet/scratch/retired_rule_cases-absent.json" --absent &
(
  python3 -B "$packet/scripts/probe_gate1b.py" --tree "$head" \
    --cases "$packet/scripts/cases_r1.py" --out "$out/resolver-off-sdk.json" \
    --sdk "$sdk" --patch "$packet/scripts/patches/disconnect-resolver-function.json" \
    > "$out/resolver-off-sdk.log" 2>&1
  echo "exit=$?" >> "$out/resolver-off-sdk.log"
) &
wait
cmp "$dump" "$packet/scratch/retired_rule_cases-absent.json" && echo "dumps identical"
probe base-sdk "$base" "$dump" --sdk "$sdk" &
probe base-absent "$base" "$dump" --absent &
wait
for f in "$out"/*.log; do
  echo "== $(basename "$f" .log)"
  grep -E '^(ACCEPTED|REFUSED|PROBE DONE|exit=|AssertionError)' "$f"
done
