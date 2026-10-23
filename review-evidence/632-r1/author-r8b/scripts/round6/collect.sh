#!/usr/bin/env bash
# Copy round-5 scratch logs into receipts/round6/<label>/ with host paths stripped;
# a file of 200 KB or more is recorded by sha256 and size only.
# usage: collect.sh <label> <file>...
set -u
label=$1; shift
out=$MANAGEMENT/2026-09-23/632-a659/receipts/round6/$label
mkdir -p "$out"
strip() { sed -E -e 's#$VALIDATION_STORAGE/[A-Za-z0-9._/+-]*#<host path>#g' -e 's#$WORKSPACE_HOME/[A-Za-z0-9._/+-]*#<host path>#g' \
                 -e 's#/tmp/[A-Za-z0-9._/+-]*#<tmp path>#g'; }
for f in "$@"; do
  [ -f "$f" ] || { echo "missing $f"; continue; }
  if [ "$(stat -c %s "$f")" -lt 200000 ]; then
    strip < "$f" > "$out/$(basename "$f")"
  else
    printf '%s  %s bytes  %s\n' "$(sha256sum < "$f" | cut -d' ' -f1)" "$(stat -c %s "$f")" "$(basename "$f")" >> "$out/large_logs.sha256"
  fi
done
ls "$out" | wc -l
