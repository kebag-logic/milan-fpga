#!/bin/bash
# Reviewer probe runs with the instrumented binary; inputs from the faithful builds.
# usage: probe_runs.sh <scratch>
set -u
S=$1
B1=$S/build-endstation_ax7101_1x1_tdm8; B8=$S/build-endstation_ax7101_8x8
mkdir -p $S/runs
printf 'milan_nvm\nmilan_nvm\nmilan_nvm\n' > $S/runs/plan-status3.txt
printf 'milan_nvm commit\n' > $S/runs/plan-commit1.txt
run() { # name build commands erase_us program_us
  local n=$1 b=$2 c=$3 e=$4 p=$5
  ( cd $b/gateware && PROBE_LOG=$S/runs/$n.probe /usr/bin/time -v $S/probe-$6/native/Vsim $b/aem_desc.bin $b/slots.bin $c $e $p > $S/runs/$n.log 2> $S/runs/$n.err; echo "$n rc=$?" >> $S/runs/status.txt ) &
}
run PA-1x1-standard $B1 $B1/commands.txt 0 0 1x1
run PB-8x8-standard $B8 $B8/commands.txt 1000 1000 8x8
run PC-8x8-commit-devicemax $B8 $S/runs/plan-commit1.txt 3000000 5000 8x8
run PD-8x8-status3 $B8 $S/runs/plan-status3.txt 0 0 8x8
wait
echo DONE >> $S/runs/status.txt
