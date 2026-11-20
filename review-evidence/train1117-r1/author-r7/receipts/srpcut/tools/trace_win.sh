#!/bin/bash
# trace_win.sh BUILD RESULTS GROUP AFTER PCS OUT: a measured group's committed PCs from bus cycle AFTER, PCS of them
# (sim_main.cpp's BUDGET_TRACE_AFTER and BUDGET_TRACE_PCS), into OUT; the simulation is stopped once they are out
# (head closes the pipe). Scratch only: the SRP cut's profile (#665's ruling of 2026-11-20, item 3).
set -u
T=<scratch>; . $T/bin/env.sh
B=$1 R=$2 G=$3 A=$4 N=$5 O=$6
echo "trace $G from $A, $N PCs, start $(date +%T)"
(cd $B/gateware && BUDGET_TRACE_AFTER=$A BUDGET_TRACE_PCS=$N $B/native/Vsim $R/$G.txt - 2>/dev/null | grep --line-buffered '^PC ' | head -n $N > $O)
echo "$(wc -l < $O) PCs, end $(date +%T)"
