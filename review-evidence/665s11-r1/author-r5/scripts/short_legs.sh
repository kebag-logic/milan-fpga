#!/bin/bash
# The short legs in turn on one range: the answering-ports leg at 1x1/1if (B1F, with aecp-reboot), the 8x8/2if
# REBOOT leg (B8R, reported) and the redelivery control (C-R1). usage: short_legs.sh CLONE
set -u
C=$1 T=<scratch> L=$T/r5/scripts/leg.sh B=$T/r5/legs
rc=0
bash $L $C $B/B1F 1x1 4 --variant answering-ports --groups aecp-fanout,aecp,aecp-largest-notice,aecp-reboot > $B/B1F.log 2>&1 || rc=1
bash $L $C $B/B8R 8x8 4 --variant answering-ports --groups aecp-reboot > $B/B8R.log 2>&1 || rc=1
bash $L $C $B/C-R1 1x1 1 --mutation acmp-redelivered-every-poll > $B/C-R1.log 2>&1 || rc=1
for n in B1F B8R C-R1; do echo "$n $(grep -o 'END rc=[0-9]*' $B/$n.log)"; done
exit $rc
