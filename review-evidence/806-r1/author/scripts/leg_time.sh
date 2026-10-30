#!/usr/bin/env bash
# leg_time.sh <out-dir> <rev>...: run each prebuilt gptp leg binary (clone-leg-<rev8>) concurrently under
# /usr/bin/time, each from its own milan_dp directory; one log and one time line per revision.
set -u
out=$1; shift; mkdir -p "$out"; X=$VALIDATION_STORAGE/scratch/806-a701
for rev in "$@"; do
  d=$X/clone-leg-${rev:0:8}/tb/verilator/milan_dp
  ( cd "$d" && /usr/bin/time -f "rev=${rev:0:8} wall_s=%e user_s=%U sys_s=%S maxrss_kb=%M rc=%x" \
      ./obj_gptp/Vmilan_dp_gptp > "$out/leg-${rev:0:8}.log" 2> "$out/time-${rev:0:8}.txt" ) &
done
wait
cat "$out"/time-*.txt
