#!/usr/bin/env bash
# rtl_gates.sh OUTDIR: Yosys (full serial gate) and behave at the committed head.
set -u
out="$1"; mkdir -p "$out"
source $VALIDATION_STORAGE/scratch/a662/env.sh
unset MAKEFLAGS
cd $LANES/771-pin4 || exit 2
echo "head=$(git rev-parse HEAD) dirty=$(git status --porcelain | wc -l) $(yosys -V 2>/dev/null | head -1)" > "$out/env.txt"
t0=$SECONDS; syn/yosys/run.sh > "$out/yosys.log" 2>&1; echo $? > "$out/yosys.rc"; echo $((SECONDS - t0)) > "$out/yosys.seconds"
t0=$SECONDS; (cd tests && python3 -B -m behave -f plain) > "$out/behave.log" 2>&1; echo $? > "$out/behave.rc"; echo $((SECONDS - t0)) > "$out/behave.seconds"
echo "head_after=$(git rev-parse HEAD) dirty=$(git status --porcelain | wc -l)" >> "$out/env.txt"
date -Is > "$out/done"
