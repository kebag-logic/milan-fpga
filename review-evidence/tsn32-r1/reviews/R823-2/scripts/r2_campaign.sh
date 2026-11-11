#!/bin/sh
# Round 2 reviewer campaign for tsn-c-stack #32 at a530ecaf (disposable trees under scratch/).
# Runs the named jobs concurrently in the foreground of this shell and waits for all of them.
# Each job writes receipts/r2/NAME.log and receipts/r2/NAME.rc.
# Usage: TSN_TOOLS=<pinned tool root> r2_campaign.sh REVIEW_CLONE JOB...
# Jobs: differential plants conditionals-host conditionals-pinned probes mutation-walk sanitizers unit-gcc
: "${TSN_TOOLS:?set TSN_TOOLS to the pinned tool root}"
P=$(cd "$(dirname "$0")/.." && pwd)
S=$P/scratch
R=$1; shift
O=$P/receipts/r2
mkdir -p "$O"
GT="PKG_CONFIG_PATH=$TSN_TOOLS/gtest-1.14.0/lib/pkgconfig CMAKE_PREFIX_PATH=$TSN_TOOLS/gtest-1.14.0 LD_LIBRARY_PATH=$TSN_TOOLS/gtest-1.14.0/lib"
job() {
    name=$1; shift
    ( "$@" > "$O/$name.log" 2>&1; echo $? > "$O/$name.rc" ) &
}
for j in "$@"; do
    case $j in
    differential)
        job differential sh "$P/scripts/differential.sh" "$S/head-san" "$S/main" "$S/diff-out" 60 ;;
    plants)
        job plants sh -c "python3 -I '$P/scripts/plant_delta.py' '$R' 9deb0ddb a530ecaf > '$O/plant-delta.txt'; a=\$?;
            python3 -I '$P/scripts/plant_defects.py' '$R' 9deb0ddb a530ecaf > '$O/plant-defects.txt'; b=\$?;
            python3 -I '$P/scripts/plant_merge.py' '$R' ea4af6f fa31d4c 9deb0ddb a530ecaf > '$O/plant-merge.txt'; c=\$?;
            echo \"delta \$a defects \$b merge \$c\"; [ \$a\$b\$c = 000 ]" ;;
    conditionals-host)
        # The host's Clang (clang/clang++ on the host PATH) stands in for the pinned Clang 18 as clang and clang++;
        # clang-18, which the token checks call by that name, stays the pinned Clang 18.1.3.
        job conditionals-host env $GT PATH="$TSN_TOOLS/clang-18/bin:$PATH" sh -c "cd '$S/head-cond' && clang++ --version | head -1 && python3 scripts/check_conditionals.py --selftest --work '$S/cond-host' --jobs 16" ;;
    conditionals-pinned)
        job conditionals-pinned env $GT TSN_TOOLS="$TSN_TOOLS" PATH="$S/shim:$TSN_TOOLS/clang-18/bin:$PATH" sh -c "mkdir -p '$S/cond-pinned' && cd '$S/head-cond' && clang++ --version | head -1 && python3 scripts/check_conditionals.py --selftest --work '$S/cond-pinned' --jobs 16" ;;
    probes)
        job probes env $GT python3 -I "$P/scripts/probe_mutants.py" "$S/head-probe" "$S/main" "$S/probe-out" ;;
    mutation-walk)
        job mutation-walk env $GT TSN_TOOLS="$TSN_TOOLS" PATH="$TSN_TOOLS/clang-18/bin:$TSN_TOOLS/clang-tidy-18/bin:$PATH" sh -c "cd '$S/head-mut' && python3 scripts/mutation.py --work '$S/mut-walk' --jobs 12 --select walk-" ;;
    sanitizers)
        job sanitizers sh "$P/scripts/sanitizers_standin.sh" "$S/head-san" "$S/san-work" 8 ;;
    unit-gcc)
        job unit-gcc env $GT sh -c "cmake -S '$S/head-san' -B '$S/gcc-unit' -DCMAKE_BUILD_TYPE=Debug && cmake --build '$S/gcc-unit' -j8 && ctest --test-dir '$S/gcc-unit' --output-on-failure -j8" ;;
    *) echo "unknown job $j"; exit 2 ;;
    esac
done
wait
for j in "$@"; do echo "$j rc=$(cat "$O/$j.rc")"; done
