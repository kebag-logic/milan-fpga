#!/bin/bash
# cb2.sh: ctrl_boundary.py --require-rv32 --selftest at the merge head (the route's head worktree, same commit),
# with MAKEFLAGS="-j8 --no-print-directory" as the other lanes' boundary runs set it.
source /data-2/milan/tmp/lwsrppin-a834/penv.sh
export MAKEFLAGS="-j8 --no-print-directory"
o=/data-2/milan/tmp/lwsrppin-a834/r3; C=/data-2/milan/tmp/lwsrppin-r2; cd $C || exit 9
echo "HEAD $(git rev-parse HEAD) porcelain $(git status --porcelain --untracked-files=no | wc -l) start $(date -Iseconds)" > $o/cb2.log
python3 -B sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest >> $o/cb2.log 2>&1; rc=$?
echo "porcelain-after $(git status --porcelain --untracked-files=no | wc -l) END rc=$rc $(date -Iseconds)" >> $o/cb2.log
echo $rc > $o/cb2.rc
