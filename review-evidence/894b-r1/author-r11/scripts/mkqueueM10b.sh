#!/bin/bash
# Round 10's measurement in shorter legs (mkqueueM10.sh's, split after two host stops cut its first legs): at 1x1/1if
# and 8x8/1if, arm A in eight parts balanced by simulated time, the answering-every-port arm in two, each
# valid-destinations group its own leg (srp-talker-held first, at both points), the answering-ports arm's aecp,
# aecp-fanout and aecp-largest-notice; at 8x8/1if the transmit-aged control as well. Each leg its own unit
# (launchM.py). usage: mkqueueM10b.sh CLONE > queue.txt
set -u
C=$1 T=/data-2/milan/tmp/894b-a781 S=$MANAGEMENT/2026-09-23/894b-a781/round10/scripts
tag() { [ $1 = 1x1 ] && echo 1 || echo 8; }
for p in 8x8-1if 1x1; do t=$(tag $p); echo "r10-M$t-VDh python3 -B $S/legB.py $C $T/builds/R10-M$t-VDh $p valid-destinations 0 1 8 srp-talker-held"; done
for p in 8x8-1if 1x1; do t=$(tag $p); for k in 0 1 2 3 4 5 6 7; do echo "r10-M$t-A$k python3 -B $S/legB.py $C $T/builds/R10-M$t-A$k $p none $k 8 8"; done; done
for p in 8x8-1if 1x1; do t=$(tag $p)
    for k in 0 1; do echo "r10-M$t-AE$k python3 -B $S/legB.py $C $T/builds/R10-M$t-AE$k $p answering-every-port $k 2 8"; done
    for g in srp-talker srp-talker-loss; do echo "r10-M$t-VD$([ $g = srp-talker ] && echo t || echo l) python3 -B $S/legB.py $C $T/builds/R10-M$t-VD$([ $g = srp-talker ] && echo t || echo l) $p valid-destinations 0 1 8 $g"; done
    echo "r10-M$t-B python3 -B $S/legB.py $C $T/builds/R10-M$t-B $p answering-ports 0 1 8 aecp,aecp-fanout,aecp-largest-notice"
done
echo "r10-M8-CTA bash $S/leg.sh $C $T/builds/R10-M8-CTA 8x8-1if 8 --variant answering-later --mutation transmit-aged"
