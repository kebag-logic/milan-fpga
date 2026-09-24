#!/bin/sh
# R296-1 disposable probes for PR #553 at 4eca4540d6a278aeb56687029d752bade6e714e3.
# P1: refused cases are warmed with the ADMITTED 224-byte TSpec before the
#     graded 20000-byte re-declaration (the shipped fixture warms with 20000).
# P2: admitted cases are warmed with the REFUSED 20000-byte TSpec first.
# Usage: run_stale_grant_probes.sh <clean clone at the head> <verilator> <out dir>
# The clone's sim_crf_licence.cpp is patched only for the build and restored.
set -eu
REPO=$1; VERILATOR=$2; OUT=$3
HERE=$(cd "$(dirname "$0")" && pwd)
DP="$REPO/tb/verilator/milan_dp"
test "$(git -C "$REPO" rev-parse HEAD)" = 4eca4540d6a278aeb56687029d752bade6e714e3
git -C "$REPO" diff --quiet HEAD
mkdir -p "$OUT"
for p in P1_stale_slope:R296_STALE P2_stale_admit:R296_STALE2; do
  name=${p%%:*}; var=${p##*:}
  git -C "$REPO" apply "$HERE/probe_$name.patch"
  rc=0
  make -C "$DP" crflic-build VERILATOR="$VERILATOR" VERILATOR_JOBS=8 \
       CRFLIC_MDIR="$OUT/obj_$name" > "$OUT/build_$name.log" 2>&1 || rc=$?
  git -C "$REPO" checkout -- tb/verilator/milan_dp/sim_crf_licence.cpp
  test "$rc" = 0
  (cd "$DP" && env "$var=1" "$OUT/obj_$name/Vmilan_dp_crflic" > "$OUT/probe_$name.log" 2>&1) || true
  grep -E 'R296|LATENCY|FAIL\]|checks:|RESULT' "$OUT/probe_$name.log" || true
done
git -C "$REPO" diff --quiet HEAD
