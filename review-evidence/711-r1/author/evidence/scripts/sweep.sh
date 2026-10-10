#!/bin/bash
# Full Verilator sweep at the head (never beside a Vivado route). Writes sweep/go-vendor when a run completed.
root=$SCRATCH
export PATH=$root/bin5050:$PATH TMPDIR=$root/tmp PYTHONDONTWRITEBYTECODE=1 VERILATOR_JOBS=2 MAKEFLAGS=-j8
cd $root/sweep-cand || exit 2
mkdir -p $root/sweep
echo "$(date -Is) start $(verilator --version)" > $root/sweep/summary.txt
start=$SECONDS
scripts/run_all_suites.sh $root/sweep/logs > $root/sweep/run.log 2>&1
rc=$?
echo "$(date -Is) rc=$rc seconds=$((SECONDS - start)) status=$(git status --porcelain --untracked-files=all | tr '\n' ' ')" >> $root/sweep/summary.txt
grep -q "ABORTING: sweep cancellation controls failed" $root/sweep/run.log || touch $root/sweep/go-vendor
