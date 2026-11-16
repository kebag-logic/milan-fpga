#!/bin/bash
# Round 7: the coverage ratchet of the composed tree, by its tool (fw_coverage.py --write, never by hand), as CI
# reads it (--check without --lwsrp), on the worktree before the merge commit; then --check. usage: cov_write7.sh TREE OUT
set -u
TREE=$1 OUT=$2 T=/data-2/milan/tmp/897-a776
. $T/scripts/env.sh
export TMPDIR=$T/r4/tmp/cov7 MAKEFLAGS="-j8 --no-print-directory"; mkdir -p $TMPDIR $OUT
cd $TREE
cp sw/firmware/gtest/coverage.ratchet $OUT/coverage.ratchet.before
python3 -B sw/firmware/gtest/fw_coverage.py --write --jobs 8 > $OUT/fw_coverage-write.log 2>&1; echo "write rc=$?" > $OUT/summary.txt
python3 -B sw/firmware/gtest/fw_coverage.py --check --jobs 8 > $OUT/fw_coverage-check.log 2>&1; echo "check rc=$?" >> $OUT/summary.txt
diff $OUT/coverage.ratchet.before sw/firmware/gtest/coverage.ratchet > $OUT/coverage.ratchet.diff; echo "diff rc=$?" >> $OUT/summary.txt
