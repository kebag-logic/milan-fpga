#!/usr/bin/env bash
# gates.sh <head> <clone> <out>: the round's gates other than docs.yml on a clean clone of <head>, one log and one rc
# per gate, never piped: the pp_shadow suite in every leg (make run: base, vid73, crf, pending), drops-mutant (both
# clean controls, eight arms), the resource gate's check-baseline and self-test (with its mutant campaign),
# docs_inventory.py --check and git diff --check against the merge base. Then the clone's tree state.
set -u
H=$1; C=$2; G=$3
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$G"
cd "$C" || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
test -z "$(git status --porcelain)" || exit 5
source "$here/env.sh"
export MAKEFLAGS="-j8 --no-print-directory --output-sync=target" HOME=$VALIDATION_STORAGE/scratch/854-a756/home-gates
run() { id=$1; shift; { echo "# head $H gate $id: $*"; bash -c "$*"; } > "$G/$id.log" 2>&1; rc=$?; echo $rc > "$G/$id.rc"; echo "$id rc=$rc"; }
run diffcheck "git diff --check ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36 HEAD"
run docs_inventory "python3 scripts/docs_inventory.py --check"
run gate_selftest "python3 syn/ooc/pp_resource_gate.py --selftest"
run gate_mutants "python3 -X cpu_count=4 syn/ooc/pp_resource_gate_mutants.py"
run check_baseline "python3 syn/ooc/pp_resource_gate.py check-baseline"
run pp_shadow "make -C tb/verilator/pp_shadow run"
run drops_mutant "make -C tb/verilator/pp_shadow drops-mutant"
git status --short --ignored > "$G/tree-after.txt"
echo done > "$G/DONE"
