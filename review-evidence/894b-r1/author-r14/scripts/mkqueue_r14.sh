#!/bin/bash
# Round 14's final-gate queue at a head, for launchM.py (no campaign and no leg, by the round's brief): the quick checks
# (each grader's check and self-test, the flip check at 1x1/1if and 8x8/1if and its self-test, the documents and idiom
# gates, the comment scans and diff checks), the harness self-test with its mutants, every image against d0a2a160's
# (img_all8.py: all eight identical) and the docs workflow's jobs, each job on its own fresh clone (run_wf.py).
# usage: mkqueue_r14.sh HEAD OUT_QUEUE
set -eu
H=$1 Q=$2
T=/data-2/milan/tmp/894b-a781 S=$(dirname "$(readlink -f "$0")") F=/data-2/milan/tmp/894b-a781/fullR14
B=$T/fullR13/qimg-d0a2a1605d7acc691936a61f9afaa0e67f4b46f2.txt
mkdir -p "$F"
cat > "$Q" <<EOF
r14-F-quick bash $T/scripts/clone.sh $F/cQ $H > $F/cQ.clone.log 2>&1 && bash $S/quick_checks_r14.sh $F/cQ $H > $F/quick-checks.txt 2>&1
r14-F-harness bash $T/scripts/clone.sh $F/cH $H > $F/cH.clone.log 2>&1 && cd $F/cH && python3 -B tb/verilator/ctrl_service_budget/run.py --self-test > $F/harness-selftest.txt 2>&1; rc=\$?; echo "harness self-test rc=\$rc; clone after: \$(git -C $F/cH status --porcelain --untracked-files=all | wc -l) changed path(s)" >> $F/harness-selftest.txt; exit \$rc
r14-F-img bash $T/scripts/clone.sh $F/cI $H > $F/cI.clone.log 2>&1 && bash $S/qimg.sh $F/cI $F/qimg > $F/qimg-$H.txt 2>&1; python3 -I $S/img_all8.py $B $F/qimg-$H.txt "images at $H" d0a2a160 > $F/img-identity.txt 2>&1
r14-W-docs-gates-0 mkdir -p $F/wf; /usr/bin/python3 $S/run_wf.py docs.yml $H docs-gates-0 $F/wf > $F/wf/docs-docs-gates-0.driver.log 2>&1
r14-W-docs-gates-1 mkdir -p $F/wf; /usr/bin/python3 $S/run_wf.py docs.yml $H docs-gates-1 $F/wf > $F/wf/docs-docs-gates-1.driver.log 2>&1
r14-W-docs-gates-2 mkdir -p $F/wf; /usr/bin/python3 $S/run_wf.py docs.yml $H docs-gates-2 $F/wf > $F/wf/docs-docs-gates-2.driver.log 2>&1
r14-W-docs-a mkdir -p $F/wf; for j in wire-accountability docs-check-no-git docs-check; do /usr/bin/python3 $S/run_wf.py docs.yml $H \$j $F/wf > $F/wf/docs-\$j.driver.log 2>&1; done
EOF
wc -l "$Q"
