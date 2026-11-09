#!/usr/bin/env bash
# gates3b.sh <head> <clone> <out>: the resource gate on a clean clone of <head>, because round 3 edits
# docs/design/AREA_BUDGET.md and pp_resource_gate.py reads that page's policy table: check-baseline, the self-test
# and the mutant campaign, one log and one rc per gate, never piped. Then the clone's tree state.
set -u
H=$1; C=$2; G=$3
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$G"
cd "$C" || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
source "$here/env.sh"
export HOME=$VALIDATION_STORAGE/scratch/854-a756c/home-gates
mkdir -p "$HOME"
run() { id=$1; shift; { echo "# head $H gate $id: $*"; bash -c "$*"; } > "$G/$id.log" 2>&1; rc=$?; echo $rc > "$G/$id.rc"; echo "$id rc=$rc"; }
run check_baseline "python3 syn/ooc/pp_resource_gate.py check-baseline"
run gate_selftest "python3 syn/ooc/pp_resource_gate.py --selftest"
run gate_mutants "python3 -X cpu_count=4 syn/ooc/pp_resource_gate_mutants.py"
git status --short --ignored > "$G/tree-after-b.txt"
echo done > "$G/DONE-b"
