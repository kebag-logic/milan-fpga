#!/usr/bin/env bash
# Run one batch of the docs gate set; append "rc<TAB>command" to $OUT/EXITS.txt and each log to $OUT/logs/.
set -u
PY=${PY:-/tmp/a212/gates/bin/python}
OUT=${OUT:-$MANAGEMENT/2026-09-23/437-a212/gates}
mkdir -p "$OUT/logs"
n=$(ls "$OUT/logs" | wc -l)
while IFS= read -r cmd; do
  [ -z "$cmd" ] && continue
  n=$((n+1)); log=$(printf "%s/logs/%03d.log" "$OUT" "$n")
  echo "\$ $cmd" > "$log"
  start=$(date +%s)
  bash -c "${cmd//python3 /$PY -B }" >> "$log" 2>&1
  rc=$?
  printf "%s\t%ss\t%s\n" "$rc" "$(( $(date +%s) - start ))" "$cmd" | tee -a "$OUT/EXITS.txt"
done
