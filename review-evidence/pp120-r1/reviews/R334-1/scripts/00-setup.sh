#!/usr/bin/env bash
# Export exact base and head trees into disposable scratch copies (the clone stays untouched).
set -euo pipefail
PK=$(cd "$(dirname "$0")/.." && pwd); CLONE=${CLONE:-$REVIEWS/r334-1-pp120}
BASE=0922e43408f891fc0b84a84691df86b4fd0f1c0d; HEAD=a9b7874d415d935949becd7ccfd58799927efb08
for n in base:$BASE head:$HEAD; do
  d=$PK/scratch/${n%%:*}; rm -rf "$d"; mkdir -p "$d"
  git -C "$CLONE" archive "${n#*:}" | tar -x -C "$d"
  # parallelism only: cap Verilator build jobs at 8 in the scratch copies
  grep -rl -- '--build -j 0' "$d/tb" | xargs -r sed -i 's/--build -j 0/--build -j 8/'
done
echo "exported base $BASE and head $HEAD"
