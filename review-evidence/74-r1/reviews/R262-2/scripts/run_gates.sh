#!/bin/sh
# Focused static/doc gates for the delta (REGISTER_MAP.md, the comment-only
# KL_media_grid_align.sv hunk, the regenerated matrix lines), read-only, run
# in the review clone with bytecode writes disabled.
# Usage: run_gates.sh <clone-dir> <pinned-verilator-dir>
set -u
C=${1:?clone}; VDIR=${2:?dir holding the pinned verilator}
cd "$C" || exit 2
export PYTHONDONTWRITEBYTECODE=1 PATH="$VDIR:$PATH"
BASE=ede8d48ecd7c7f589a14b957951f040d92c99c70
run() {
  echo "===== $*"
  out=$("$@" 2>&1); rc=$?
  printf '%s\n' "$out" | tail -n 12
  echo "rc=$rc"
}
echo "verilator: $(verilator --version)"
run python3 scripts/docs_check.py
run python3 scripts/check_em_dash.py --base "$BASE"
run python3 scripts/check_em_dash.py --base 553edeb86b9144f7b15721255fbe5ad11ef1fe36
run python3 scripts/check_doc_style.py
run python3 scripts/gen_toc.py --check
run python3 scripts/gen_toc.py --verify-anchors
run python3 docs/traceability/gen_module_matrix.py --check
run python3 scripts/check_doc_paths.py
run python3 scripts/check_hygiene.py --check
run python3 scripts/check_sv_idiom.py
run python3 scripts/measure_naming.py --check
run python3 scripts/check_port_contracts.py
run python3 scripts/check_todo_ownership.py
run python3 scripts/lint_rtl.py --check
echo "===== git diff --check $BASE HEAD"; git diff --check "$BASE" HEAD; echo "rc=$?"
echo "===== git diff --check HEAD~1 HEAD"; git diff --check HEAD~1 HEAD; echo "rc=$?"
