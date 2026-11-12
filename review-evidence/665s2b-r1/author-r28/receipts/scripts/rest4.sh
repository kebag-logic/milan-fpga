#!/bin/bash
# The fourth range's runs: the donor column's 1x1/1if leg beside arm B's aecp group at both points, then the fan-out's
# cost control at 8x8/2if on the head image.
T=<scratch>
bash $T/scripts/fleg.sh $T/L-D1 D1 1x1 4 - $(cat $T/groups-D1.txt) &
( bash $T/scripts/fleg.sh $T/L-GB8 GB8 8x8 1 - aecp --variant answering-ports
  bash $T/scripts/fleg.sh $T/L-GB1 GB1 1x1 1 - aecp --variant answering-ports
  bash $T/scripts/ctl.sh $(git -C $T/L-CTL rev-parse HEAD) notice-fan-out-as-it-was ) &
wait
