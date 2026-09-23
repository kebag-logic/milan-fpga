#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Build and run datapath mutants on one sim_nxn leg, several at a time.
#
# usage: bash run_mutants.sh <tree> <leg> <harness> <tag> <mutdir> <scratch> <outdir> <par> <id>...
#   harness  file in <tree>/tb/verilator/milan_dp (e.g. sim_nxn.cpp)
#   tag      label for this campaign (goes into build/log names)
#   par      concurrent builds; each uses JOBS=8/par C++ jobs (<= 8 in total)
# For each id, <mutdir>/<id>.sv is built as DP_SRC. A receipt
# <outdir>/<tag>__<id>.txt holds the mutant, harness and binary sha256, the
# build and run exit codes, the harness tally, the verdict and every [FAIL]
# line. The full log stays in <scratch>/mutlogs; the build dir is deleted.
# Verdict: KILLED (built, ran, exit != 0 or failures > 0), SURVIVED (built,
# ran, exit 0, 0 failures), BUILD_FAIL (did not elaborate/compile).
set -eu
tree=$1; leg=$2; harness=$3; tag=$4; mutdir=$5; scratch=$6; outdir=$7; par=$8
shift 8
here=$(cd "$(dirname "$0")" && pwd)
: "${VERILATOR:?set VERILATOR to the pinned 5.050}"
jobs=$((8 / par)); [ "$jobs" -ge 1 ] || jobs=1
mkdir -p "$outdir" "$scratch/mutlogs" "$scratch/builds"
one() {
  id=$1
  sv="$mutdir/$id.sv"
  b="$scratch/builds/${tag}__${id}"
  log="$scratch/mutlogs/${tag}__${id}.log"
  r="$outdir/${tag}__${id}.txt"
  rm -rf "$b"
  if JOBS=$jobs sh "$here/build_leg.sh" "$tree" "$leg" "$b" "$harness" "$sv" > "$log.build" 2>&1; then
    brc=0
  else
    brc=$?
  fi
  {
    echo "campaign=$tag leg=$leg mutant=$id"
    echo "mutant_sha256=$(sha256sum "$sv" | cut -d' ' -f1)"
    echo "harness_sha256=$(sha256sum "$tree/tb/verilator/milan_dp/$harness" | cut -d' ' -f1)"
    echo "build_exit=$brc"
    if [ "$brc" -eq 0 ]; then
      line=$(sh "$here/run_leg.sh" "$tree" "$leg" "$b" "$log")
      echo "$line"
      rc=$(echo "$line" | sed -n 's/.* exit=\([0-9]*\) .*/\1/p')
      fl=$(echo "$line" | sed -n 's/.* failures=\([0-9a-z]*\) .*/\1/p')
      if [ "$rc" = 0 ] && [ "$fl" = 0 ]; then echo "verdict=SURVIVED"; else echo "verdict=KILLED"; fi
      grep '^  \[FAIL\]' "$log" || true
    else
      echo "verdict=BUILD_FAIL"
      grep -m5 '%Error' "$log.build" || true
    fi
  } > "$r"
  rm -rf "$b"
  echo "$id $(grep '^verdict=' "$r")"
}
running=0
for id in "$@"; do
  one "$id" &
  running=$((running + 1))
  if [ "$running" -ge "$par" ]; then wait -n 2>/dev/null || wait; running=$((running - 1)); fi
done
wait
