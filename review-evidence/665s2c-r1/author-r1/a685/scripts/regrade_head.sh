#!/bin/bash
# Regrade every arm at the head, on its attested build, and compare each table with the one the arm's run wrote.
# usage: regrade_head.sh CHECKOUT OUT
set -u
. $MANAGEMENT/2026-09-23/665s2c-a685/scripts/env.sh
C=$1 O=$2
B=$VALIDATION_STORAGE/665s2c-a685/builds
H=$C/tb/verilator/ctrl_service_budget/run.py
G=acmp-cmd,acmp-noresp,acmp-notk,acmp-disc,backlog,backlog-adp,backlog-owed,aecp-fanout
mkdir -p "$O"
go() {  # NAME POINT GEOM [args...]
  local name=$1 point=$2 geom=$3; shift 3
  cp "$B/$name/results/table.md" "$O/$name.before.md"
  python3 -B "$H" --point "$point" --build-dir "$B/$name" --fetch-l1 "$geom" --regrade --out "$B/$name/results" "$@" \
    > "$O/$name.regrade.log" 2>&1
  local rc=$?
  if cmp -s "$O/$name.before.md" "$B/$name/results/table.md"; then same=identical; else same=DIFFERENT; fi
  echo "$name rc=$rc table=$same $(tail -n 1 "$O/$name.regrade.log")"
  rm -f "$O/$name.before.md"
}
for g in none 32x1 64x1 128x1 64x2 256x1; do
  go P1-$g 1x1 $g --record-budget-findings
  go P8-$g 8x8 $g --record-budget-findings
done
go B1-64x1 1x1 64x1 --variant answering-ports --groups $G --record-budget-findings
go B8-64x1 8x8 64x1 --variant answering-ports --groups $G --record-budget-findings
go S1-64x1 1x1 64x1 --variant shutdown-entry --record-budget-findings
go S8-64x1 8x8 64x1 --variant shutdown-entry --record-budget-findings
go C1-asbuilt-64x1 1x1 64x1 --cpu-regions as-built
go C1-slow-64x1 1x1 64x1 --mutation slow-adp-rx
go C1-shutdown-64x1 1x1 64x1 --variant shutdown-entry --mutation slow-adp-shutdown
for a in "P1-xip-64x1 1x1 64x1" "P8-xip-64x1 8x8 64x1" "P1-xip-512x1 1x1 512x1" "P8-xip-512x1 8x8 512x1"; do
  set -- $a
  [ -f "$B/$1/build.json" ] && go "$1" "$2" "$3" --xip --record-budget-findings
done
