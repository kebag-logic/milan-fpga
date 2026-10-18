#!/usr/bin/env bash
# the check as recorded: 1-inductive invariant after a reset cycle (-maxsteps 1);
# the unmutated control at 1x1, then each planted mutant at 1x1 (must fail)
cd <data>/tmp/pp181-a635/equiv
H=<data>/lanes/pp181-cut/hdl/aecp/KL_aecp_notify.sv
run() { local n=$1; shift; local t0=$SECONDS rc=0
  timeout 3600 ./inv.sh "$n" "$@" > "inv-$n.out" 2>&1 || rc=$?
  echo "$n rc=$rc ($((SECONDS - t0))s)" >> inv2_rc.txt; }
S="-set N_STREAM_IN_P 1 -set N_STREAM_OUT_P 1"
run k1-head-1x1 "$H" $S &
for m in N1-pop-keeps-occupied N2-push-not-seen N3-pop-off-by-one; do
  run "k1-m-$m" "$PWD/mutants/$m.sv" $S &
done
wait
echo DONE >> inv2_rc.txt
