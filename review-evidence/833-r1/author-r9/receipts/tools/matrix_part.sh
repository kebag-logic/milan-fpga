#!/usr/bin/env bash
# One part of the --matrix campaign at the head snapshot: every named mutant on every control and the whole test.
# usage: matrix_part.sh <part number> [jobs]
set -u
S=$VALIDATION_STORAGE/833-a726i; out=$MANAGEMENT/2026-09-23/833-a726i/receipts/final; n=$1; jobs=${2:-10}
export TMPDIR=$S/tmp PYTHONDONTWRITEBYTECODE=1
cd $S/wt-head || exit 2
grep SigIgn /proc/self/status > $out/matrix-part$n.sigign
cat /proc/loadavg > $out/matrix-part$n.load
python3 -B scripts/test_suite_cancellation.py --mutants $(cat $S/tmp/matrix-part$n.names) --matrix --jobs $jobs > $out/matrix-part$n.log 2>&1
rc=$?; echo $rc > $out/matrix-part$n.rc
cat /proc/loadavg >> $out/matrix-part$n.load
echo "part $n rc $rc: $(grep -A5 '^owned-process mutants' $out/matrix-part$n.log | tr '\n' ' ')"
