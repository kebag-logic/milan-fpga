#!/usr/bin/env bash
# the notify proofs: default shape and the shipping 1x1 stream shape
cd <data>/tmp/pp181-a635/equiv
E=$PWD/src; H=<data>/lanes/pp181-cut/hdl/aecp/KL_aecp_notify.sv
W="wire cmdq_nempty_r = (cmdq_count_r != 5'd0);"
run() { local n=$1; shift; local t0=$SECONDS rc=0
  timeout 10800 ./equiv.sh "$n" "$E/base_KL_aecp_notify.sv" "$H" KL_aecp_notify 2 "$W" "$@" > "$n.out" 2>&1 || rc=$?
  echo "$n rc=$rc ($((SECONDS - t0))s)" >> notify_rc.txt; }
export EQUIV_MEM2REG=1
run notify-default &
run notify-1x1 -- -set N_STREAM_IN_P 1 -set N_STREAM_OUT_P 1 &
wait
echo DONE >> notify_rc.txt
