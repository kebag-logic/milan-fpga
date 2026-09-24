#!/usr/bin/env bash
# Usage: author_suites_on_mutant.sh <head-tree> <mutant.sv> <work-dir> <log-dir>
# Copies hdl + tb/common + tb/srp_admission + tb/srp_top, installs the mutant as
# KL_srp_admission.sv, runs the author's unit suite at N=2 and N=8 and srp_top.
set -uo pipefail
head=$1; mut=$2; work=$3; logs=$4; name=$(basename "$mut" .sv)
rm -rf "$work/$name"; mkdir -p "$work/$name/tb" "$logs"
cp -r "$head/hdl" "$work/$name/"; for s in common srp_admission srp_top; do
  rsync -a --exclude 'obj*' "$head/tb/$s" "$work/$name/tb/"; done
cp "$mut" "$work/$name/hdl/srp/KL_srp_admission.sv"
for run in "srp_admission run N=2" "srp_admission run N=8" "srp_top run"; do
  set -- $run; suite=$1; shift
  tag="$name-$suite${2:+-${2#N=}}"
  (cd "$work/$name/tb/$suite" && make "$@") > "$logs/$tag.log" 2>&1; rc=$?
  echo "$tag rc=$rc $(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$logs/$tag.log" | tail -1)"
done
