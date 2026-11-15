#!/bin/bash
# The 1x1/1if stated-table compare over arm A's two halves, the answering-every-port arm and the answering-ports leg of
# a builds directory, each by its leg prefix, against TREE's statements, by #894's tools unchanged (round 28's parts.py,
# eventcost.py, costs24.py and aecp_kinds.py; round 20's datapath eventcost.py; round 12's aecp_records.py; round 11's
# compare_point.py, copied into scripts/tools902). usage: compare1.sh TREE BUILDS OUT
set -eu
TREE=$1 B=$2 A=$3
K=<scratch>/r5/scripts/tools902
mkdir -p "$A/view" "$A/costs1"
for v in A1:A/results-h1 A2:A/results-h2 E1:E1/results B1F:B1F/results; do
  n=${v%%:*} r=${v#*:}; d=${r%%/*}
  mkdir -p "$A/view/$n"; ln -sfn "$B/$d/build.json" "$A/view/$n/build.json"; ln -sfn "$B/$r" "$A/view/$n/results"
done
V=(); for n in A1 A2 E1 B1F; do V+=("$A/view/$n"); done
R=(); for n in A1 A2 E1 B1F; do R+=("$A/view/$n/results"); done
H=$TREE/tb/verilator/ctrl_service_budget
python3 -I $K/tools-r28/parts.py "$A/costs1/parts.json" "${R[@]}" > "$A/costs1/parts.txt"
python3 -I $K/tools-r28/eventcost.py "${R[@]}" > "$A/costs1/events.json"
python3 -I $K/tools-r28/costs24.py "$A/costs1/costs.json" 1x1/1if 1 "$A/costs1/parts.json" "$A/costs1/events.json" "${R[@]}" > "$A/costs1/costs.txt"
python3 -I $K/tools-r28/aecp_kinds.py "$H" "$A/costs1/aecp.json" "${V[@]}" > "$A/costs1/aecp.txt"
cat "$A/costs1/costs.txt" "$A/costs1/aecp.txt" > "$A/costs1.out"
python3 -I $K/eventcost_datapath.py $TREE $B/A/results-h*/datapath-events.log > $A/datapath-1x1.json
python3 -I $K/aecp_records.py $TREE $A/records-1x1.json "${R[@]}" > $A/records-1x1.txt
python3 -I $K/compare_point.py $TREE $A/costs1/costs.json $A/costs1/aecp.json $A/datapath-1x1.json $A/records-1x1.json 1x1/1if > $A/compare-1x1.txt
echo FINISHED
