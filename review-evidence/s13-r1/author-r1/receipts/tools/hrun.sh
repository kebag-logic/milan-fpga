#!/bin/bash
# hrun.sh CLONE MEAS POINT WORKERS: every part of every arm at POINT (MEAS/<point>/<arm>/parts.json, written by
# hbuild.sh), WORKERS at once, the largest arms first, each `legs.py run ... <part> 1` (the formal measurement's
# options, run.py --reuse-build); each part's log and rc beside its arm.
set -u
S=<scratch>; . $S/bin/fwenv.sh
export MAKEFLAGS="-j2 --no-print-directory" PYTHONUNBUFFERED=1
C=$1 M=$2 P=$3 W=$4
list=$M/$P/parts.list; : > $list
for V in none answering-ports answering-every-port valid-destinations talker-notices answering-later declaring-outputs shutdown-entry; do
  n=$(python3 -c "import json;print(len(json.load(open('$M/$P/$V/parts.json'))['parts']))")
  for k in $(seq 0 $((n-1))); do echo "$V $k" >> $list; done
done
echo "$(wc -l < $list) parts, $W workers, start $(date +%T)"
xargs -P "$W" -L 1 bash -c 'V=$0 K=$1; python3 -B '"$S"'/tools/legs.py run '"$C $M/$P"'/$V '"$P"' $V $K 1 > '"$M/$P"'/$V.part$K.log 2>&1; echo $? > '"$M/$P"'/$V.part$K.rc; echo "$V part$K rc=$(cat '"$M/$P"'/$V.part$K.rc) $(date +%T)"' < $list
echo "END $(date +%T)"
