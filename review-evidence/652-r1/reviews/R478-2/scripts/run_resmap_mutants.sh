#!/bin/sh
# Run every row of resmap_mutants.tsv through mutate_module.py (in memory),
# 16 at a time, one log per mutant, then tabulate verdict against expectation.
# Usage: run_resmap_mutants.sh <clone> <packet dir>
C=$1; P=$2; R=$P/receipts/mut; mkdir -p "$R"
grep -v '^#' "$P/scripts/resmap_mutants.tsv" > "$R/.rows"
while IFS="$(printf '\t')" read -r id mod old new want; do
  ( cd "$C" && python3 "$P/scripts/mutate_module.py" "$mod" "$old" "$new" > "$R/$id.log" 2>&1 ) &
  while [ "$(jobs -r | wc -l)" -ge 16 ]; do sleep 1; done
done < "$R/.rows"; wait
grep -v '^#' "$P/scripts/resmap_mutants.tsv" | while IFS="$(printf '\t')" read -r id mod old new want; do
  got=$(grep -o 'SELFTEST rc=[0-9]*' "$R/$id.log" | tail -1); [ -n "$got" ] || got="$(tail -1 "$R/$id.log")"
  case "$got" in "SELFTEST rc=0") v=green;; "SELFTEST rc=1") v=red;; *) v="other";; esac
  ok=$([ "$want" = "$v" ] && echo AS-EXPECTED || echo "UNEXPECTED")
  [ "$want" = report ] && ok=REPORTED
  echo "$id want=$want got=$v $ok | $(grep -m2 'FAILED\|raised\|anchor' "$R/$id.log" | tr '\n' ' ' | cut -c1-300)"
done
