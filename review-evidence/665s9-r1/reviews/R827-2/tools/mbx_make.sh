#!/bin/bash
# mbx_make.sh <source clone> <scratch dir> <verilator> <log>
# Copies the clone and runs the mailbox bench's default make (suites + quick mutants).
set -u
src=$1; dir=$2; vl=$3; log=$4
rm -rf "$dir"; cp -a "$src" "$dir"
{
  echo "head $(git -C "$src" rev-parse HEAD)"; "$vl" --version
  echo "command: make -C tb/verilator/mbx VERILATOR=<pinned 5.050> VBUILD_JOBS=16"
  echo "---"
  make -C "$dir/tb/verilator/mbx" VERILATOR="$vl" VBUILD_JOBS=16
  echo "rc=$?"
  echo "tree after:"; git -C "$dir" status --porcelain --untracked-files=no
} > "$log" 2>&1
