#!/bin/bash
# mapbuild.sh REV: the harness's image in each of its six arms at its three points, built as run.py builds by default,
# for the link maps the hot-list filter reads (which sections each served image links). Into r5hot/maps/REV.
set -u
T=<scratch>; . $T/bin/env.sh
export MAKEFLAGS="-j4 --no-print-directory" PYTHONUNBUFFERED=1
REV=$1; C=$T/clones/r5-map-$REV; M=$T/r5hot/maps/$REV; mkdir -p $M
[ -d $C ] || $T/bin/clone.sh $REV $C > /dev/null || exit 2
for P in 1x1 8x8-1if 8x8; do for V in none answering-ports shutdown-entry answering-later answering-every-port valid-destinations; do
  ( python3 -B $T/tools/legs.py build $C $M/$P-$V $P $V 1 > $M/$P-$V.log 2>&1; echo "$P $V rc=$? $(ls $M/$P-$V/image/ctrl_app.map 2>/dev/null | wc -l) map" ) &
done; wait; done
echo "END $(date +%T)"
