#!/bin/sh
# Launch the three dynamic campaigns concurrently, each in its own clone of
# head 84fd227 with its own log and rc file.
# usage: launch_dynamic.sh <source repo> <packet dir>
set -u
SRC=$1; P=$2; S=$P/scratch; R=$P/receipts/dynamic
H=84fd22781c95f7b7e65d7d18c99a5ed49a68e11c
mkdir -p "$R" "$S/tmp"
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH TMPDIR=$S/tmp
for c in parser engine arm; do
  rm -rf "$S/c-$c"; git clone -q --no-hardlinks "$SRC" "$S/c-$c"
  git -C "$S/c-$c" checkout -q --detach $H
done
verilator --version > "$R/verilator-version.txt"
( cd "$S/c-parser" && make -C tb/verilator/parser > "$R/parser.log" 2>&1; echo $? > "$R/parser.rc" ) &
( cd "$S/c-engine" && make -C tb/verilator/engine run > "$R/engine-run.log" 2>&1; echo $? > "$R/engine-run.rc" ) &
( cd "$S/c-arm" && python3 "$P/scripts/engine_arm_subset.py" tb/verilator/engine "$R/engine-arm-p100.jsonl" --jobs 8 > "$R/engine-arm-p100.log" 2>&1; echo $? > "$R/engine-arm-p100.rc" ) &
echo launched
