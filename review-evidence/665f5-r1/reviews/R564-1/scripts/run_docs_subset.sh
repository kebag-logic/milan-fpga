#!/usr/bin/env bash
# Reviewer docs/code-quality gate subset over a candidate checkout.
# Usage: run_docs_subset.sh <candidate-root> <python-with-markdown-lock> <log-dir>
set -u
root=$1; py=$2; logs=$3
mkdir -p "$logs"
cd "$root" || exit 2
cmds=(
  "scripts/docs_check.py"
  "scripts/check_em_dash.py --base 5603c353137e90c1fa95429f6d00ef7a2298d9ee"
  "scripts/check_doc_style.py"
  "docs/DOC_MAP.gen.py --check"
  "scripts/check_solution_docs.py"
  "scripts/check_feature_status.py --self-test"
  "docs/traceability/gen_module_matrix.py --check"
  "scripts/check_baremetal_only.py --check"
  "scripts/measure_naming.py --check"
  "scripts/check_port_contracts.py"
  "scripts/measure_fail_fast.py --check"
  "scripts/check_todo_ownership.py"
  "scripts/measure_test_evidence.py --check"
  "scripts/check_hygiene.py --check"
  "scripts/check_cpp_idiom.py"
  "scripts/check_py_idiom.py"
  "scripts/check_sh_idiom.py"
  "scripts/check_doc_paths.py"
  "scripts/gen_toc.py --verify-anchors"
  "scripts/gen_toc.py --check"
  "scripts/ci_events.py --check"
)
n=0
for c in "${cmds[@]}"; do
  n=$((n+1)); name=$(printf '%02d' "$n")
  # shellcheck disable=SC2086
  timeout 560 "$py" -B $c > "$logs/$name.log" 2>&1
  rc=$?
  printf '%s rc=%s %s\n' "$name" "$rc" "$c" | tee -a "$logs/summary.txt"
done
