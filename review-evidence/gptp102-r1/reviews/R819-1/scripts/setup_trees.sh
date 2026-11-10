#!/bin/sh
# Extract the exact head and the base into disposable trees, and put the
# pinned Verilator first on PATH through a symlink directory.
# usage: setup_trees.sh <clone> <packet>
set -eu
CLONE=$1; PKT=$2; S=$PKT/scratch
HEAD=97d83a72f4939ff938917deef33fa1ec1a5ba810
BASE=1616fc8f062fbf58c35ad31674b5b233207bbdb8
for t in head base gates; do rm -rf "$S/$t"; mkdir -p "$S/$t"; done
git -C "$CLONE" archive "$HEAD" | tar -x -C "$S/head"
git -C "$CLONE" archive "$HEAD" | tar -x -C "$S/gates"
git -C "$CLONE" archive "$BASE" | tar -x -C "$S/base"
mkdir -p "$S/bin"
ln -sf $VALIDATION_TOOLS/pinned-verilator-5.050/verilator "$S/bin/verilator"
PATH=$S/bin:$PATH verilator --version
