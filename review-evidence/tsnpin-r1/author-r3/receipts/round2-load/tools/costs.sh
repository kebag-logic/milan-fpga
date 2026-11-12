#!/bin/bash
# costs.sh OUTDIR POINT N_IF HARNESS_DIR BUILD_DIR...: one leg's measured costs, by S2b's own parsers (#665 round 25's
# costs25.sh, its tools unchanged: round 21's parts.py, round 20's eventcost.py, round 24's costs24.py, aecp_kinds.py).
set -eu
O=$1 P=$2 N=$3 H=$4; shift 4
T=<scratch>/tools/s2b
mkdir -p "$O"
R=(); for b in "$@"; do R+=("$b/results"); done
python3 -I $T/parts.py "$O/parts.json" "${R[@]}" > "$O/parts.txt"
python3 -I $T/eventcost.py "${R[@]}" > "$O/events.json"
python3 -I $T/costs24.py "$O/costs.json" "$P" "$N" "$O/parts.json" "$O/events.json" "${R[@]}" > "$O/costs.txt"
python3 -I $T/aecp_kinds.py "$H" "$O/aecp.json" "$@" > "$O/aecp.txt"
cat "$O/costs.txt" "$O/aecp.txt"
