#!/usr/bin/env bash
# gates3.sh <head> <clone> <out>: the round 3 ruling's gates other than docs.yml on a clean clone of <head>, one log
# and one rc per gate, never piped: git diff --check against the merge base, docs_inventory.py --check, and
# make -C tb/verilator/pp_shadow drops-mutant (both clean controls, eight arms). Then the clone's tree state.
set -u
H=$1; C=$2; G=$3
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$G"
cd "$C" || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
test -z "$(git status --porcelain)" || exit 5
source "$here/env.sh"
export MAKEFLAGS="-j16 --no-print-directory --output-sync=target" HOME=$VALIDATION_STORAGE/scratch/854-a756c/home-gates
mkdir -p "$HOME"
run() { id=$1; shift; { echo "# head $H gate $id: $*"; bash -c "$*"; } > "$G/$id.log" 2>&1; rc=$?; echo $rc > "$G/$id.rc"; echo "$id rc=$rc"; }
run diffcheck "git diff --check ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36 HEAD"
run docs_inventory "python3 scripts/docs_inventory.py --check"
run drops_mutant "make -C tb/verilator/pp_shadow drops-mutant"
git status --short --ignored > "$G/tree-after.txt"
echo done > "$G/DONE"
