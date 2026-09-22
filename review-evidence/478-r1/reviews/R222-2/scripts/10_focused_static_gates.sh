#!/usr/bin/env bash
# Focused fast static gates at the exact head in the initialized scratch clone
# (not the full builder, not RTL/Yosys/processor/native suites, and never the
# candidate's act_ci.py). Covers the documentation, idiom and hygiene gates
# that read the three changed files. Scratch only; the clone must stay clean.
set -uo pipefail
S=${SCRATCH:-/tmp/r222-478-r2-scratch}
D="$S/git-sub"
BASE=88e9276b2a220c716f64a843f7e1eb8f9265e896
echo "head=$(git -C "$D" rev-parse HEAD) submodules: $(git -C "$D" submodule status | cut -c1 | tr -d '\n')"
fail=0
step() {
  local out rc
  out=$(cd "$D" && "$@" 2>&1); rc=$?
  [ $rc -eq 0 ] || fail=$((fail+1))
  printf 'exit %-3s %s\n' "$rc" "$*"
  printf '%s\n' "$out" | tail -2 | sed 's/^/        | /'
}
step python3 scripts/docs_check.py
step python3 scripts/check_doc_paths.py
step python3 scripts/check_doc_style.py
step python3 scripts/gen_toc.py --selftest
step python3 scripts/gen_toc.py --verify-anchors
step python3 scripts/gen_toc.py --check
step python3 scripts/check_archive.py
step python3 scripts/check_em_dash.py --base "$BASE"
step python3 scripts/check_em_dash.py --selftest
step python3 scripts/check_py_idiom.py
step python3 scripts/check_hygiene.py --check
step python3 scripts/check_todo_ownership.py
step python3 scripts/pp_srcs.py --check
step python3 scripts/check_feature_status.py
step git diff --check "$BASE" HEAD
echo "non-zero steps: $fail"
echo "clone status lines after run: $(git -C "$D" status --porcelain --untracked-files=all | wc -l)"
git -C "$D" status --porcelain --untracked-files=all | head
