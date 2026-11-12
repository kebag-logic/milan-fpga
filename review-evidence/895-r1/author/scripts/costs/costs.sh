#!/bin/bash
# costs.sh OUTDIR POINT N_IF HARNESS_DIR BUILD_DIR...: one point's measured costs over its legs, by S2b's own parsers
# (#665 round 21's parts.py, round 20's eventcost.py, round 24's costs24.py, round 25's aecp_kinds.py, unchanged).
set -eu
O=$1 P=$2 N=$3 H=$4; shift 4
T=$(dirname "$(readlink -f "$0")")
mkdir -p "$O"
R=(); for b in "$@"; do R+=("$b/results"); done
python3 -I $T/parts.py "$O/parts.json" "${R[@]}" > "$O/parts.txt"
python3 -I $T/eventcost.py "${R[@]}" > "$O/events.json"
python3 -I $T/costs24.py "$O/costs.json" "$P" "$N" "$O/parts.json" "$O/events.json" "${R[@]}" > "$O/costs.txt"
python3 -I $T/aecp_kinds.py "$H" "$O/aecp.json" "$@" > "$O/aecp.txt"
cat "$O/costs.txt" "$O/aecp.txt"
