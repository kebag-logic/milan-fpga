#!/usr/bin/env bash
# milan_dp at the head, every leg: the suite's own run target with the notify
# leg left out of the pool (it fails at the current processor pin by design and
# the pool starts no leg after a failure), then the notify leg alone.
set -u
C=$VALIDATION_STORAGE/scratch/632-a659/r3/clone-sweep
L=$VALIDATION_STORAGE/scratch/632-a659/r3/logs
export PATH=$VALIDATION_STORAGE/scratch/632-a659/r3/bin:$VALIDATION_STORAGE/scratch/632-a659/r2/venv31213/bin:$PATH
export VERILATOR_JOBS=2 SIM_JOBS=2 JOBS=2 START_JOBS=2 POOL=2
cd "$C/tb/verilator/milan_dp"
date -Is > $L/mdp_all.start
make clean > /dev/null 2>&1
/usr/bin/time -f 'wall %e s' make run ORDINARY_CASES="base crflic dynmap nxn nxndv nxn8 nxn4c nolpf prune ax1x1 aclk" > $L/mdp_all.log 2>&1
echo $? > $L/mdp_all.rc
/usr/bin/time -f 'wall %e s' make run-notify > $L/mdp_notify.log 2>&1
echo $? > $L/mdp_notify.rc
date -Is > $L/mdp_all.end
