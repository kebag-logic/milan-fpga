#!/bin/bash
# Round 10's measurement on a clean clone of a head (#930: both points' images change): at 1x1/1if and at 8x8/1if,
# arm A in four parts balanced by simulated time, the answering-every-port arm, the answering-ports arm's aecp,
# aecp-fanout and aecp-largest-notice, the valid-destinations arm (srp-talker, srp-talker-loss, srp-talker-held);
# at 8x8/1if the transmit-aged control as well. Each leg its own unit (launchM.py), the longest first.
# usage: mkqueueM10.sh CLONE > queue.txt
set -u
C=$1 T=/data-2/milan/tmp/894b-a781 S=$MANAGEMENT/2026-09-23/894b-a781/round10/scripts
for p in 8x8-1if 1x1; do
    tag=$([ $p = 1x1 ] && echo 1 || echo 8)
    for k in 0 1 2 3; do echo "r10-M$tag-A$k python3 -B $S/legB.py $C $T/builds/R10-M$tag-A$k $p none $k 4 8"; done
done
for p in 8x8-1if 1x1; do
    tag=$([ $p = 1x1 ] && echo 1 || echo 8)
    echo "r10-M$tag-AE python3 -B $S/legB.py $C $T/builds/R10-M$tag-AE $p answering-every-port 0 1 8"
    echo "r10-M$tag-VD python3 -B $S/legB.py $C $T/builds/R10-M$tag-VD $p valid-destinations 0 1 8"
    echo "r10-M$tag-B python3 -B $S/legB.py $C $T/builds/R10-M$tag-B $p answering-ports 0 1 8 aecp,aecp-fanout,aecp-largest-notice"
done
echo "r10-M8-CTA bash $S/leg.sh $C $T/builds/R10-M8-CTA 8x8-1if 8 --variant answering-later --mutation transmit-aged"
