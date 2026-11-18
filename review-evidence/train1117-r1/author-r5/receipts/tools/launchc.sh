#!/bin/bash
# launchc.sh REV: launch.sh with its units named c-*; the formal measurement at REV at the three points the harness holds, 1x1/1if (1x1), 8x8/1if (8x8-1if)
# and 8x8/2if (8x8): arm A in eight parts, the answering-every-port arm in two, the answering-ports arm's held groups
# (record_classes.HELD_IN_ARM_B, aecp-fanout, and at 1x1 aecp-reboot) in two, the valid-destinations arm in three.
set -u
T=<scratch>; REV=$1; M=$T/r4meas/$REV
for P in 1x1 8x8-1if 8x8; do
  C=$T/clones/r4-meas-$REV-$P
  [ -d $C ] || $T/bin/clone.sh $REV $C > /dev/null || exit 2
  AP=aecp,aecp-largest-notice,aecp-fanout; [ $P = 1x1 ] && AP=$AP,aecp-reboot
  mkdir -p $M/$P
  BG_WEIGHT=250 $T/bin/bgunit.sh c-$P-none $T $M/$P/none.log bash $T/r4meas/leg.sh $C $M/$P/none $P none 8
  BG_WEIGHT=250 $T/bin/bgunit.sh c-$P-aep $T $M/$P/aep.log bash $T/r4meas/leg.sh $C $M/$P/aep $P answering-every-port 2
  BG_WEIGHT=250 $T/bin/bgunit.sh c-$P-ap $T $M/$P/ap.log bash $T/r4meas/leg.sh $C $M/$P/ap $P answering-ports 2 $AP
  BG_WEIGHT=250 $T/bin/bgunit.sh c-$P-vd $T $M/$P/vd.log bash $T/r4meas/leg.sh $C $M/$P/vd $P valid-destinations 3
done
