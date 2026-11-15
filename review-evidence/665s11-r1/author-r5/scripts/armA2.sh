#!/bin/bash
# One half of the full arm A at 1x1/1if (every group of run.py's arm A, in two interleaved halves of 48 on one build):
# half 1 builds into BUILD and runs its groups into BUILD/results-h1; half 2, launched once that build exists, reuses
# it. usage: armA2.sh HALF CLONE BUILD [HALF1_UNIT_LOG]
set -u
H=$1 C=$2 B=$3 W=${4:-}
T=<scratch>
G=$(cat $T/r5/scripts/armA-h$H.groups)
if [ "$H" = 1 ]; then
  exec bash $T/r5/scripts/leg.sh "$C" "$B" 1x1 8 --out "$B/results-h1" --groups "$G"
fi
if [ ! -s "$B/build.json" ] || [ ! -e "$B/native/Vsim" ] || ! grep -q '^COMMAND .*native/Vsim' "$W"; then
  echo "no build yet in $B"; exit 3
fi
exec bash $T/r5/scripts/leg.sh "$C" "$B" 1x1 8 --reuse-build --out "$B/results-h2" --groups "$G"
