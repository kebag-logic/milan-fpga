#!/usr/bin/env bash
# Gate 1b at the committed head through the lane's own driver, SDK mapped and
# cross tools absent, each with its argv audit, log, exit and elapsed time.
# Usage: run_pristine_gates.sh <checkout> <sdk-prefix> <out-dir> <verilator-bin-dir>
set -uo pipefail
checkout=$1 sdk=$2 out=$3 vbin=$4
mkdir -p "$out"
cd "$checkout" || exit 2
head=$(git rev-parse HEAD)
one() {  # name args...
  local name=$1; shift
  local start; start=$(date +%s)
  PATH="$vbin:$PATH" python3 -u sw/builder/test_firmware_compiler.py "$@" \
    --audit "$out/$name-argv.jsonl" > "$out/$name.log" 2>&1
  local rc=$?
  echo "exit=$rc elapsed=$(( $(date +%s) - start ))s head=$head dirty=$(git status --porcelain | wc -l) argv=$*" > "$out/$name.exit"
  echo "$name exit=$rc $(grep -E '^GATE 1b' "$out/$name.log" | tail -1)"
}
one pristine-sdk --sdk-destination "$sdk" &
one pristine-absent --absent &
wait
