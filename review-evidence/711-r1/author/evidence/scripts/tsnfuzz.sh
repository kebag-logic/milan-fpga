#!/bin/bash
# The tsn_fuzz suite with the CI-pinned tsn-gen field oracle, after the vendor stages.
root=$SCRATCH
# runs immediately
export PATH=$root/bin5050:$PATH TMPDIR=$root/tmp PYTHONDONTWRITEBYTECODE=1 VERILATOR_JOBS=2 MAKEFLAGS=-j8 TSN_GEN_ROOT=$root/tsn-gen
cd $root/sweep-cand || exit 2
mkdir -p $root/tsnfuzz
echo "$(date -Is) start tsn-gen $(git -C $TSN_GEN_ROOT rev-parse HEAD)" > $root/tsnfuzz/summary.txt
start=$SECONDS
timeout 1800 make -C tb/verilator/tsn_fuzz > $root/tsnfuzz/tsn_fuzz.log 2>&1
rc=$?
python3 scripts/suite_tally.py --verdict $root/tsnfuzz/tsn_fuzz.log > $root/tsnfuzz/verdict.txt 2>&1
vrc=$?
echo "$(date -Is) make rc=$rc verdict rc=$vrc seconds=$((SECONDS - start)) status=$(git status --porcelain --untracked-files=all | tr '\n' ' ')" >> $root/tsnfuzz/summary.txt
