#!/usr/bin/env bash
# invariant proofs: head at three shapes, then each planted mutant at 1x1 (must fail)
cd <data>/tmp/pp181-a635/equiv
H=<data>/lanes/pp181-cut/hdl/aecp/KL_aecp_notify.sv
run() { local n=$1; shift; local t0=$SECONDS rc=0
  timeout 3600 ./inv.sh "$n" "$@" > "inv-$n.out" 2>&1 || rc=$?
  echo "$n rc=$rc ($((SECONDS - t0))s)" >> inv_rc.txt; }
run head-default "$H" &
run head-2if-ident "$H" -set N_IF_P 2 -set EN_IDENTIFY_NOTIF_P 1 &
for m in N1-pop-keeps-occupied N2-push-not-seen N3-pop-off-by-one; do
  run "m-$m" "$PWD/mutants/$m.sv" -set N_STREAM_IN_P 1 -set N_STREAM_OUT_P 1 &
done
wait
echo DONE >> inv_rc.txt
