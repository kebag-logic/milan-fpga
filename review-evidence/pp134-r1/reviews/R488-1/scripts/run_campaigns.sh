#!/bin/sh
# R488-1 reviewer campaigns for PR #160 at 5ab43bd9 (issue #134).
# Usage: run_campaigns.sh <packet-dir>   (head/base trees already extracted
# with `git archive` into <packet>/scratch/{head,base}).
# Starts each campaign detached with its own log and rc file under
# <packet>/receipts; wait on the rc files.
set -eu
P=$1
V=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
export VERILATOR="$V"
mkdir -p "$P/receipts" "$P/scratch/tmp"
export TMPDIR="$P/scratch/tmp"

start() {  # name, dir, command...
  name=$1; dir=$2; shift 2
  ( cd "$dir" && { "$@" > "$P/receipts/$name.log" 2>&1; echo $? > "$P/receipts/$name.rc"; } ) &
}

# full srp_top default suite (timer-arm FIFO arms + every group), base and head
start srp_top-full-head "$P/scratch/head/tb/srp_top" make VERILATOR="$V"
start srp_top-full-base "$P/scratch/base/tb/srp_top" make VERILATOR="$V"
# the checked-in campaign driver: control lvleave + the two new arms
mkdir -p "$P/receipts/mutants-head"
start mutants-new-head "$P/scratch/head" env PATH="$(dirname "$V"):$PATH" \
  python3 tb/srp_top/mutants.py --output "$P/receipts/mutants-head" \
  --only lv-second-lv-ends,lv-never-ends --jobs 3
wait
