#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
# usage: profile.sh <OFF|ON>; REVIEW_SOURCE=exact-head checkout, SCRATCH=scratch dir
set -u
mode=$1; B="$SCRATCH/build-$mode"; P="$SCRATCH/prefix"
export CMAKE_PREFIX_PATH="$P" LD_LIBRARY_PATH="$P/lib" CPATH="$P/include" LIBRARY_PATH="$P/lib"
cd "$REVIEW_SOURCE"
step() { name=$1; shift; echo "== $name: $*"; "$@"; rc=$?; echo "== $name rc=$rc"; [ $rc -eq 0 ] || fails=$((fails+1)); }
fails=0
rm -rf "$B"
step configure cmake -S . -B "$B" -DCMAKE_BUILD_TYPE=Debug -DLWSRP_MILAN=$mode
step build cmake --build "$B" --parallel 4
step ctest ctest --test-dir "$B" --output-on-failure
step units "$B/unit_tests"
SHLAN_LIBRARY="$B/libshlan.so" step behave behave
step behave-dry behave --dry-run
echo "profile $mode failures=$fails"
exit $fails
