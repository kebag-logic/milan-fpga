#!/bin/bash
# collect_receipts.sh <job-dir-name> [step-tag:label ...]
# Copy one replayed job's driver log, summary and the named step logs into
# receipts/replay/, with the home prefix written $HOME. Refuse a copy over
# 200 KB (keep its tail instead, marked).
set -u
R=$VALIDATION_STORAGE/629-a517/replay
D=$HOME/milan-fpga-management/2026-09-23/629-a517/receipts/replay
mkdir -p "$D"
job=$1; shift
mask() { sed -e "s#$HOME#\$HOME#g" "$1"; }
cap() {  # cap <src> <dst>
  mask "$1" > "$2"
  if [ "$(stat -c %s "$2")" -gt 200000 ]; then
    { echo "### TAIL ONLY: the full log is $(stat -c %s "$1") B, sha256 $(sha256sum "$1" | cut -d' ' -f1)"; mask "$1" | tail -n 400; } > "$2"
  fi
}
cap "$R/$job.log" "$D/$job.log"
cp "$R/$job/summary.json" "$D/$job.summary.json"
[ -f "$R/$job/make_invocations.tsv" ] && cut -f1 "$R/$job/make_invocations.tsv" | sort | uniq -c > "$D/$job.make_calls_per_step.txt"
for item in "$@"; do
  tag=${item%%:*}; label=${item#*:}
  cap "$R/$job/step_$tag.log" "$D/$job.step$tag.$label.log"
done
