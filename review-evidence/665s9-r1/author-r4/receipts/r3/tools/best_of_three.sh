#!/usr/bin/env bash
# best_of_three.sh: #818's other two placement directives on the split route's synthesis checkpoint, one at a time,
# stopping at the first whose every signoff corner meets WNS >= +0.030 ns and WHS >= 0.
S=<scratch>
for d in ExtraTimingOpt AltSpreadLogic_high; do
  bash $S/tools/route_directive.sh $d
  echo "$d rc=$(cat $S/route/split-$d/route.rc)"
  python3 $S/tools/signoff.py $S/route/split-$d > $S/route/split-$d/signoff.txt 2>&1; s=$?
  cat $S/route/split-$d/signoff.txt
  [ $s -eq 0 ] && break
done
echo done > $S/route/BEST3_DONE
