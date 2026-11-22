#!/usr/bin/env bash
# Reviewer's docs/tooling gate subset at the reviewed head, run concurrently (each with its own log and rc).
# Usage: docs_gates.sh <repo> <logdir>
set -u
repo=$1; logs=$2; mkdir -p "$logs"; cd "$repo" || exit 2
export PYTHONDONTWRITEBYTECODE=1
cmds=(
 "python3 scripts/docs_check.py"
 "python3 scripts/check_feature_status.py"
 "python3 scripts/check_feature_status.py --self-test"
 "python3 scripts/check_doc_style.py"
 "python3 scripts/check_doc_paths.py"
 "python3 scripts/check_em_dash.py --base 59b09884"
 "python3 scripts/check_py_idiom.py"
 "python3 scripts/check_hygiene.py --check"
 "python3 scripts/docs_inventory.py --check"
 "python3 docs/DOC_MAP.gen.py --check"
 "python3 scripts/gen_toc.py --check"
 "python3 scripts/gen_toc.py --verify-anchors"
 "python3 scripts/check_solution_docs.py"
 "python3 scripts/check_todo_ownership.py"
 "python3 scripts/measure_naming.py --check"
 "python3 scripts/measure_test_evidence.py --check"
 "python3 scripts/measure_fail_fast.py --check"
 "python3 scripts/check_sweep_shape.py --self-test"
 "python3 syn/resmap/soc_sweep.py --selftest"
 "python3 scripts/gen_register_reference.py --check"
 "python3 scripts/check_submodule_docs.py"
 "python3 docs/traceability/gen_module_matrix.py --check"
)
i=0
for c in "${cmds[@]}"; do
  i=$((i+1)); n=$(printf %02d $i)
  ( bash -c "$c" > "$logs/$n.log" 2>&1; echo $? > "$logs/$n.rc" ) &
  echo "$n $c" >> "$logs/index.txt"
  if (( i % 16 == 0 )); then wait; fi
done
wait
while read -r n c; do printf '%s rc=%s  %s  | %s\n' "$n" "$(cat "$logs/$n.rc")" "$c" "$(tail -n1 "$logs/$n.log" | cut -c1-120)"; done < "$logs/index.txt"
