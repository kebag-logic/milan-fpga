#!/bin/bash
# Run every mutant of mutants.py, each in its own disposable copy of the checkout, on one Git, all pin controls.
# Usage: mutant_campaign.sh <checkout> <scratch-dir> <receipts-dir> <git-bin-dir|system> <tag> [mutant ...]
# Each run is bounded by 300 s (a mutant that lets Git fetch from itself may recurse; rc=124 is a timeout).
set -u
SRC=$1; SCR=$2; REC=$3; GBIN=$4; TAG=$5; shift 5
LIST=${*:-$(python3 -I "$(dirname "$0")/mutants.py" --list)}
HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$SCR" "$REC"
for m in $LIST; do
  (
    copy="$SCR/copy-$TAG-$m"
    rm -rf "$copy"; cp -a "$SRC" "$copy"
    python3 -I "$HERE/mutants.py" "$copy" "$m" > "$REC/mutant_${TAG}_$m.log" 2>&1 || { echo rc=apply > "$REC/mutant_${TAG}_$m.rc"; exit; }
    if [ "$GBIN" = system ]; then P=$PATH; else P=$GBIN:$PATH; fi
    PATH=$P timeout -k 10 300 python3 -I "$HERE/run_pins.py" "$copy" "$copy.work" >> "$REC/mutant_${TAG}_$m.log" 2>&1
    echo "rc=$?" > "$REC/mutant_${TAG}_$m.rc"
    rm -rf "$copy" "$copy.work"
  ) &
done
wait
for m in $LIST; do
  log="$REC/mutant_${TAG}_$m.log"
  printf '%-26s %s escaped=%s %s\n' "$m" "$(cat "$REC/mutant_${TAG}_$m.rc")" "$(grep -c '^\[ESCAPED\]' "$log")" "$(grep '^PINS' "$log" || tail -1 "$log")"
done
