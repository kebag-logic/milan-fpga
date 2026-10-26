#!/bin/bash
# Regrade every arm and control of round 3 from its results directory, on its attested build.
# Usage: regrade_r3.sh CHECKOUT BUILDS RUNS LOGS
set -u
C=$1 B=$2 R=$3 L=$4
H=$C/tb/verilator/ctrl_service_budget/run.py
G=acmp-cmd,acmp-noresp,acmp-notk,acmp-disc,backlog,backlog-adp,backlog-owed,aecp-fanout
go() { local name=$1; shift; python3 -B "$H" "$@" > "$L/regrade-$name.log" 2>&1; echo "$name rc=$? $(tail -1 "$L/regrade-$name.log")"; }
go A1 --point 1x1 --build-dir "$B/A1" --regrade --out "$R/A1" --record-budget-findings
go A8 --point 8x8 --build-dir "$B/A8" --regrade --out "$R/A8" --record-budget-findings
go B1 --point 1x1 --build-dir "$B/B1" --variant answering-ports --groups $G --regrade --out "$R/B1" --record-budget-findings
go B8 --point 8x8 --build-dir "$B/B8" --variant answering-ports --groups $G --regrade --out "$R/B8" --record-budget-findings
go S1 --point 1x1 --build-dir "$B/S1" --variant shutdown-entry --regrade --out "$R/S1" --record-budget-findings
go S8 --point 8x8 --build-dir "$B/S8" --variant shutdown-entry --regrade --out "$R/S8" --record-budget-findings
go C-slow --point 1x1 --build-dir "$B/C-slow" --mutation slow-adp-rx --regrade --out "$R/C-slow"
go C-shutdown --point 1x1 --build-dir "$B/C-shutdown" --variant shutdown-entry --mutation slow-adp-shutdown --regrade --out "$R/C-shutdown"
go C-asbuilt --point 1x1 --build-dir "$B/C-asbuilt" --cpu-regions as-built --regrade --out "$R/C-asbuilt"
