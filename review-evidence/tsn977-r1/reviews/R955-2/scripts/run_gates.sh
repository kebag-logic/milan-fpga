#!/bin/bash
# Re-run the quality job's gates (scripts/validate.py's command list, continuing past failures)
# and the bare-metal job from an extracted exact-head tree, <=16 parallel jobs. Usage: run_gates.sh TREE OUT
set -u
source "$(dirname "$0")/env.sh"
T=$1; O=$2; mkdir -p "$O"; W=$P/scratch/work; mkdir -p $W/temp
export TMPDIR=$W/temp
step() { local n=$1; shift; ( "$@" ) >"$O/$n.log" 2>&1; local rc=$?; echo $rc >"$O/$n.rc"; echo "$n rc $rc" >>"$O/summary.txt"; return $rc; }
: >"$O/summary.txt"
cd $T
# Phase 1: source and metadata gates, in validate.py's order.
step entity-golden python3 scripts/entity_yaml.py --examples --check
step entity-controls python3 scripts/entity_selftest.py --work $W/entity-controls
step boundary python3 scripts/check_boundary.py --selftest --work $W/boundary --jobs 8
step needles python3 scripts/needle_audit.py --selftest
step assertion-templates python3 scripts/assertion_templates.py --check --selftest --work $W/assertion-templates
step dependencies python3 scripts/dependency_selftest.py --work $W/dependency-controls --jobs 8
step comments python3 scripts/check_comments.py --selftest --work $W/comment-controls
step conditionals python3 scripts/check_conditionals.py --selftest --work $W/conditionals --jobs 8
step port-contracts python3 scripts/check_port_contracts.py --selftest
step acmp-cache python3 scripts/check_acmp_cache.py --selftest --work $W/acmp-cache-controls --jobs 8
step registration-controls python3 scripts/registration_selftest.py --work $W/registration-controls
step license python3 scripts/check_license.py --selftest
step traceability python3 scripts/traceability.py --selftest --build $W/registration --jobs 8
step test-inventory python3 scripts/test_inventory.py --build $W/registration --jobs 8
step coverage-controls python3 scripts/coverage_selftest.py
step privacy-selftest python3 scripts/check_privacy.py --selftest
step privacy python3 scripts/check_privacy.py
# Phase 2: builds, campaign and RV32 concurrently (3+3+8+2 = 16 jobs).
gcc_job() { rm -rf $W/gcc; step gcc-configure cmake -S $T -B $W/gcc -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=gcc -DCMAKE_CXX_COMPILER=g++ -DTSN_COVERAGE=ON &&
  step gcc-build cmake --build $W/gcc -j3 && { find $W/gcc -name '*.gcda' -delete; step gcc-test ctest --test-dir $W/gcc --output-on-failure -j3; } &&
  step coverage python3 scripts/coverage.py $W/gcc; }
clang_job() { rm -rf $W/clanghost; step clanghost-configure cmake -S $T -B $W/clanghost -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=/usr/bin/clang -DCMAKE_CXX_COMPILER=/usr/bin/clang++ -DTSN_SANITIZERS=ON &&
  step clanghost-build cmake --build $W/clanghost -j3 && step clanghost-test ctest --test-dir $W/clanghost --output-on-failure -j3; }
mut_job() { rm -rf $W/mut; step mutation python3 scripts/mutation.py --work $W/mut --jobs 8; cp $W/mut/results.json "$O/mutation-results.json" 2>/dev/null; }
rv_job() { rm -rf $W/rv32; step baremetal python3 scripts/baremetal.py --work $W/rv32 --jobs 2; cp $W/rv32/results.json "$O/baremetal-results.json" 2>/dev/null; }
gcc_job & clang_job & mut_job & rv_job & wait
# Phase 3: remaining quality gates.
step static-analysis python3 scripts/static_analysis.py
step mutation-controls python3 scripts/mutation_selftest.py --work $W/mutation-controls --jobs 8
step graphs python3 scripts/render_graphs.py --output $W/graphs
echo done > "$O/ALL.done"
