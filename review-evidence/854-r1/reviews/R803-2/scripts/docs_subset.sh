#!/usr/bin/env bash
# docs_subset.sh <tree> <outdir>: a focused subset of docs.yml run: steps on a clean copy of the head,
# one log and one rc per step.
set -u
tree=$1; out=$2; mkdir -p "$out"; cd "$tree" || exit 2
i=0
while IFS= read -r cmd; do
  [ -z "$cmd" ] && continue
  i=$((i+1)); id=$(printf 'step%02d' "$i")
  { echo "# $cmd"; bash -c "$cmd"; } > "$out/$id.log" 2>&1; rc=$?
  echo "$rc" > "$out/$id.rc"; printf '%s rc=%s %s\n' "$id" "$rc" "$cmd"
done <<'LIST'
python3 scripts/docs_check.py
python3 scripts/check_feature_status.py
python3 scripts/check_em_dash.py --base ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36
python3 scripts/check_doc_style.py
python3 docs/DOC_MAP.gen.py --check
python3 docs/traceability/gen_module_matrix.py --check
python3 scripts/check_port_contracts.py
python3 scripts/measure_naming.py --check
python3 scripts/measure_fail_fast.py --check
python3 scripts/check_todo_ownership.py
python3 scripts/measure_test_evidence.py --check
python3 scripts/check_hygiene.py --check
python3 scripts/check_sv_idiom.py
python3 scripts/check_cpp_idiom.py
python3 scripts/check_py_idiom.py
python3 scripts/check_doc_paths.py
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/gen_toc.py --check
python3 scripts/check_rtl_source_lists.py
python3 scripts/docs_inventory.py --check
LIST
