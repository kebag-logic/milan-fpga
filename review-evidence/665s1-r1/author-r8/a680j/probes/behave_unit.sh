#!/bin/bash
# cd tests && behave, from a checkout, into a log with the head, elapsed and rc last.  usage: behave_unit.sh CHECKOUT LOG
set -u
export TMPDIR=$VALIDATION_STORAGE/scratch/665s1-a680j-work/tmp
cd "$1/tests" || exit 2
start=$(date +%s)
echo "HEAD $(git rev-parse HEAD) DIRTY $(git status --porcelain --untracked-files=no | wc -l)" > "$2"
behave --no-capture -f plain >> "$2" 2>&1
rc=$?
echo "elapsed=$(( $(date +%s) - start ))s" >> "$2"
echo "rc=$rc" >> "$2"
