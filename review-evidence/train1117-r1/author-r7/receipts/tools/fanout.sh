#!/bin/bash
# fanout.sh REV: the answering-ports arm's aecp-fanout group alone at 8x8/2if at REV (a clone of the lane), built and run
# as the formal measurement's legs are, into r4meas/fanout/REV.
set -u
T=<scratch>; . $T/bin/env.sh
export MAKEFLAGS="-j4 --no-print-directory" PYTHONUNBUFFERED=1
REV=$1; C=$T/clones/r4-fan-$REV; B=$T/r4meas/fanout/$REV
[ -d $C ] || $T/bin/clone.sh $REV $C > /dev/null || exit 2
mkdir -p $B; echo "HEAD $(git -C $C rev-parse --short=8 HEAD) start $(date +%T)"
python3 -B $T/tools/legs.py build $C $B 8x8 answering-ports 1 aecp-fanout > $B.build.log 2>&1 || { echo "build rc=$?"; tail -3 $B.build.log; exit 3; }
python3 -B $T/tools/legs.py run $C $B 8x8 answering-ports 0 1 > $B.part0.log 2>&1; echo "run rc=$? $(date +%T)"
grep -c '^STATED' $B.part0.log; grep '^STATED' $B.part0.log | sort -t' ' -k6 | tail -2
