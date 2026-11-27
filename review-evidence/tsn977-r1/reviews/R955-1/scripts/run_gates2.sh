#!/bin/bash
# Re-run: mutation campaign (clang-18 used only for raw-token lexing) and the sanitizer arm with the host Clang,
# because Clang 18 cannot parse this host's GCC 16 libstdc++ headers. Usage: run_gates2.sh TREE OUT
set -u
source "$(dirname "$0")/env.sh"
T=$1; O=$2; mkdir -p "$O"; W=$P/scratch/work; mkdir -p $W
step() { local n=$1; shift; ( "$@" ) >"$O/$n.log" 2>&1; echo $? >"$O/$n.rc"; }
clang_job() { rm -rf $W/clanghost; step clanghost-configure cmake -S $T -B $W/clanghost -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=/usr/bin/clang -DCMAKE_CXX_COMPILER=/usr/bin/clang++ -DTSN_SANITIZERS=ON &&
  step clanghost-build cmake --build $W/clanghost -j6 && step clanghost-test ctest --test-dir $W/clanghost --output-on-failure -j6; }
mut_job() { rm -rf $W/mut; (cd $T && step mutation python3 scripts/mutation.py --work $W/mut --jobs 10); cp $W/mut/results.json "$O/mutation-results.json" 2>/dev/null; }
clang_job & mut_job & wait
echo done > "$O/ALL2.done"
