#!/bin/bash
# Regrade every S2c arm at the re-based head, on its attested build, from a copy of the logs its
# run recorded; the build's own results are left as the run wrote them.
# usage: regrade_rebased.sh CHECKOUT BUILDS OUT
set -u
. $MANAGEMENT/2026-09-23/665s2c-a685/scripts/env.sh
C=$1 B=$2 O=$3
H=$C/tb/verilator/ctrl_service_budget/run.py
G=acmp-cmd,acmp-noresp,acmp-notk,acmp-disc,backlog,backlog-adp,backlog-owed,aecp-fanout
mkdir -p "$O"
go() {  # NAME POINT GEOM [args...]
  local name=$1 point=$2 geom=$3; shift 3
  rm -rf "${O:?}/$name"
  mkdir -p "$O/$name"
  cp -a "$B/$name/results/." "$O/$name/"
  cp "$B/$name/results/table.md" "$O/$name.before.md"
  python3 -B "$H" --point "$point" --build-dir "$B/$name" --fetch-l1 "$geom" --regrade --out "$O/$name" "$@" \
    > "$O/$name.regrade.log" 2>&1
  local rc=$?
  echo "rc=$rc" >> "$O/$name.regrade.log"
  echo "$name rc=$rc $(tail -n 2 "$O/$name.regrade.log" | head -n 1)"
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
go P1-xip-64x1 1x1 64x1 --xip --record-budget-findings
go P8-xip-64x1 8x8 64x1 --xip --record-budget-findings
go P1-xip-512x1 1x1 512x1 --xip --record-budget-findings
go P8-xip-512x1 8x8 512x1 --xip --record-budget-findings
