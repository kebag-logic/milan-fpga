#!/usr/bin/env bash
# Read-only: fetch the parent's gate scripts (and KL_pp_shadow.sv) at parent dev
# 7eb3b0d4 into scratch, and check each blob id against the parent tree listing.
set -euo pipefail
PK=$(cd "$(dirname "$0")/.." && pwd); S=$PK/scratch; REF=7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a
mkdir -p $S/parent-scripts
gh api "repos/kebag-logic/milan-fpga/git/trees/$REF?recursive=1" > $S/parent-tree.json
get() { gh api "repos/kebag-logic/milan-fpga/contents/$1?ref=$REF" -H "Accept: application/vnd.github.raw" > "$2"
  want=$(python3 -c "import json,sys;print([e['sha'] for e in json.load(open('$S/parent-tree.json'))['tree'] if e['path']=='$1'][0])")
  got=$(git hash-object "$2"); [ "$want" = "$got" ] && echo "ok $got $1" || { echo "MISMATCH $1"; exit 1; }; }
for f in check_cpp_idiom check_port_contracts check_py_idiom measure_test_evidence sv_ports lint_rtl lint_rtl_policy code_quality_scope suite_tally; do
  get scripts/$f.py $S/parent-scripts/$f.py; done
get hdl/milan/KL_pp_shadow.sv $S/KL_pp_shadow.sv
