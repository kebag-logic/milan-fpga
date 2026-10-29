#!/bin/bash
# lwSRP's own suite (doc/tester.md "Run the suites") on one checkout, built outside it: configure, build, ctest,
# the unit runner. The unit framework is cgreen 1.6.5, built in scratch (no system package on this host).
# usage: lwsrp_suite.sh CHECKOUT BUILD_DIR LOG
set -u
C=$1 B=$2 LOG=$3
P=$VALIDATION_STORAGE/665s2b-a683j/cgreen/prefix
export CGREEN_PREFIX=$P CMAKE_PREFIX_PATH=$P LD_LIBRARY_PATH=$P/lib CPATH=$P/include LIBRARY_PATH=$P/lib
{ echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain | wc -l)"
  cd "$C" && cmake -S . -B "$B" -DCMAKE_BUILD_TYPE=Debug -DLWSRP_MILAN=OFF && cmake --build "$B" --parallel 4 \
    && ctest --test-dir "$B" --output-on-failure && "$B/unit_tests"; echo "rc=$?"; } > "$LOG" 2>&1
tail -3 "$LOG"
