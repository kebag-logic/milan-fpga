#!/usr/bin/env bash
# Diff each suite log of two per-suite runs after masking only what differs by
# construction between two trees and two runs: the tree's own path, Verilator's
# walltime/cpu/memory report line, and unittest's duration. Prints, per suite,
# the number of differing lines left (0 = every other printed line identical).
# usage: norm_diff.sh BASE_DIR HEAD_DIR BASE_TREE HEAD_TREE
b=$1; h=$2; bt=$3; ht=$4
norm() { sed -e "s#$2#TREE#g" -e 's/^- Verilator: Walltime .*/- Verilator: Walltime MASKED/' \
             -e 's/^\(Ran [0-9]* tests\? in \)[0-9.]*s$/\1MASKEDs/' "$1"; }
for f in "$h"/*.log; do
  s=$(basename "$f" .log)
  n=$(diff <(norm "$b/$s.log" "$bt") <(norm "$f" "$ht") | grep -c '^[<>]')
  echo "$s rc $(cat "$b/$s.rc")/$(cat "$h/$s.rc") lines $(wc -l <"$f") residual-diff $n"
done
