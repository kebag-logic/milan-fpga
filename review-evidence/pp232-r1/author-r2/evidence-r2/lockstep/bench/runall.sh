#!/usr/bin/env bash
# builds the five shapes, then runs 8 seeds each (1-4 protocol-shaped, 5-8 fully random), 1,000,000 cycles
set -u
H=$SCRATCH/r1b/lockstep; cd $H
C=$H/cand-6e950fea.sv
b() { ./build.sh $C obj_$1 ix_busy_w "${@:2}" > /dev/null 2>&1; echo "$? build $1" >> $H/build.rc; }
b t16_22 -GN_CTRL_P=16 -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 &
b t16_99 -GN_CTRL_P=16 -GN_STREAM_IN_P=9 -GN_STREAM_OUT_P=9 &
b t2_11 -GN_CTRL_P=2 -GN_STREAM_IN_P=1 -GN_STREAM_OUT_P=1 &
b t16_22i -GN_CTRL_P=16 -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 -GEN_IDENTIFY_NOTIF_P=1 &
b t5_88 -GN_CTRL_P=5 -GN_STREAM_IN_P=8 -GN_STREAM_OUT_P=8 &
wait
for o in t16_22:16 t16_99:16 t2_11:2 t16_22i:16 t5_88:5; do
  s=${o%%:*}; n=${o##*:}
  for seed in 1 2 3 4 5 6 7 8; do
    chaos=0; [ $seed -gt 4 ] && chaos=1
    ( ./obj_$s/Vls $seed 1000000 $n $chaos > run_${s}_$seed.log 2>&1; echo "$? $s $seed" >> runs.rc ) &
  done
  wait
done
echo done > $H/ALL.done
