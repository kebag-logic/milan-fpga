#!/bin/bash
# launchv.sh: launch.sh's measurement at the scratch variant r4var/src's HEAD (the tip febbfc4b, its hot list less the
# two entries the 8x8/2if fixture compiles out; not committed to the lane), into r4meas/var.
set -u
T=<scratch>; M=$T/r4meas/var; V=$(git -C $T/r4var/src rev-parse HEAD)
for P in 1x1 8x8-1if 8x8; do
  C=$T/clones/r4-var-$P
  if [ ! -d $C ]; then
    $T/bin/clone.sh febbfc4b $C > /dev/null || exit 2
    git -C $C fetch -q $T/r4var/src HEAD && git -C $C -c advice.detachedHead=false checkout -q $V || exit 2
  fi
  AP=aecp,aecp-largest-notice,aecp-fanout; [ $P = 1x1 ] && AP=$AP,aecp-reboot
  mkdir -p $M/$P
  BG_WEIGHT=250 $T/bin/bgunit.sh v-$P-none $T $M/$P/none.log bash $T/r4meas/leg.sh $C $M/$P/none $P none 8
  BG_WEIGHT=250 $T/bin/bgunit.sh v-$P-aep $T $M/$P/aep.log bash $T/r4meas/leg.sh $C $M/$P/aep $P answering-every-port 2
  BG_WEIGHT=250 $T/bin/bgunit.sh v-$P-ap $T $M/$P/ap.log bash $T/r4meas/leg.sh $C $M/$P/ap $P answering-ports 2 $AP
  BG_WEIGHT=250 $T/bin/bgunit.sh v-$P-vd $T $M/$P/vd.log bash $T/r4meas/leg.sh $C $M/$P/vd $P valid-destinations 3
done
