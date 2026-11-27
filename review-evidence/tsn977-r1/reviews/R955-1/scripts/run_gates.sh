#!/bin/bash
# Run the head's own gates from an extracted copy of the exact-head tree, concurrently, <=16 jobs total.
# Usage: run_gates.sh TREE OUT
set -u
source "$(dirname "$0")/env.sh"
T=$1; O=$2; mkdir -p "$O"; W=$P/scratch/work; mkdir -p $W
step() { local n=$1; shift; ( "$@" ) >"$O/$n.log" 2>&1; echo $? >"$O/$n.rc"; }
gcc_job() { rm -rf $W/gcc; step gcc-configure cmake -S $T -B $W/gcc -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=gcc -DCMAKE_CXX_COMPILER=g++ -DTSN_COVERAGE=ON &&
  step gcc-build cmake --build $W/gcc -j4 && step gcc-test ctest --test-dir $W/gcc --output-on-failure -j4 &&
  (cd $T && step coverage python3 scripts/coverage.py $W/gcc); }
clang_job() { rm -rf $W/clang; step clang-configure cmake -S $T -B $W/clang -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -DTSN_SANITIZERS=ON &&
  step clang-build cmake --build $W/clang -j4 && step clang-test ctest --test-dir $W/clang --output-on-failure -j4; }
mut_job() { rm -rf $W/mut; (cd $T && step mutation python3 scripts/mutation.py --work $W/mut --jobs 6); cp $W/mut/results.json "$O/mutation-results.json" 2>/dev/null; }
rv_job() { rm -rf $W/rv32; (cd $T && step baremetal python3 scripts/baremetal.py --work $W/rv32 --jobs 2); cp $W/rv32/results.json "$O/baremetal-results.json" 2>/dev/null; }
gcc_job & clang_job & mut_job & rv_job & wait
echo done > "$O/ALL.done"
