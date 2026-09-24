#!/usr/bin/env bash
# Run the documentation gates the PR names, in the review clone, foreground,
# one after another. Prints each command, its tail, and its exit status.
# Usage: run_doc_gates.sh <clone> <base-sha>
set -u
cd "$1" || exit 2
base=$2
run() {
  echo "### $*"
  out=$("$@" 2>&1); rc=$?
  printf '%s\n' "$out" | tail -n 4
  echo "### exit=$rc"
  echo
}
export PYTHONDONTWRITEBYTECODE=1
run python3 -B scripts/docs_check.py
run python3 -B scripts/check_em_dash.py --base "$base"
run python3 -B scripts/check_em_dash.py --selftest
run python3 -B scripts/check_feature_status.py
run python3 -B scripts/check_feature_status.py --self-test
run python3 -B scripts/check_baremetal_only.py --check
run python3 -B docs/traceability/gen_module_matrix.py --check
run python3 -B scripts/check_gptp_docs.py --with-submodule
run python3 -B scripts/check_doc_style.py
run python3 -B scripts/gen_toc.py --check
run python3 -B scripts/gen_toc.py --verify-anchors
run python3 -B scripts/check_doc_paths.py
run python3 -B scripts/check_submodule_docs.py
run git diff --check "$base" HEAD
