#!/bin/bash
# After the fresh 8x8 legs at 6c284a97: GA8's runs merged and regraded there (head33.sh, merge mode, at the legs' head,
# which writes results.json), every round of the fresh 8x8 legs tallied by n and k (trigger 2's rounds), and the 8x8
# measured costs (costs.sh) from views named as the legs.
set -u
T=/data-2/milan/tmp/665s2b-a683zo F=6c284a975f4932affb02ca81aeef2d5cd3bd7a9f
. $T/scripts/env.sh
bash $T/scripts/head33.sh $F merge $T/L33-GA8 F-GA8 8x8
echo "merge-regrade rc=$(cat $T/logs/head-F-GA8.log.rc)"
python3 -I $T/tools/tally_rounds.py $T/L33-GA8/tb/verilator/ctrl_service_budget $T/tally/F-rounds-8x8.json F-GA8:8x8 F-GN8:8x8 F-GB8:8x8 > $T/tally/F-rounds-8x8.txt 2>&1
echo "tally rc=$?"
mkdir -p $T/views/GA8 $T/views/GN8
for n in GA8 GN8; do for f in build.json image split-soc; do ln -sfn $T/builds/F-$n/$f $T/views/$n/$f; done; done
ln -sfn $T/builds/F-GA8/results-merged $T/views/GA8/results
ln -sfn $T/builds/F-GN8/results $T/views/GN8/results
bash $T/scripts/costs.sh $T/costs33/G8 8x8/2if 2 $T/L33-GA8/tb/verilator/ctrl_service_budget $T/views/GA8 $T/views/GN8 > $T/costs33/G8.log 2>&1
echo "costs rc=$?"
