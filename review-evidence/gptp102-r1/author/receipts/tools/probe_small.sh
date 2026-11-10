#!/bin/bash
# Time the gaskets and tsngen mutant drivers serially, alone, at main (item 5 decision).
S=/data-2/milan/tmp/gptp102-a762
C=$S/probe/clone
for t in "tb/verilator/gaskets mutants" "tb/tsngen mutants"; do
  set -- $t
  name=$(echo $1 | tr / _)
  python3 $S/tools/timed_make.py $C $S/runs/probe-$name -C $1 $2
done
