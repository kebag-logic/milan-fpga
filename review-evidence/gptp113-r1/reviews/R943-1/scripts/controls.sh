#!/bin/bash
# Re-run the unplanted passes-test controls, three at once, each with its own log and rc file.
# usage: controls.sh SCRATCH_RUNS OUTDIR
S=$1; R=$2; mkdir -p "$R"
for n in pt-head-control pt-head-control-c0 pt-base-control; do
  pre=""; [ $n = pt-head-control-c0 ] && pre="ulimit -c 0;"
  ( cd "$S/$n" && bash -c "$pre /usr/bin/time -f 'wall %e s' make -C tb/verilator/engine passes-test" > "$R/$n.log" 2>&1; echo $? > "$R/$n.rc" ) &
done
wait; echo DONE > "$R/DONE"
