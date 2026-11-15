#!/bin/bash
# A committed-PC trace of one group's sim on a built tree, from bus cycle AFTER for PCS commits (sim_main.cpp's
# BUDGET_TRACE_AFTER / BUDGET_TRACE_PCS), into OUT. usage: trace.sh BUILD GROUP AFTER PCS OUT
set -eu
B=$1 G=$2 A=$3 N=$4 O=$5
cd "$B/gateware"
BUDGET_TRACE_AFTER=$A BUDGET_TRACE_PCS=$N "$B/native/Vsim" "$B/results/$G.txt" - > "$O"
echo "END $(date +%FT%T)"
