#!/bin/bash
# After both parts of the full arm A and the answering-every-port arm at 1x1/1if: merge arm A's group logs and scripts
# (hard links) into results-merged, then round 4's costs.sh over a view of arm A, the every-port arm (E1) and the
# answering-ports leg (B1F), each by its leg prefix, the datapath eventcost.py over arm A's datapath-events,
# aecp_records.py over the three, and round 11's compare_point.py against TREE's statements at 1x1/1if; and the same
# over the 8x8 legs at 8x8/2if (#894 issuecomment-6881287231; R837-6-F1). usage: finish.sh TREE OUT
set -eu
T=/data-2/milan/tmp/894-a773
TREE=$1 A=$2
B=$T/r12/gates-out/builds
M=$B/A/results-merged
CP=$MANAGEMENT/2026-09-23/894-a773/round11/scripts/compare_point.py
mkdir -p "$A"
if [ ! -e "$M" ]; then
  mkdir -p "$M"
  for p in p1 p2; do for f in "$B/A/results-$p"/*.log "$B/A/results-$p"/*.txt; do ln "$f" "$M/$(basename "$f")"; done; done
fi
echo "MERGED logs $(ls "$M"/*.log | wc -l) scripts $(ls "$M"/*.txt | wc -l)"
rm -rf "$A/view" "$A/costs1" "$A/costs8"; mkdir -p "$A/view"
for v in A:A/results-merged E1:E1/results B1F:H-B1F/results L8A:H-L8A/results L8N:H-L8N/results L8L:H-L8L/results \
         L8O:H-L8O/results B8F:H-B8F/results J8:H-J8/results; do
  n=${v%%:*} r=${v#*:}; d=${r%%/*}
  mkdir -p "$A/view/$n"; ln -sfn "$B/$d/build.json" "$A/view/$n/build.json"; ln -sfn "$B/$r" "$A/view/$n/results"
done
H=$TREE/tb/verilator/ctrl_service_budget
bash $T/scripts/costs.sh $A/costs1 1x1/1if 1 $H $A/view/A $A/view/E1 $A/view/B1F > $A/costs1.out
python3 -I $T/scripts/eventcost.py $TREE "$M/datapath-events.log" > $A/datapath-1x1.json
python3 -I $MANAGEMENT/2026-09-23/894-a773/round12/scripts/aecp_records.py $TREE $A/records-1x1.json $A/view/A/results $A/view/E1/results \
  $A/view/B1F/results > $A/records-1x1.txt
python3 -I $CP $TREE $A/costs1/costs.json $A/costs1/aecp.json $A/datapath-1x1.json $A/records-1x1.json 1x1/1if \
  > $A/compare-1x1.txt
bash $T/scripts/costs.sh $A/costs8 8x8/2if 2 $H $A/view/L8A $A/view/L8N $A/view/L8L $A/view/L8O $A/view/B8F \
  $A/view/J8 > $A/costs8.out
python3 -I $T/scripts/eventcost.py $TREE "$B/H-L8A/results/datapath-events.log" > $A/datapath-8x8.json
AECP_RECORDS_POINT=8x8/2if python3 -I $MANAGEMENT/2026-09-23/894-a773/round12/scripts/aecp_records.py $TREE $A/records-8x8.json $A/view/L8A/results $A/view/L8N/results \
  $A/view/L8L/results $A/view/L8O/results $A/view/B8F/results $A/view/J8/results > $A/records-8x8.txt
python3 -I $CP $TREE $A/costs8/costs.json $A/costs8/aecp.json $A/datapath-8x8.json $A/records-8x8.json 8x8/2if \
  > $A/compare-8x8.txt
tail -n 30 $A/compare-1x1.txt; tail -n 20 $A/compare-8x8.txt
echo FINISHED
