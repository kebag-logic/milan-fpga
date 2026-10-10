#!/bin/bash
export TMPDIR=$SCRATCH/tmp PYTHONDONTWRITEBYTECODE=1
cd $SCRATCH/yosys-cand || exit 2
start=$SECONDS
syn/yosys/run.sh --results $SCRATCH/yosys/results > $SCRATCH/yosys/run.log 2>&1
rc=$?
echo "rc=$rc seconds=$((SECONDS - start)) clean=$(git status --porcelain --untracked-files=all | wc -l)" > $SCRATCH/yosys/summary.txt
