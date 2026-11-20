#!/bin/bash
# launch6.sh REV POINT: the full CPU budget measurement of the train at REV at one point, on CPUs 0-63 (cpu_ranges.py's
# four free 16-blocks; the session pool 64-95 is left to the gates): every arm the harness holds (arm A and each of
# build.py's VARIANTS), every group of each, each arm's parts on CPUs of its own (leg.sh: legs.py build, then its parts
# at once, one group a part at a time, with the formal measurement's options).
set -u
T=<scratch>; REV=$1; P=$2; M=$T/r6meas/$REV
C=$T/clones/r6-meas-$REV-$P
[ -d $C ] || $T/bin/clone.sh $REV $C > $M.clone-$P.log 2>&1 || exit 2
mkdir -p $M/$P
# arm:parts:first CPU, 64 CPUs in all
for spec in none:22:0 answering-ports:22:22 answering-every-port:6:44 valid-destinations:3:50 answering-later:3:53 \
            shutdown-entry:2:56 talker-notices:2:58 declaring-outputs:4:60; do
  IFS=: read -r V N F <<< "$spec"
  mem=12G; [ $N -ge 20 ] && mem=30G
  BG_WEIGHT=300 BG_MEM=$mem BG_CPUS=$F-$((F + N - 1)) $T/bin/bgunit.sh m6-$P-$V $T $M/$P/$V.log \
    bash $T/r4meas/leg.sh $C $M/$P/$V $P $V $N > /dev/null 2>&1
done
