#!/usr/bin/env bash
# Focused gate 1b runs (at most 5 in parallel), each with its own log/exit.
# Usage: run_focused_gates.sh <out-dir> <clone>
set -uo pipefail
out=$1 clone=$2
sdk="$out/sdk-fresh/host"
# Directory holding the scoped Verilator 5.050 wrapper (identity in receipt 15).
vbin=${VERILATOR_BIN_DIR:-$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin}
logs="$out/receipts/gate1b"
mkdir -p "$logs"
run() {  # name dir args...
  local name=$1 dir=$2; shift 2
  ( cd "$dir" && start=$(date +%s) &&
    PATH="$vbin:$PATH" python3 -u sw/builder/test_firmware_compiler.py "$@" \
      > "$logs/$name.log" 2>&1; rc=$?
    echo "exit=$rc elapsed=$(( $(date +%s) - start ))s head=$(git -C "$dir" rev-parse HEAD) dirty=$(git -C "$dir" status --porcelain | wc -l)" \
      > "$logs/$name.exit" ) &
}
run pristine-sdk "$clone" --sdk-destination "$sdk" --audit "$logs/pristine-sdk-argv.jsonl"
run pristine-absent "$clone" --absent --audit "$logs/pristine-absent-argv.jsonl"
for k in float double uint32; do
  run "probe-$k" "$out/scratch-$k" --sdk-destination "$sdk" --audit "$logs/probe-$k-argv.jsonl"
done
wait
for f in "$logs"/*.exit; do echo "$(basename "$f" .exit): $(cat "$f")"; done
