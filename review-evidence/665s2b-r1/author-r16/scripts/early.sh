#!/bin/bash
# Grade a running leg's finished groups from copies of their scripts and logs (a pre-check, never a result).
# usage: early.sh LEG POINT [run.py args]
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683u/scripts/env.sh
T=$VALIDATION_STORAGE/665s2b-a683u
LEG=$1 POINT=$2; shift 2
Q=$T/early/$LEG
rm -rf "$Q"; mkdir -p "$Q"
names=""
for f in $(grep -l "^SUMMARY " $T/builds/$LEG/results/*.log $T/builds/$LEG/results-$LEG-rest/*.log 2>/dev/null); do
    g=$(basename "$f" .log)
    cp "$f" "${f%.log}.txt" "$Q/"
    names="$names,$g"
done
names=${names#,}
echo "$LEG: $names"
[ -z "$names" ] && exit 0
CK=C; case $LEG in D-*) CK=CD ;; esac
cd $T/$CK && python3 -B tb/verilator/ctrl_service_budget/run.py --point "$POINT" --build-dir "$T/builds/$LEG" --reuse-build \
  --regrade --out "$Q" --groups "$names" --record-budget-findings --record-share-findings "$@" > "$Q.regrade.log" 2>&1
echo "rc=$?"
grep -v "^COMMAND" "$Q.regrade.log" | tail -12 | cut -c1-260
