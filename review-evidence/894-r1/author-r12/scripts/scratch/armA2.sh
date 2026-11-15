#!/bin/bash
# One part of the full arm A at 1x1/1if (#894 round 11: every group of run.py's arm A, split in two parts of 48 on one
# build, as round 4's M1A and the aecp-check ran): part 1 builds into BUILD and runs its groups into BUILD/results-p1;
# part 2 waits for that build, then reuses it for its groups into BUILD/results-p2. usage: armA.sh PART CLONE BUILD
set -u
P=$1 C=$2 B=$3 T=/data-2/milan/tmp/894-a773
G=$(cat $T/r12/scripts/armA-p$P.groups)
if [ "$P" = 1 ]; then
  exec bash $T/scripts/leg.sh "$C" "$B" 1x1 8 --out "$B/results-p1" --groups "$G"
fi
timeout 3000 bash -c "until [ -s '$B/build.json' ] && [ -e '$B/native/Vsim' ] && grep -q '^COMMAND .*native/Vsim' $T/units/r12-A2-p1.log; do sleep 20; done" || { echo "no build"; exit 3; }
exec bash $T/scripts/leg.sh "$C" "$B" 1x1 8 --reuse-build --out "$B/results-p2" --groups "$G"
