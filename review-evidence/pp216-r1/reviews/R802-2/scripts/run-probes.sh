#!/usr/bin/env bash
# Reviewer probes: each patch is applied to its own fresh clone of the exact head
# and graded by one suite; the tally and every FAIL line are recorded.
# usage: run-probes.sh <review-clone> <head-sha> <work-dir> <out-dir> <suite> <run-args> <patch>...
set -u
src=$1; head=$2; work=$3; out=$4; suite=$5; runargs=$6; shift 6
mkdir -p "$work" "$out"
for p in "$@"; do
  name=$(basename "$p" .patch)
  t="$work/$name"
  rm -rf "$t"
  git clone -q --shared "$src" "$t" && git -C "$t" checkout -q --detach "$head"
  if ! (cd "$t" && patch -p1 --no-backup-if-mismatch < "$p") > "$out/$name.apply.log" 2>&1; then
    echo "$name: PATCH-FAILED" > "$out/$name.result"; continue
  fi
  (cd "$t" && make -C "tb/$suite" run RUN_ARGS="$runargs") > "$out/$name.$suite.log" 2>&1
  rc=$?
  tally=$(grep -E '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$out/$name.$suite.log" | tail -1)
  fails=$(grep -E '^\s*FAIL' "$out/$name.$suite.log" | cut -c1-140 | tr '\n' '|')
  echo "$name: rc=$rc tally=[$tally] fails=[$fails]" > "$out/$name.result"
done
