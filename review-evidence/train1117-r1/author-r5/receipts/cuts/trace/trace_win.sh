#!/bin/bash
# trace_win.sh BUILD PART GROUP AFTER_SYS NPCS OUT: committed PCs of a group's run from AFTER_SYS for NPCS, the
# simulation stopped once they are written. Scratch only.
set -u
. <scratch>/bin/env.sh
B=$1 K=$2 G=$3 A=$4 N=$5 O=$6
cd $B/gateware && BUDGET_TRACE_AFTER=$A BUDGET_TRACE_PCS=$N $B/native/Vsim $B/$K/$G.txt - 2>/dev/null | grep --line-buffered '^PC ' | head -n $N > $O
echo "$(wc -l < $O) PCs $(date +%T)"
