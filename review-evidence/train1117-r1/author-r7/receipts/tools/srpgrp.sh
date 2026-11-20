#!/bin/bash
# srpgrp.sh REV: the valid-destinations arm's srp-talker-held alone at 8x8/1if at REV, built and run as the legs are.
set -u
T=<scratch>; . $T/bin/env.sh
export MAKEFLAGS="-j4 --no-print-directory" PYTHONUNBUFFERED=1
REV=$1; C=$T/clones/r4-fan-$REV; B=$T/r4meas/srp/$REV
[ -d $C ] || $T/bin/clone.sh $REV $C > /dev/null || exit 2
mkdir -p $B; echo "HEAD $(git -C $C rev-parse --short=8 HEAD) start $(date +%T)"
python3 -B $T/tools/legs.py build $C $B 8x8-1if valid-destinations 1 srp-talker-held > $B.build.log 2>&1 || { echo "build rc=$?"; exit 3; }
python3 -B $T/tools/legs.py run $C $B 8x8-1if valid-destinations 0 1 > $B.part0.log 2>&1; echo "run rc=$? $(date +%T)"
grep '^STATED' $B.part0.log
