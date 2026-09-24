#!/usr/bin/env bash
# R269-3: focused, read-only gates relevant to the PR #534 diff, run in the
# exact-head clone. Each gate's command, exit status and tail go to one receipt.
# usage: focused_gates.sh <clone> <receipt> ; VERILATOR must be the pinned 5.050
set -u
clone=$1 out=$2
cd "$clone" || exit 90
export PATH="$(dirname "${VERILATOR:?}"):$PATH"
: > "$out"
run() {
  printf '### %s\n' "$*" >> "$out"
  "$@" > "$out.tmp" 2>&1
  rc=$?
  tail -n 6 "$out.tmp" >> "$out"
  printf 'exit=%s\n\n' "$rc" >> "$out"
  rm -f "$out.tmp"
}
run python3 scripts/docs_check.py
run python3 scripts/check_em_dash.py --base ede8d48ecd7c7f589a14b957951f040d92c99c70
run python3 scripts/check_doc_style.py
run python3 scripts/check_cpp_idiom.py
run python3 scripts/check_sv_idiom.py
run python3 scripts/measure_naming.py --check
run python3 scripts/measure_test_evidence.py --check
run python3 scripts/check_hygiene.py --check
run python3 scripts/check_rtl_source_lists.py
run python3 scripts/lint_rtl.py --check
run python3 docs/traceability/gen_module_matrix.py --check
{ echo "### git status --porcelain after the gates"; git status --porcelain; echo "(end)"; } >> "$out"
