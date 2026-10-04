#!/usr/bin/env bash
# the seven planted controls at shape 16/2/2, 8 seeds each (1-4 protocol, 5-8 random)
set -u
H=$SCRATCH/r1b/lockstep; cd $H
for n in last_chunk_ignored no_clear no_override no_set override_set_only refresh_not_reindexed_claim_too stamp_unread_valid; do
  ./build.sh $H/mutf/$n.sv obj_c_$n ix_busy_w -GN_CTRL_P=16 -GN_STREAM_IN_P=2 -GN_STREAM_OUT_P=2 > /dev/null 2>&1; echo "$? build $n" >> ctl-build.rc
  for seed in 1 2 3 4 5 6 7 8; do chaos=0; [ $seed -gt 4 ] && chaos=1
    ( ./obj_c_$n/Vls $seed 1000000 16 $chaos > ctl_${n}_$seed.log 2>&1; echo "$? $n $seed" >> ctl-runs.rc ) &
  done
  wait
done
echo done > CTL.done
