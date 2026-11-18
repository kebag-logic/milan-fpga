#!/bin/bash
# hot-rec.sh: the recorded procedure with a third window, arm A's aecp-largest-notice (the largest legal command's
# record), traced the same way from 300,000 bus cycles before its first record's commit (its first RXC after the
# load's mark, aecp_long.*) for 900,000 committed PCs, and appended after the two recorded traces in first-run order. Scratch only:
# a variant of the procedure, for information.
set -u
T=<scratch>; . $T/bin/env.sh
export PYTHONUNBUFFERED=1
C=$T/attr/clones/hot-trace; H=$T/attr/hot; B=$H/trace-build
python3 -B $C/tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir $B --reuse-build --out $B/part1 \
  --groups aecp-largest-notice --record-budget-findings --record-share-findings --jobs 1 > $H/trace-run-rec.log 2>&1
echo "untraced rc=$? $(date +%T)"
g=aecp-largest-notice
mark=$(grep -m1 '^MARK [0-9]* aecp_long\.' $B/part1/$g.log | awk '{print $2}')
first=$(awk -v m=${mark:-0} '$1=="RXC" && $2>=m {print $2; exit}' $B/part1/$g.log)
after=$((first - 300000))
echo "$g: load mark ${mark:-none}, first RXC at bus cycle $first, traced after $after"
(cd $B/gateware && BUDGET_TRACE_AFTER=$after BUDGET_TRACE_PCS=900000 $B/native/Vsim $B/part1/$g.txt - | grep '^PC ' > $H/$g.pcs)
echo "$g: $(wc -l < $H/$g.pcs) PCs traced $(date +%T)"
python3 -I $H/order.py $B/image/ctrl_app.map $H/backlog.pcs $H/backlog-adp.pcs $H/$g.pcs > $H/order-rec.txt 2> $H/order-rec.summary
cat $H/order-rec.summary
[ -d $T/attr/clones/hot-rec ] || $T/bin/clone.sh 4a5bfb32 $T/attr/clones/hot-rec > /dev/null
python3 -I $H/apply.py $T/attr/clones/hot-rec $H/order-rec.txt $H/backlog.pcs $H/backlog-adp.pcs $H/$g.pcs
(cd $T/attr/clones/hot-rec && python3 sw/firmware/ctrl/test/ctrl_hot.py --check --map $B/image/ctrl_app.map)
echo "END $(date +%T)"
