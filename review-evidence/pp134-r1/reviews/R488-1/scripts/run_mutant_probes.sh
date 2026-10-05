#!/bin/sh
# R488-1: mutant probes for PR #160 at 5ab43bd9.
# Usage: run_mutant_probes.sh <packet-dir>   (head tree in <packet>/scratch/head)
#  - each new arm through the complete default srp_top suite (must fail only S checks)
#  - the older talker-strict-lv / talker-no-expiry arms through the lvleave group
#  - the full checked-in srp_top campaign (coverage incl. S1-S3), --jobs 6
set -eu
P=$1
V=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
export VERILATOR="$V" PATH="$(dirname "$V"):$PATH"
mkdir -p "$P/receipts" "$P/scratch/tmp"
export TMPDIR="$P/scratch/tmp"

arm() {  # name, patch, run_args
  name=$1; patch=$2; args=$3
  t="$P/scratch/arm-$name"
  rm -rf "$t"; mkdir -p "$t/tb"
  cp -r "$P/scratch/head/hdl" "$t/hdl"
  for s in common srp_top; do cp -r "$P/scratch/head/tb/$s" "$t/tb/$s"; done
  rm -rf "$t/tb/srp_top/obj_"*
  # (as run in R488-1 this subshell inherited `set -e`, so a failing make
  # skipped the rc file; the verdicts were read from each log's tally and
  # make's Error line. Fixed below: set +e records the rc.)
  ( set +e; cd "$t" && git apply "$P/scratch/head/tb/srp_top/mutations/$patch.patch" || exit 1
    make -C tb/srp_top RUN_ARGS="$args" > "$P/receipts/arm-$name.log" 2>&1
    echo $? > "$P/receipts/arm-$name.rc" ) &
}
arm full-lv-second-lv-ends lv-second-lv-ends ""
arm full-lv-never-ends lv-never-ends ""
arm lvleave-talker-strict-lv talker-strict-lv lvleave
arm lvleave-talker-no-expiry talker-no-expiry lvleave
mkdir -p "$P/receipts/mutants-full-head"
( cd "$P/scratch/head" && { python3 tb/srp_top/mutants.py --output "$P/receipts/mutants-full-head" --jobs 6 \
    > "$P/receipts/mutants-full-head.log" 2>&1; echo $? > "$P/receipts/mutants-full-head.rc"; } ) &
wait
