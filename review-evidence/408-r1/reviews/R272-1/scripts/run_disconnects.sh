#!/usr/bin/env bash
# Grade the retired rules' hostile controls at head with each replacement
# instrument disconnected in memory, in parallel (at most 7 jobs).
# Usage: run_disconnects.sh <packet> <head-tree> <sdk-dir>
set -u
packet=$1 head=$2 sdk=$3
out="$packet/receipts/disconnect"
mkdir -p "$out"
# Scoped Verilator 5.050 for the RTL mutant elaboration; override with R272_VERILATOR_BIN.
export PATH="${R272_VERILATOR_BIN:-$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin}:$PATH"
p="$packet/scripts/patches"
run() {  # tag, mode flag(s)..., then patches
  local tag=$1; shift
  python3 -B "$packet/scripts/probe_gate1b.py" --tree "$head" --anchor mutations \
    --cases "$packet/scripts/cases_disconnect.py" --out "$out/$tag.json" "$@" \
    > "$out/$tag.log" 2>&1
  echo "exit=$?" >> "$out/$tag.log"
}
run connected-sdk --sdk "$sdk" &
run connected-absent --absent &
# With the per-selection grading disconnected the gate's own accepted-case
# loop refuses the guarded printf (the dependency this measures), so these
# two runs skip the accepted loops to reach the mutation-table hook.
skip=(--patch "$p/skip-accepted-loops.json")
run sel-sdk --sdk "$sdk" --patch "$p/disconnect-sel.json" "${skip[@]}" &
run sel-absent --absent --patch "$p/disconnect-sel.json" "${skip[@]}" &
run e-sdk --sdk "$sdk" --patch "$p/disconnect-e.json" &
run h-sdk --sdk "$sdk" --patch "$p/disconnect-h.json" &
run res-sdk --sdk "$sdk" --patch "$p/disconnect-res.json" &
wait
run eres-sdk --sdk "$sdk" --patch "$p/disconnect-e.json" --patch "$p/disconnect-res.json"
for f in "$out"/*.log; do
  echo "== $(basename "$f" .log): $(grep -c '^ACCEPTED' "$f") accepted, \
$(grep -c 'pin_ok=True' "$f") refused on pin, $(grep -c 'REFUSED pin_ok=False' "$f") refused off pin; $(tail -n 1 "$f")"
done
