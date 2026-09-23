#!/usr/bin/env bash
# Measured gate 1b runs at the committed head, 8 concurrent jobs at most.
# Usage: run_final_gates.sh <checkout> <packet-dir> <sdk-prefix> <verilator-bin-dir>
set -uo pipefail
checkout=$1 packet=$2 sdk=$3 vbin=$4
logs="$packet/receipts/gate1b"
mkdir -p "$logs"
cd "$checkout" || exit 2
head=$(git rev-parse HEAD)
run() {  # name args...
  local name=$1; shift
  ( start=$(date +%s)
    PATH="$vbin:$PATH" python3 -u "$@" > "$logs/$name.log" 2>&1; rc=$?
    echo "exit=$rc elapsed=$(( $(date +%s) - start ))s head=$head dirty=$(git status --porcelain | wc -l)" \
      > "$logs/$name.exit" ) &
}
run pristine-sdk sw/builder/test_firmware_compiler.py --sdk-destination "$sdk" --audit "$logs/pristine-sdk-argv.jsonl"
run pristine-absent sw/builder/test_firmware_compiler.py --absent --audit "$logs/pristine-absent-argv.jsonl"
run capture-all "$packet/scripts/capture_census.py" "$checkout" "$sdk" "$packet/scratch/capture-all" 1000000
run mutants-slow-and-plants "$packet/scripts/mutate_store_classes.py" drive "$checkout" "$sdk" "$packet/scratch/mut-f1" "$vbin" \
  "pre-fix classification and literal-assembly control removed" \
  "pre-fix classification, literal control and compiled measurement removed" \
  plant-float plant-double plant-uint32
wait
for f in "$logs"/*.exit; do echo "$(basename "$f" .exit): $(cat "$f")"; done
