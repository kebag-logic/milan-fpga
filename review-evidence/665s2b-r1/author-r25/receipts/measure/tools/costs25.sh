#!/bin/bash
# Round 25 (#665): one column's measured costs at a point from its traced legs: round 21's parts.py, round 20's
# eventcost.py and round 24's costs24.py (unchanged), and this round's aecp_kinds.py. usage:
#   costs25.sh OUTDIR POINT N_IF HARNESS_DIR BUILD_DIR...
set -eu
O=$1 P=$2 N=$3 H=$4; shift 4
T=<scratch>/tools
mkdir -p "$O"
R=(); for b in "$@"; do R+=("$b/results"); done
python3 -I $T/parts.py "$O/parts.json" "${R[@]}" > "$O/parts.txt"
python3 -I $T/eventcost.py "${R[@]}" > "$O/events.json"
python3 -I $T/costs24.py "$O/costs.json" "$P" "$N" "$O/parts.json" "$O/events.json" "${R[@]}" > "$O/costs.txt"
python3 -I $T/aecp_kinds.py "$H" "$O/aecp.json" "$@" > "$O/aecp.txt"
cat "$O/costs.txt" "$O/aecp.txt"
