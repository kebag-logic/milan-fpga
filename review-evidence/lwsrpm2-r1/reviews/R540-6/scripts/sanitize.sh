#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
# usage: sanitize.sh <OFF|ON>; ASan/UBSan units plus both probes. REVIEW_SOURCE, SCRATCH set.
set -u
m=$1; B="$SCRATCH/san-$m"; P="$SCRATCH/prefix"; S=$REVIEW_SOURCE
F='-fsanitize=address,undefined -fno-omit-frame-pointer -fno-sanitize-recover=all'
export LD_LIBRARY_PATH="$P/lib"
rm -rf "$B"; fails=0
step() { echo "== $*"; "$@"; rc=$?; echo "== rc=$rc"; [ $rc -eq 0 ] || fails=$((fails+1)); }
step cmake -S "$S" -B "$B" -DCMAKE_BUILD_TYPE=Debug -DCMAKE_PREFIX_PATH="$P" -DLWSRP_MILAN=$m "-DCMAKE_C_FLAGS=$F" "-DCMAKE_EXE_LINKER_FLAGS=$F" "-DCMAKE_SHARED_LINKER_FLAGS=$F"
step cmake --build "$B" --parallel 4
step "$B/unit_tests"
for probe in "$PKT_SCRIPTS/r540_6_probe.c" "$SCRATCH/ev/reviews/R541-5/scripts/probe.c"; do
  exe="$B/$(basename "$probe" .c)"
  step cc -std=c11 $F -I"$S/src/include" -I"$S/src" -I"$S/tests/unit" "$probe" "$S/tests/unit/fault_alloc.c" -L"$B" -Wl,-rpath,"$B" -lshlan -o "$exe"
  step "$exe"
done
step "$B/probe" cross-port
echo "sanitize $m failures=$fails"; exit $fails
