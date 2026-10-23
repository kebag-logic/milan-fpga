#!/usr/bin/env bash
# Copy logs into receipts/round4/<label>/ with host paths stripped; a file over
# 200 KB is recorded by sha256 and size only. usage: collect_logs.sh <label> <file>...
set -euo pipefail
label=$1; shift
out=$MANAGEMENT/2026-09-23/632-a659/receipts/round4/$label
mkdir -p "$out"
strip() { sed -E -e 's#$VALIDATION_STORAGE/[A-Za-z0-9._/+-]*#<host path>#g' -e 's#$WORKSPACE_HOME/[A-Za-z0-9._/+-]*#<host path>#g' \
                 -e 's#/tmp/[A-Za-z0-9._/+-]*#<tmp path>#g'; }
for f in "$@"; do
  [ -f "$f" ] || continue
  name=$(basename "$f")
  if [ "$(stat -c %s "$f")" -lt 200000 ]; then
    strip < "$f" > "$out/$name"
  else
    printf '%s  %s bytes  %s\n' "$(sha256sum < "$f" | cut -d' ' -f1)" "$(stat -c %s "$f")" "$name" >> "$out/large_logs.sha256"
  fi
done
ls "$out" | wc -l
