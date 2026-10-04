#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# R458-2: each committed slope control (tb/srp_top/mutations/slope-*.patch) in the
# admission suite one shape at a time (N = 1, 2, 3, 5, 8), to re-measure the
# README/PR-body cells the campaign itself does not reach (it stops at N = 2).
# usage: slope_shapes.sh <head_tree> <work> ; VERILATOR = the pinned tool or a wrapper.
# Runs up to $JOBS (default 4) shapes at once; prints "<patch> N=<n> rc=<rc> <tally>".
set -u
head=$1; work=$2; jobs=${JOBS:-4}
mkdir -p "$work"
for p in slope-stored-at-stage-2-index slope-stored-at-source-0 slope-store-source-0-only slope-read-source-0; do
  for n in 1 2 3 5 8; do
    d="$work/$p-N$n"; rm -rf "$d"; mkdir -p "$d/tb"
    cp -r "$head/hdl" "$d/"; cp -r "$head/tb/common" "$head/tb/srp_admission" "$d/tb/"
    (cd "$d" && git init -q . && git apply "$head/tb/srp_top/mutations/$p.patch") || { echo "$p: patch failed"; exit 1; }
    echo "$p $n $d"
  done
done | {
  while read -r p n d; do
    while [ "$(jobs -r | wc -l)" -ge "$jobs" ]; do sleep 2; done
    ( cd "$d/tb/srp_admission" && make run N="$n" VERILATOR="$VERILATOR" > run.log 2>&1; echo $? > run.rc ) &
  done
  wait
}
for p in slope-stored-at-stage-2-index slope-stored-at-source-0 slope-store-source-0-only slope-read-source-0; do
  for n in 1 2 3 5 8; do
    d="$work/$p-N$n/tb/srp_admission"
    t=$(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$d/run.log" | tail -1)
    echo "$p N=$n rc=$(cat "$d/run.rc" 2>/dev/null || echo none) $t"
  done
done
