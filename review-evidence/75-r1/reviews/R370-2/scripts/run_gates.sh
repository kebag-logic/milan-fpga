#!/usr/bin/env bash
# Run the assigned documentation and policy gates in one tree and print rc per gate.
# Usage: run_gates.sh PYTHON TREE MODE   (MODE: full | nosub | nogit)
set -u
PY="$1"; TREE="$2"; MODE="$3"
cd "$TREE" || exit 2
run() {
  local label="$1"; shift
  local out rc
  out="$(timeout 900 "$@" 2>&1)"; rc=$?
  printf '=== %s\nrc=%s\n%s\n' "$label" "$rc" "$(printf '%s\n' "$out" | tail -n 4)"
}
echo "mode=$MODE"
if [ "$MODE" != nogit ]; then echo "head=$(git rev-parse HEAD) tree=$(git rev-parse HEAD^{tree})"; fi
run "docs_check.py" "$PY" -B scripts/docs_check.py
run "check_feature_status.py" "$PY" -B scripts/check_feature_status.py
if [ "$MODE" = full ]; then
  run "check_doc_style.py" "$PY" -B scripts/check_doc_style.py
  run "gen_toc.py --check" "$PY" -B scripts/gen_toc.py --check
  run "check_em_dash.py --base 8bc97021" "$PY" -B scripts/check_em_dash.py --base 8bc97021
  run "check_doc_paths.py" "$PY" -B scripts/check_doc_paths.py
  run "ci_scope.py --selftest" "$PY" -B scripts/ci_scope.py --selftest
  run "check_baremetal_only.py --check" "$PY" -B scripts/check_baremetal_only.py --check
  run "check_feature_status.py --self-test" "$PY" -B scripts/check_feature_status.py --self-test
  run "git diff --check base..head" git diff --check 8bc97021f28fb7f729418d3a00851c84ea0b50fd 5c7577e51702b00683a121f97a9806c167eb072b
  run "git diff --check (worktree)" git diff --check
fi
