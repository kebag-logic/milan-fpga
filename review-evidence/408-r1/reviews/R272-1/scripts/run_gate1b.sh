#!/usr/bin/env bash
# Run gate 1b at the checked-out head, once with the pinned RV32 SDK mapped and
# once with every cross compiler hidden, in parallel (two jobs).
# Usage: run_gate1b.sh <clone> <sdk-dir> <verilator-bin-dir> <receipt-dir> <tag>
set -u
clone=$1 sdk=$2 vbin=$3 out=$4 tag=$5
mkdir -p "$out"
cd "$clone" || exit 2
export PATH="$vbin:$PATH"
command -v verilator > "$out/$tag-verilator-path.txt"
verilator --version >> "$out/$tag-verilator-path.txt"
git rev-parse HEAD > "$out/$tag-head.txt"
date -u +%FT%TZ > "$out/$tag-time.txt"
(
  python3 -B sw/builder/test_firmware_compiler.py --sdk-destination "$sdk" \
    --audit "$out/$tag-gate1b-sdk.audit.jsonl" > "$out/$tag-gate1b-sdk.log" 2>&1
  echo "exit=$?" >> "$out/$tag-gate1b-sdk.log"
) &
(
  python3 -B sw/builder/test_firmware_compiler.py --absent \
    --audit "$out/$tag-gate1b-absent.audit.jsonl" > "$out/$tag-gate1b-absent.log" 2>&1
  echo "exit=$?" >> "$out/$tag-gate1b-absent.log"
) &
wait
date -u +%FT%TZ >> "$out/$tag-time.txt"
tail -n 3 "$out/$tag-gate1b-sdk.log"
tail -n 3 "$out/$tag-gate1b-absent.log"
