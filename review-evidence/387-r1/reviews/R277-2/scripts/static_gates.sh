#!/bin/sh
# Run the cheap static documentation and code-quality gates the PR's scope
# touches, at the exact head of a disposable clone. Prints one line per gate
# with its exit code; the full output of each follows its line.
# Usage: static_gates.sh <clone at 021b2e07>
set -u
cd "${1:?usage: static_gates.sh <clone>}"
export PYTHONDONTWRITEBYTECODE=1
base=759da623072358afdb0e9d570a7b4b6a788492c9
echo "head $(git rev-parse HEAD) base $base"
run() {
  name=$1; shift
  out=$("$@" 2>&1); code=$?
  echo "=== GATE $name exit=$code"
  printf '%s\n' "$out" | tail -n 12
}
run docs_check python3 -B scripts/docs_check.py
run check_doc_style python3 scripts/check_doc_style.py
run check_em_dash python3 scripts/check_em_dash.py --base "$base"
run check_gptp_docs python3 scripts/check_gptp_docs.py
run check_gptp_docs_with_submodule python3 scripts/check_gptp_docs.py --with-submodule
run gen_toc_check python3 scripts/gen_toc.py --check
run check_feature_status python3 scripts/check_feature_status.py
run check_submodule_docs python3 scripts/check_submodule_docs.py
run measure_test_evidence_check python3 scripts/measure_test_evidence.py --check
run check_cpp_idiom python3 scripts/check_cpp_idiom.py
run check_py_idiom python3 scripts/check_py_idiom.py
run git_diff_check git diff --check "$base" HEAD
