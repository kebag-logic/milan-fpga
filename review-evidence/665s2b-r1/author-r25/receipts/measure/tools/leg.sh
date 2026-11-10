#!/bin/bash
# One harness leg: build (or reuse) a point and run groups from a checkout, every row and pass finding recorded.
# usage: leg.sh CHECKOUT NAME POINT GROUPS|all [extra run.py args]
set -u
. <scratch>/scripts/env.sh
C=$1 NAME=$2 POINT=$3 GROUPS_ARG=$4; shift 4
B=<scratch>/builds
L=<scratch>/logs
mkdir -p "$B" "$L"
export TMPDIR=<scratch>/tmp-$NAME; mkdir -p "$TMPDIR"
export MAKEFLAGS="-j8 --no-print-directory"
reuse=()
[ -f "$B/$NAME/build.json" ] && reuse=(--reuse-build)
g=()
[ "$GROUPS_ARG" != all ] && g=(--groups "$GROUPS_ARG")
start=$(date +%s)
echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=no | wc -l)" > "$L/$NAME.log"
python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$B/$NAME" "${reuse[@]}" \
  "${g[@]}" --record-budget-findings --record-share-findings --jobs "${JOBS:-8}" "$@" >> "$L/$NAME.log" 2>&1
rc=$?
echo "elapsed=$(( $(date +%s) - start ))s" >> "$L/$NAME.log"
echo "rc=$rc" >> "$L/$NAME.log"
