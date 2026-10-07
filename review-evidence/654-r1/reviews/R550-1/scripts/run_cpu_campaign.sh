#!/usr/bin/env bash
# Sequential CPU-option campaign for one CPU family at one recipe source.
# Usage: run_cpu_campaign.sh PYTHON SOC_PY CPU DATA_DIR WORK_DIR
# Writes WORK_DIR/<cpu>-<xlen>-<option>.{json,log,rc}; exits non-zero if any case failed.
set -u
py=$1 soc=$2 cpu=$3 data=$4 work=$5
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$work"
export PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1
fail=0
for xlen in 32 64; do
  for opt in none fpu l2 zero; do
    tag=$cpu-$xlen-$opt
    rm -rf "$work/build-$tag"
    "$py" "$here/measure_cpu_option.py" "$soc" "$cpu" "$xlen" "$opt" "$data" \
      "$work/build-$tag" "$work/$tag.json" >"$work/$tag.log" 2>&1
    rc=$?; echo "$rc" >"$work/$tag.rc"; echo "$tag rc=$rc"
    [ "$rc" = 0 ] || fail=1
  done
done
exit $fail
