#!/usr/bin/env bash
# R297-3 reviewer gates at the exact head. Usage: static_gates.sh <repo> <receipt-dir>
# Each gate's full output goes to <receipt-dir>/<name>.log; summary.txt lists rc.
set -u
REPO=$1; OUT=$2; mkdir -p "$OUT"; : > "$OUT/summary.txt"
cd "$REPO" || exit 2
gate() { name=$1; shift
  "$@" > "$OUT/$name.log" 2>&1; rc=$?
  printf '%-28s rc=%d  %s\n' "$name" "$rc" "$*" >> "$OUT/summary.txt"; }
gate behave_full          bash -c 'cd tests && behave --no-capture -f plain'
gate docs_check_git       python3 -B scripts/docs_check.py
gate docs_check_nogit     env GIT_DIR=/nonexistent-r297-3-git python3 -B scripts/docs_check.py
gate check_em_dash        python3 -B scripts/check_em_dash.py --base 864b36f5e9450ef64f75ca3f0d68c44330e447d7
gate gen_toc_check        python3 -B scripts/gen_toc.py --check
gate gen_toc_anchors      python3 -B scripts/gen_toc.py --verify-anchors
gate check_doc_style      python3 -B scripts/check_doc_style.py
gate check_doc_paths      python3 -B scripts/check_doc_paths.py
gate measure_test_evidence python3 -B scripts/measure_test_evidence.py --check
gate module_matrix_check  python3 -B docs/traceability/gen_module_matrix.py --check
gate diff_check_delta     git diff --check f219a5edaa191b33acc8b77abd22469f8f0db1f9 6e4a3b420e055ef7529ceb16bb2ab5be93c34487
gate absence_grep         bash -c 'grep -rnE "Residual|pending fix|previous slope" tests/; rc=$?; echo "grep rc=$rc (1 = no match)"; [ $rc -eq 1 ]'
cat "$OUT/summary.txt"
