#!/usr/bin/env bash
# milan_dp's timed notify leg at the merged head, at the processor pin the
# merge brings (93fb0b2d): its own build and run, the suite's recipe.
# usage: notify.sh <clone> <out>
set -u
here=$(cd "$(dirname "$0")" && pwd)
source "$here/env.sh"
export TSN_GEN_ROOT=$VALIDATION_STORAGE/scratch/632-a659/tsn-gen
C=$1; O=$2; mkdir -p "$O"
cd "$C/tb/verilator/milan_dp" || exit 2
git rev-parse HEAD > "$O/HEAD.txt"; git -C ../../../protocol-processor rev-parse HEAD > "$O/pp_HEAD.txt"
date -Is > "$O/start"
make --no-print-directory ci-prepare > "$O/ci_prepare.log" 2>&1; echo "ci-prepare rc=$?" > "$O/summary.txt"
make --no-print-directory build-notify > "$O/build_notify.log" 2>&1; echo "build-notify rc=$?" >> "$O/summary.txt"
make --no-print-directory exec-notify > "$O/notify.log" 2>&1; echo "exec-notify rc=$?" >> "$O/summary.txt"
grep -E 'checks: *[0-9]+ +failures: *[0-9]+|[0-9]+ checks, [0-9]+ failures' "$O/notify.log" | tail -1 >> "$O/summary.txt"
date -Is > "$O/end"
