#!/bin/bash
# One half of the full arm A at 1x1/1if (every group of run.py's arm A, in two interleaved halves of 48 on one build):
# half 1 builds into BUILD and runs its groups into BUILD/results-h1; half 2 waits for that build, then reuses it.
# usage: armA.sh HALF CLONE BUILD
set -u
H=$1 C=$2 B=$3 T=<scratch>
G=$(cat $T/r5/scripts/armA-h$H.groups)
if [ "$H" = 1 ]; then
  exec bash $T/r5/scripts/leg.sh "$C" "$B" 1x1 8 --out "$B/results-h1" --groups "$G"
fi
timeout 5400 bash -c "until [ -s '$B/build.json' ] && [ -e '$B/native/Vsim' ] && grep -q '^COMMAND .*native/Vsim' $T/r5/units/A1.log; do sleep 20; done" || { echo "no build"; exit 3; }
exec bash $T/r5/scripts/leg.sh "$C" "$B" 1x1 8 --reuse-build --out "$B/results-h2" --groups "$G"
