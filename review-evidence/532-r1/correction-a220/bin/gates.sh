#!/usr/bin/env bash
# [A220] Offline gates at the lane head (clean tree). No Docker, act, sudo,
# privilege or host network. The candidate runner's own --selftest is NOT run
# here; see run-selftest-sandbox.sh (runner-change bootstrap rule).
# Usage: gates.sh LANE
set -uo pipefail
cd "$1" || exit 2
echo "head $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}') dirty=$(git status --porcelain | wc -l)"
run() {
  local out rc
  out=$("$@" 2>&1)
  rc=$?
  printf '== rc=%s :: %s\n' "$rc" "$*"
  printf '%s\n' "$out" | tail -n 3 | sed 's/^/   | /'
}
run python3 scripts/check_baremetal_only.py --check
run python3 scripts/check_baremetal_only.py --selftest
run python3 scripts/docs_check.py
run python3 scripts/check_em_dash.py --base 759da623
run python3 scripts/check_py_idiom.py
run python3 scripts/check_sh_idiom.py
run python3 scripts/gen_toc.py --check
run python3 scripts/check_doc_paths.py
run python3 scripts/check_doc_style.py
run bash -n scripts/act_slot_proof.sh
run git diff --check 759da623 HEAD
run git diff --check f5497170 HEAD
echo "commits since f5497170 (subject lines; body lines beyond the subject):"
git rev-list f5497170..HEAD | while read -r commit; do
  printf '  %s body-lines=%s %s\n' "${commit:0:8}" "$(git log -1 --format=%B "$commit" | sed '/^$/d' | tail -n +2 | wc -l)" "$(git log -1 --format=%s "$commit")"
done
