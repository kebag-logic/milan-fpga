#!/bin/bash
# hot.sh: decision 3's main cut, rehearsed on a scratch clone of the step-9 tip (nothing committed): the recorded
# procedure of sw/firmware/ctrl/plat/ctrl_split_hot.txt. The 1x1/1if split image, arm A, groups backlog and
# backlog-adp, built and run as run.py does by default; each run again with its committed PCs traced from 300,000 bus
# cycles before its first record's commit (its first RXC) for 900,000 committed PCs (BUDGET_TRACE_AFTER,
# BUDGET_TRACE_PCS); every function those passes ran, in the order they first ran it (order.py).
set -u
T=<scratch>; . $T/bin/env.sh
export MAKEFLAGS="-j4 --no-print-directory" PYTHONUNBUFFERED=1
REV=${1:-8f6fbb84}; C=$T/attr/clones/hot-trace; H=$T/attr/hot; B=$H/trace-build
[ -d $C ] || $T/bin/clone.sh $REV $C || exit 2
echo "HEAD $(git -C $C rev-parse HEAD) dirty $(git -C $C status --porcelain --untracked-files=no | wc -l) start $(date +%T)"
python3 -B $T/tools/legs.py build $C $B 1x1 none 1 backlog,backlog-adp > $H/trace-build.log 2>&1 || { echo "build failed"; exit 3; }
python3 -B $T/tools/legs.py run $C $B 1x1 none 0 2 > $H/trace-run.log 2>&1; echo "untraced run rc=$? $(date +%T)"
for g in backlog backlog-adp; do
  first=$(grep -m1 '^RXC ' $B/part0/$g.log | awk '{print $2}')
  after=$((first - 300000))
  echo "$g: first RXC at bus cycle $first, traced after $after"
  (cd $B/gateware && BUDGET_TRACE_AFTER=$after BUDGET_TRACE_PCS=900000 $B/native/Vsim $B/part0/$g.txt - | grep '^PC ' > $H/$g.pcs)
  echo "$g: $(wc -l < $H/$g.pcs) PCs traced $(date +%T)"
done
python3 -I $H/order.py $B/image/ctrl_app.map $H/backlog.pcs $H/backlog-adp.pcs > $H/order.txt 2> $H/order.summary
cat $H/order.summary; echo "END $(date +%T)"
