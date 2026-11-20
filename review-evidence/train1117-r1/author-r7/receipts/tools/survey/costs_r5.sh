#!/bin/bash
# One point's measured costs from its legs, by #665 round 28's tools unchanged (parts.py, eventcost.py, costs24.py,
# aecp_kinds.py; read-only copies, their sha256 in the packet), as #902's costs.sh runs them.
# usage: costs_r5.sh TOOLS OUTDIR POINT N_IF HARNESS_DIR LEG_DIR...
set -eu
X=$1 O=$2 P=$3 N=$4 H=$5; shift 5
mkdir -p "$O"
R=(); for b in "$@"; do R+=("$b/results"); done
python3 -I $X/parts.py "$O/parts.json" "${R[@]}" > "$O/parts.txt"
python3 -I $X/eventcost.py "${R[@]}" > "$O/events.json"
python3 -I $X/costs24.py "$O/costs.json" "$P" "$N" "$O/parts.json" "$O/events.json" "${R[@]}" > "$O/costs.txt"
python3 -I $X/aecp_kinds.py "$H" "$O/aecp.json" "$@" > "$O/aecp.txt"
cat "$O/costs.txt" "$O/aecp.txt"
