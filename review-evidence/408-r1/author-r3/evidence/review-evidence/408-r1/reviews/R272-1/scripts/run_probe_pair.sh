#!/usr/bin/env bash
# Run one probe case file at head and at base, in one compiler mode, in parallel.
# Usage: run_probe_pair.sh <packet> <head-tree> <base-tree> <sdk-dir|absent> <cases.py> <tag>
set -u
packet=$1 head=$2 base=$3 mode=$4 cases=$5 tag=$6
out="$packet/receipts/probes"
mkdir -p "$out"
# Scoped Verilator 5.050 for the RTL mutant elaboration; override with R272_VERILATOR_BIN.
export PATH="${R272_VERILATOR_BIN:-$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin}:$PATH"
if [ "$mode" = absent ]; then flag=(--absent); m=absent; else flag=(--sdk "$mode"); m=sdk; fi
for side in head base; do
  tree=$head; [ "$side" = base ] && tree=$base
  (
    python3 -B "$packet/scripts/probe_gate1b.py" --tree "$tree" "${flag[@]}" \
      --cases "$cases" --out "$out/$tag-$side-$m.json" \
      > "$out/$tag-$side-$m.log" 2>&1
    echo "exit=$?" >> "$out/$tag-$side-$m.log"
  ) &
done
wait
for side in head base; do
  echo "== $side ($m)"
  grep -E '^(ACCEPTED|REFUSED|PROBE DONE|exit=)' "$out/$tag-$side-$m.log"
done
