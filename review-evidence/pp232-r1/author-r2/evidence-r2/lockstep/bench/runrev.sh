#!/usr/bin/env bash
# the reviewers' two rewrite-window edits at shape 16/2/2, 8 seeds each (1-4 protocol, 5-8 random), 1,000,000 cycles
set -u
H=$SCRATCH/r2/lockstep; cd $H
for n in override_set_only own_compare_new_row; do
  ./build.sh $H/rev/$n.sv obj_r_$n ix_busy_w -GN_CTRL_P=16 -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 > /dev/null 2>&1; echo "$? build $n" >> rev-build.rc
  for seed in 1 2 3 4 5 6 7 8; do chaos=0; [ $seed -gt 4 ] && chaos=1
    ( ./obj_r_$n/Vls $seed 1000000 16 $chaos > rev_${n}_$seed.log 2>&1; echo "$? $n $seed" >> rev-runs.rc ) &
  done
  wait
done
echo done > REV.done
