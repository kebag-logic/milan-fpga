#!/bin/bash
# The 1x1/1if stated-table compare over arm A's two parts, the answering-every-port arm and the answering-ports leg of
# a builds directory, each by its leg prefix, against TREE's statements (round 4's costs.sh, round 20's eventcost.py,
# round 12's point-aware aecp_records.py, round 11's compare_point.py). usage: compare1.sh TREE BUILDS OUT
set -eu
T=/data-2/milan/tmp/894-a773
TREE=$1 B=$2 A=$3
S=$MANAGEMENT/2026-09-23/894-a773/round12/scripts
CP=$MANAGEMENT/2026-09-23/894-a773/round11/scripts/compare_point.py
rm -rf "$A"; mkdir -p "$A/view"
for v in A1:A/results-q1 A2:A/results-q2 A3:A/results-q3 A4:A/results-q4 E1:E1/results B1F:H-B1F/results; do
  n=${v%%:*} r=${v#*:}; d=${r%%/*}
  mkdir -p "$A/view/$n"; ln -sfn "$B/$d/build.json" "$A/view/$n/build.json"; ln -sfn "$B/$r" "$A/view/$n/results"
done
bash $T/scripts/costs.sh $A/costs1 1x1/1if 1 $TREE/tb/verilator/ctrl_service_budget $A/view/A1 $A/view/A2 $A/view/A3 $A/view/A4 $A/view/E1 $A/view/B1F > $A/costs1.out
python3 -I $T/scripts/eventcost.py $TREE $B/A/results-q*/datapath-events.log > $A/datapath-1x1.json
python3 -I $S/aecp_records.py $TREE $A/records-1x1.json $A/view/A1/results $A/view/A2/results $A/view/A3/results $A/view/A4/results $A/view/E1/results $A/view/B1F/results > $A/records-1x1.txt
python3 -I $CP $TREE $A/costs1/costs.json $A/costs1/aecp.json $A/datapath-1x1.json $A/records-1x1.json 1x1/1if > $A/compare-1x1.txt
echo FINISHED
