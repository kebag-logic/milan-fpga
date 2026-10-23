#!/usr/bin/env bash
# Copy one sweep shard's receipts into receipts/sweep_<head>/shard<i>/: the
# runner's summary, its rc and timestamps, and every suite log under 200 KB with
# host paths stripped; a larger log is recorded by sha256 and size only.
# usage: collect_sweep.sh <sweep out dir> <shard> <label>
set -euo pipefail
src=$1; i=$2; label=$3
out=$MANAGEMENT/2026-09-23/632-a659/receipts/round4/$label/shard$i
mkdir -p "$out"
strip() { sed -E -e 's#$VALIDATION_STORAGE/[A-Za-z0-9._/+-]*#<host path>#g' -e 's#$WORKSPACE_HOME/[A-Za-z0-9._/+-]*#<host path>#g' \
                 -e 's#/tmp/[A-Za-z0-9._/+-]*#<tmp path>#g'; }
cp "$src/HEAD.txt" "$out/HEAD.txt"
for f in start end rc; do [ -f "$src/shard$i.$f" ] && cp "$src/shard$i.$f" "$out/shard.$f"; done
strip < "$src/shard$i.summary" > "$out/summary.txt"
: > "$out/large_logs.sha256"
for log in "$src/shard$i"/*.log; do
  [ -f "$log" ] || continue
  if [ "$(stat -c %s "$log")" -lt 200000 ]; then
    strip < "$log" > "$out/$(basename "$log")"
  else
    printf '%s  %s bytes  %s\n' "$(sha256sum < "$log" | cut -d' ' -f1)" "$(stat -c %s "$log")" "$(basename "$log")" >> "$out/large_logs.sha256"
  fi
done
ls "$out" | wc -l
