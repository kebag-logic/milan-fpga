#!/bin/bash
# Round 13's final-gate queue at a head, for launchM.py: the quick checks (each harness grader's check and self-test,
# the documents and idiom gates, the comment scans and diff checks), the harness self-test with its mutants, every
# image against 8883d499's, the SRP campaign (the Talker hold-off plants among it) and the docs workflow's jobs, each
# job on its own fresh clone (run_wf.py). usage: mkqueue_r13.sh HEAD OUT_QUEUE
set -eu
H=$1 Q=$2
T=/data-2/milan/tmp/894b-a781 S=$(dirname "$(readlink -f "$0")") F=/data-2/milan/tmp/894b-a781/fullR13
mkdir -p "$F"
cat > "$Q" <<EOF
r13-F-quick bash $T/scripts/clone.sh $F/cQ $H > $F/cQ.clone.log 2>&1 && bash $S/quick_checks_r13.sh $F/cQ $H > $F/quick-checks.txt 2>&1
r13-F-harness bash $T/scripts/clone.sh $F/cH $H > $F/cH.clone.log 2>&1 && cd $F/cH && python3 -B tb/verilator/ctrl_service_budget/run.py --self-test > $F/harness-selftest.txt 2>&1; rc=\$?; echo "harness self-test rc=\$rc; clone after: \$(git -C $F/cH status --porcelain --untracked-files=all | wc -l) changed path(s)" >> $F/harness-selftest.txt; exit \$rc
r13-F-img bash $T/scripts/clone.sh $F/cI $H > $F/cI.clone.log 2>&1 && bash $S/qimg.sh $F/cI $F/qimg > $F/qimg-$H.txt 2>&1; python3 -I $S/img_r13.py $T/fullR12/qimg-8883d499.txt $T/fullR12/qimg $F/qimg-$H.txt $F/qimg $WORKSPACE_HOME/br-milan-rv32/host/bin/riscv32-linux-objdump > $F/img-identity.txt 2>&1
r13-W-fw-srp mkdir -p $F/wf; /usr/bin/python3 $S/run_wf.py rtl-fast.yml $H firmware-srp-mutants $F/wf > $F/wf/rtl-fast-firmware-srp-mutants.driver.log 2>&1
r13-W-docs-gates-0 mkdir -p $F/wf; /usr/bin/python3 $S/run_wf.py docs.yml $H docs-gates-0 $F/wf > $F/wf/docs-docs-gates-0.driver.log 2>&1
r13-W-docs-gates-1 mkdir -p $F/wf; /usr/bin/python3 $S/run_wf.py docs.yml $H docs-gates-1 $F/wf > $F/wf/docs-docs-gates-1.driver.log 2>&1
r13-W-docs-gates-2 mkdir -p $F/wf; /usr/bin/python3 $S/run_wf.py docs.yml $H docs-gates-2 $F/wf > $F/wf/docs-docs-gates-2.driver.log 2>&1
r13-W-docs-a mkdir -p $F/wf; for j in wire-accountability docs-check-no-git docs-check; do /usr/bin/python3 $S/run_wf.py docs.yml $H \$j $F/wf > $F/wf/docs-\$j.driver.log 2>&1; done
EOF
wc -l "$Q"
