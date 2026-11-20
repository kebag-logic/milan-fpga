#!/bin/bash
# leg.sh CLONE BUILD POINT VARIANT NPARTS [GROUPS]: one arm of the formal measurement at a point: its build (legs.py
# build, as run.py builds by default) and then its NPARTS parts at once, one group a part at a time (legs.py run).
set -u
T=<scratch>; . $T/bin/env.sh
export MAKEFLAGS="-j4 --no-print-directory" PYTHONUNBUFFERED=1
C=$1 B=$2 P=$3 V=$4 N=$5 G=${6:-}
mkdir -p $B
echo "HEAD $(git -C $C rev-parse HEAD) dirty $(git -C $C status --porcelain --untracked-files=no | wc -l) $P $V $N parts start $(date +%T)"
python3 -B $T/tools/legs.py build $C $B $P $V $N $G > $B.build.log 2>&1 || { echo "build rc=$?"; exit 3; }
tail -1 $B.build.log
for k in $(seq 0 $((N - 1))); do
  ( python3 -B $T/tools/legs.py run $C $B $P $V $k 1 > $B.part$k.log 2>&1; echo $? > $B.part$k.rc; echo "part $k rc=$(cat $B.part$k.rc) $(date +%T)" ) &
done
wait; echo "END $(date +%T)"
