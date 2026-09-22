#!/usr/bin/env bash
# Core #464 gates at the committed head of the lane checkout. Read-only on
# tracked state (bytecode writing disabled); prints one verdict line per gate.
#   final_head_gates.sh <checkout> <base> [python3.12]
set -uo pipefail
cd "$1" || exit 2
base=$2; py312=${3:-}
export PYTHONDONTWRITEBYTECODE=1
echo "head $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}') base $base"
[ -z "$(git status --porcelain --ignored)" ] && echo "lane pristine before gates" || echo "LANE NOT PRISTINE"
run() {
  out=$("$@" 2>&1); rc=$?
  printf '%-58s exit=%s | %s\n' "$*" "$rc" "$(printf '%s\n' "$out" | grep -v '^[[:space:]]*$' | tail -1 | cut -c1-120)"
}
run python3 -B avdecc/gen_aem_store.py --self-test
[ -n "$py312" ] && run "$py312" -B avdecc/gen_aem_store.py --self-test
run python3 -B scripts/ci_events.py --check
run python3 -B scripts/ci_events.py --selftest
run python3 -B scripts/docs_check.py
run python3 -B scripts/check_doc_paths.py
run python3 -B scripts/gen_toc.py --check
run python3 -B scripts/check_em_dash.py --base "$base"
run python3 -B scripts/check_feature_status.py
run python3 -B scripts/check_py_idiom.py
run python3 -B scripts/check_hygiene.py --check
run git diff --check "$base" HEAD
[ -z "$(git status --porcelain --ignored)" ] && echo "lane pristine after gates" || echo "LANE NOT PRISTINE"
