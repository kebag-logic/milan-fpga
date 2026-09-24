#!/usr/bin/env bash
# R272-5: grade the allowlist entries and reviewer shapes connected and with
# the allowlist disconnected (in-memory, count-checked patch), in both modes.
# Absent runs go in parallel (2 jobs); SDK runs one at a time (each spawns up
# to 8 compiler threads).
# Usage: run_disconnect.sh <packet> <clone> <sdk-dir>
set -u
packet=$1 clone=$2 sdk=$3
out="$packet/receipts/r5/disconnect"
mkdir -p "$out"
export PATH="${R272_VERILATOR_BIN:-$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin}:$PATH"
probe="$packet/scripts/r1/probe_gate1b.py"
cases="$packet/scripts/r5/cases_r5_disconnect.py"
patchf="$packet/scripts/r5/patches/disconnect-allowlist.json"
run() { # tag mode-args... (R272_TAG_PREFIX prefixes every tag)
  local tag="${R272_TAG_PREFIX:-}$1"; shift
  python3 -B "$probe" --tree "$clone" --anchor mutations --cases "$cases" \
    --out "$out/$tag.json" "$@" > "$out/$tag.log" 2>&1
  echo "exit=$?" >> "$out/$tag.log"
}
run connected-absent --absent &
run disconnected-absent --absent --patch "$patchf" &
wait
run connected-sdk --sdk "$sdk"
run disconnected-sdk --sdk "$sdk" --patch "$patchf"
for tag in connected-absent disconnected-absent connected-sdk disconnected-sdk; do tag="${R272_TAG_PREFIX:-}$tag"
  echo "== $tag"
  grep -E '^(ACCEPTED|REFUSED|PROBE DONE|exit=|Traceback|AssertionError)' "$out/$tag.log"
done
