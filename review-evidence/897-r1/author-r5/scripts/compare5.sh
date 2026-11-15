#!/bin/bash
# The 1x1/1if stated-table compare over arm A's four parts, the answering-every-port arm and the answering-ports leg,
# each by its leg prefix, against TREE's statements (#894 round 13's compare1.sh, its tools copied into compare/:
# #665 round 28's parts.py, eventcost.py, costs24.py and aecp_kinds.py, #894's aecp_records.py and compare_point.py).
# usage: compare5.sh TREE BUILDS OUT
set -eu
TREE=$1 B=$2 A=$3
D=/data-2/milan/tmp/897-a776/scripts/r4/compare
rm -rf "$A"; mkdir -p "$A/view"
for v in A1:mA1/results-q1 A2:mA1/results-q2 A3:mA1/results-q3 A4:mA1/results-q4 E1:mE1/results B1:mB1/results; do
  n=${v%%:*} r=${v#*:}; d=${r%%/*}
  mkdir -p "$A/view/$n"; ln -sfn "$B/$d/build.json" "$A/view/$n/build.json"; ln -sfn "$B/$r" "$A/view/$n/results"
done
H=$TREE/tb/verilator/ctrl_service_budget
V=(); for n in A1 A2 A3 A4 E1 B1; do V+=("$A/view/$n"); done
R=(); for b in "${V[@]}"; do R+=("$b/results"); done
mkdir -p "$A/costs1"
python3 -I $D/parts.py "$A/costs1/parts.json" "${R[@]}" > "$A/costs1/parts.txt"
python3 -I $D/eventcost.py "${R[@]}" > "$A/costs1/events.json"
python3 -I $D/costs24.py "$A/costs1/costs.json" 1x1/1if 1 "$A/costs1/parts.json" "$A/costs1/events.json" "${R[@]}" > "$A/costs1/costs.txt"
python3 -I $D/aecp_kinds.py "$H" "$A/costs1/aecp.json" "${V[@]}" > "$A/costs1/aecp.txt"
python3 -I /data-2/milan/tmp/897-a776/scripts/r4/eventcost.py $TREE $B/mA1/results-q*/datapath-events.log > $A/datapath-1x1.json
python3 -I $D/aecp_records.py $TREE $A/records-1x1.json "${R[@]}" > $A/records-1x1.txt
python3 -I $D/compare_point.py $TREE $A/costs1/costs.json $A/costs1/aecp.json $A/datapath-1x1.json $A/records-1x1.json 1x1/1if > $A/compare-1x1.txt
echo FINISHED
