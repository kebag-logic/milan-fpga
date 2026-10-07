#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
# usage: run_probe.sh <OFF|ON> <libdir> <label>; REVIEW_SOURCE=exact-head checkout
PKT=$(cd "$(dirname "$0")/.." && pwd); S=$REVIEW_SOURCE; m=$1; L=$2; label=$3
exe="$PKT/scratch/$label-probe"
cc -std=c11 -Wall -Wextra -I"$S/src/include" -I"$S/src" -I"$S/tests/unit" "$PKT/scripts/r540_6_probe.c" "$S/tests/unit/fault_alloc.c" \
  -L"$L" -Wl,-rpath,"$L" -lshlan $PROBE_CFLAGS -o "$exe" > "$PKT/receipts/$label-build.log" 2>&1
echo $? > "$PKT/receipts/$label-build.rc"
"$exe" > "$PKT/receipts/$label.log" 2>&1; rc=$?; echo $rc > "$PKT/receipts/$label.rc"
echo "$label build=$(cat "$PKT/receipts/$label-build.rc") rc=$rc"; tail -1 "$PKT/receipts/$label.log"
