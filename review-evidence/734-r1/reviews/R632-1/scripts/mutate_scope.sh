#!/usr/bin/env bash
# Reviewer mutation probes for PR #735. Usage: mutate_scope.sh <source-clone> <workdir> <receipts>
# Each arm: a disposable clone at the reviewed head, one textual edit, then
# `ci_scope.py --selftest` and `ci_events.py --check`; rc of each recorded.
set -euo pipefail
src=$1; work=$2; out=$3
head=0519ff3684258482a56892056edbfbb65c186f88
mkdir -p "$work" "$out"

arm() {  # name file python-replacement-expression
  local name=$1 file=$2 old=$3 new=$4 dir="$work/$1"
  rm -rf "$dir"
  git clone --quiet --shared --no-checkout "$src" "$dir"
  git -C "$dir" -c advice.detachedHead=false checkout --quiet "$head"
  OLD=$old NEW=$new python3 - "$dir/$file" <<'PY'
import os, sys
p = sys.argv[1]; t = open(p).read(); o = os.environ["OLD"]; n = os.environ["NEW"]
c = t.count(o)
assert c >= 1, f"anchor missing in {p}: {o!r}"
open(p, "w").write(t.replace(o, n, 1))
PY
  ( set +e; cd "$dir" && python3 scripts/ci_scope.py --selftest > "$out/$name.scope.log" 2>&1; echo $? > "$out/$name.scope.rc" ) &
  ( set +e; cd "$dir" && python3 scripts/ci_events.py --check > "$out/$name.events.log" 2>&1; echo $? > "$out/$name.events.rc" ) &
}

for wf in rtl elaborate; do
  arm "$wf-two-dot-merge" ".github/workflows/$wf.yml" '"$PR_BASE_SHA...$PR_HEAD_SHA"' '"$PR_BASE_SHA" "$GITHUB_SHA"'
  arm "$wf-head-bound-github-sha" ".github/workflows/$wf.yml" 'PR_HEAD_SHA: ${{ github.event.pull_request.head.sha }}' 'PR_HEAD_SHA: ${{ github.sha }}'
  arm "$wf-three-dot-merge-commit" ".github/workflows/$wf.yml" '"$PR_BASE_SHA...$PR_HEAD_SHA"' '"$PR_BASE_SHA...$GITHUB_SHA"'
done
arm fast-two-dot-merge .github/workflows/rtl-fast.yml '"$base...$PR_HEAD_SHA"' '"$base" "$GITHUB_SHA"'
arm fast-head-bound-github-sha .github/workflows/rtl-fast.yml 'PR_HEAD_SHA: ${{ github.event.pull_request.head.sha }}' 'PR_HEAD_SHA: ${{ github.sha }}'
arm fast-push-three-dot .github/workflows/rtl-fast.yml '"$base" "$GITHUB_SHA"' '"$base...$GITHUB_SHA"'
arm rtl-shallow .github/workflows/rtl.yml 'fetch-depth: 0' 'fetch-depth: 1'
arm fast-shallow .github/workflows/rtl-fast.yml 'fetch-depth: 0' 'fetch-depth: 1'
arm elab-shallow .github/workflows/elaborate.yml 'fetch-depth: 0' 'fetch-depth: 1'
arm scope-history-unwired scripts/ci_scope.py 'failures += history_selftest(ROOT)' 'failures += 0'
arm classifier-hdl-docs scripts/ci_scope.py 'DOC_PREFIXES = ["LICENSES/"]' 'DOC_PREFIXES = ["LICENSES/", "hdl/"]'
arm classifier-no-gitlink scripts/ci_scope.py 'is_submodule_path(clean) or ' ''
arm classifier-empty-docs scripts/ci_scope.py 'not changed or ' ''
wait
for f in "$out"/*.scope.rc; do
  n=$(basename "$f" .scope.rc)
  printf '%-30s ci_scope_selftest_rc=%s ci_events_check_rc=%s\n' "$n" "$(cat "$f")" "$(cat "$out/$n.events.rc")"
done
