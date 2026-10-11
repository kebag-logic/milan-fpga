#!/bin/sh
# Run the donor gates in two disposable exports of one commit, concurrently.
# usage: run_gates.sh <repo> <commit> <workdir> <receipt-dir> <verilator-shim-dir>
# Each gate writes <receipt-dir>/<gate>.log and <receipt-dir>/<gate>.rc.
set -u
repo=$1 commit=$2 work=$3 out=$4 shim=$5
PATH=$shim:$PATH; export PATH
mkdir -p "$work/tbtree" "$work/gatetree" "$out"
git -C "$repo" archive "$commit" | tar -x -C "$work/tbtree"
git -C "$repo" archive "$commit" | tar -x -C "$work/gatetree"
verilator --version > "$out/verilator-version.txt" 2>&1
( cd "$work/tbtree" && make -j16 tb > "$out/make-tb.log" 2>&1; echo $? > "$out/make-tb.rc" ) &
( cd "$work/gatetree" && { make contract > "$out/make-contract.log" 2>&1; echo $? > "$out/make-contract.rc"; \
  make lint > "$out/make-lint.log" 2>&1; echo $? > "$out/make-lint.rc"; \
  make docs > "$out/make-docs.log" 2>&1; echo $? > "$out/make-docs.rc"; } ) &
wait
