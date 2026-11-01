#!/usr/bin/env bash
# usage: gates.sh <checkout> <log-dir>; runs the docs and hygiene gates, one log per gate
set -u
dir=$1; out=$2
mkdir -p "$out"
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH TMPDIR=$VALIDATION_STORAGE/gptp96-a707e/tmp
mkdir -p "$TMPDIR"
cd "$dir" || exit 9
{ echo "head $(git rev-parse HEAD)"; echo "verilator $(command -v verilator)"; verilator --version; } > "$out/identity.txt" 2>&1
run() { name=$1; shift; "$@" > "$out/$name.log" 2>&1; rc=$?; echo "$name rc=$rc" >> "$out/rc.txt"; }
: > "$out/rc.txt"
run docs make docs
run diagrams-check make diagrams-check
run contract make contract
run lint make lint
run diff-check-main git diff --check 135afd043309369a87ddbc8d6550aff8ec52a157 HEAD
run diff-check-r4 git diff --check db9ab2215ba18aec4c1828090b3611b001dbf2b8 HEAD
run status git status --porcelain
