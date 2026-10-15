#!/usr/bin/env bash
# scratch: cold five-leg default, then cold four original legs, on CPUs 0-3, serial outer make
set -u
cd $LANES/645-bind-recentre
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
O=/tmp/a620/wallclock
mkdir -p $O
for mode in five four; do
  rm -rf tb/verilator/follow_ring/obj_dir tb/verilator/follow_ring/obj_dir_fine tb/verilator/follow_ring/obj_dir_control
  start=$(date +%s.%N)
  if [ $mode = five ]; then
    env -u MAKEFLAGS taskset -c 0-3 make -C tb/verilator/follow_ring > $O/$mode.log 2>&1
  else
    env -u MAKEFLAGS taskset -c 0-3 make -C tb/verilator/follow_ring -j4 b8 pullin small-pullin settle-control > $O/$mode.log 2>&1
  fi
  rc=$?
  end=$(date +%s.%N)
  echo "$mode rc=$rc secs=$(python3 -c "print(f'{$end - $start:.3f}')") load=$(cut -d' ' -f1-3 /proc/loadavg)" >> $O/result.txt
done
rm -rf tb/verilator/follow_ring/obj_dir tb/verilator/follow_ring/obj_dir_fine tb/verilator/follow_ring/obj_dir_control
