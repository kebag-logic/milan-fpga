#!/bin/bash
# One quarter of the full arm A at 1x1/1if (#894 round 13: every group of run.py's arm A in four parts of 24 on one
# build): part 1 builds into BUILD and runs its groups into BUILD/results-q1; the others wait for that build, then
# reuse it for their groups into BUILD/results-qN. usage: armA.sh PART CLONE BUILD
set -u
P=$1 C=$2 B=$3 T=/data-2/milan/tmp/894-a773
G=$(cat $T/r13/scripts/armA-q$P.groups)
if [ "$P" = 1 ]; then
  exec bash $T/scripts/leg.sh "$C" "$B" 1x1 8 --out "$B/results-q1" --groups "$G"
fi
timeout 3000 bash -c "until [ -s '$B/build.json' ] && [ -e '$B/native/Vsim' ] && grep -q '^COMMAND .*native/Vsim' $T/units/r13-A-q1.log; do sleep 20; done" || { echo "no build"; exit 3; }
exec bash $T/scripts/leg.sh "$C" "$B" 1x1 8 --reuse-build --out "$B/results-q$P" --groups "$G"
