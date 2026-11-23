#!/bin/bash
# relearn.sh REV: ctrl_split_hot.txt relearned at REV by its recorded procedure and the third window of #665's ruling
# of 2026-11-17 (issuecomment-6959600243, item 1). The 1x1/1if split image, arm A, built and run as run.py does by
# default, groups backlog, backlog-adp and aecp-largest-notice; each run again with its committed PCs traced from
# 300,000 bus cycles before its first record's commit for 900,000 committed PCs (BUDGET_TRACE_AFTER, BUDGET_TRACE_PCS):
# backlog's and backlog-adp's first RXC, aecp-largest-notice's first RXC after its load's mark (aecp_long.*); every
# function the passes ran, in the order they first ran it, the windows in that order (order.py).
set -u
T=<train-scratch>; . $T/bin/env.sh
export MAKEFLAGS="-j4 --no-print-directory" PYTHONUNBUFFERED=1
REV=$1; C=$T/clones/r5-hot-$REV; H=$T/r5hot/$REV; B=$H/trace-build; mkdir -p $H
[ -d $C ] || $T/bin/clone.sh $REV $C || exit 2
echo "HEAD $(git -C $C rev-parse HEAD) dirty $(git -C $C status --porcelain --untracked-files=no | wc -l) start $(date +%T)"
python3 -B $T/tools/legs.py build $C $B 1x1 none 1 backlog,backlog-adp,aecp-largest-notice > $H/trace-build.log 2>&1 || { echo "build failed"; exit 3; }
python3 -B $T/tools/legs.py run $C $B 1x1 none 0 3 > $H/trace-run.log 2>&1; echo "untraced run rc=$? $(date +%T)"
trace() {  # group first-RXC
  echo "$1: first RXC at bus cycle $2, traced after $(($2 - 300000))"
  (cd $B/gateware && BUDGET_TRACE_AFTER=$(($2 - 300000)) BUDGET_TRACE_PCS=900000 $B/native/Vsim $B/part0/$1.txt - | grep '^PC ' > $H/$1.pcs)
  echo "$1: $(wc -l < $H/$1.pcs) PCs traced $(date +%T)"
}
for g in backlog backlog-adp; do trace $g $(grep -m1 '^RXC ' $B/part0/$g.log | awk '{print $2}') & done
g=aecp-largest-notice; mark=$(grep -m1 '^MARK [0-9]* aecp_long\.' $B/part0/$g.log | awk '{print $2}')
echo "$g: load mark $mark"; trace $g $(awk -v m=$mark '$1=="RXC" && $2>=m {print $2; exit}' $B/part0/$g.log) &
wait
python3 -I $T/attr/hot/order.py $B/image/ctrl_app.map $H/backlog.pcs $H/backlog-adp.pcs $H/aecp-largest-notice.pcs > $H/order.txt 2> $H/order.summary
cat $H/order.summary; echo "END $(date +%T)"
