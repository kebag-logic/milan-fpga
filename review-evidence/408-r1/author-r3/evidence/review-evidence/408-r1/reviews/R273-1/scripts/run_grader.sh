#!/usr/bin/env bash
# Grader-shape probes at head in both environments. Usage: run_grader.sh <packet> <sdk>
set -u
packet=$1; sdk=$2; out=$packet/receipts/21-grader; mkdir -p "$out"
for mode in sdk absent; do
  if [ "$mode" = sdk ]; then flag=(--sdk "$sdk"); else flag=(--absent); fi
  ( cd "$packet/scratch/head" || exit 2
    python3 -B "$packet/scripts/probe.py" --checkout . "${flag[@]}" --cases "$packet/cases/grader.json" \
      --out "$out/head-$mode.json" > "$out/head-$mode.txt" 2>&1; echo "exit=$?" >> "$out/head-$mode.txt" ) &
done
wait
grep -hE '^(ACCEPTED|REFUSED)|^mode=|^exit=|^ +->' "$out"/head-*.txt
