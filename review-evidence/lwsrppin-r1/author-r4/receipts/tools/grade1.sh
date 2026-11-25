#!/bin/bash
# grade1.sh NAME: grade one finished harness run as round 1 did, plus the train's kept_grade on arm A.
source /data-2/milan/tmp/lwsrppin-a834/r4/bin/penv.sh
n=$1; H=/data-2/milan/tmp/lwsrppin-a834/r4/harness; G=/data-2/milan/tmp/lwsrppin-a834/r4/grade; B=/data-2/milan/tmp/lwsrppin-a834/r4/bin
L=/data-2/milan/tmp/lwsrppin-a834/r3/ledger/b-head; CSB=/data-2/milan/lanes/lwsrp-pin/tb/verilator/ctrl_service_budget
case $n in 1x1*) elf=$L/endstation_ax7101_1x1_tdm8/split-soc/mapped/image/ctrl_app.elf;; *) elf=$L/endstation_ax7101_8x8/split-soc/mapped/image/ctrl_app.elf;; esac
{
  echo "run $n: rc $(cat $H/rc-$n), head $(cat $H/head-$n), $(cat $H/start-$n) -> $(cat $H/end-$n)"
  python3 -I $B/identity.py $H/b-$n $elf
  python3 -I $B/harness_grade.py $H/run-$n.log $H/b-$n/results
  python3 -I $B/share_census.py $H/b-$n/results
  echo "run.py's closing verdict lines (REFUSED/BUDGET/SHARE/OWED/STATED/RESULT and the summary):"
  grep -E '^(REFUSED|BUDGET|SHARE|OWED|STATED|RESULT|FAIL)|groups graded|over the per-pass share' $H/run-$n.log | cut -c1-400
} > $G/grade-$n.txt 2>&1
case $n in 1x1|8x8-1if)
  (cd $CSB && python3 -I kept_grade.py $H/b-$n; echo "kept_grade rc=$?") > $G/kept-$n.txt 2>&1;;
esac
if [ $n = 8x8-1if ]; then
  (cd $CSB && python3 -I egress_ledger.py --point 8x8-1if $H/b-$n/results; echo "egress_ledger rc=$?") > $G/egress-ledger-8x8-1if.log 2>&1
  python3 -I $B/la_window.py $H/b-$n/results/save*.log $H/b-$n/results/srp-kept.log $H/b-$n/results/srp-bound.log > $G/la-window-8x8-1if.txt 2>&1
fi
if [ $n = 1x1 ]; then
  python3 -I $B/la_window.py $H/b-$n/results/save*.log $H/b-$n/results/srp-kept.log $H/b-$n/results/srp-bound.log > $G/la-window-1x1.txt 2>&1
fi
echo graded $n
