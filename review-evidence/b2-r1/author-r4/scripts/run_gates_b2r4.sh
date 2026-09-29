#!/usr/bin/env bash
# [A449] Round 4 of PR #622: the assigned gates at the committed head.
# Usage (from the physical clone directory): run_gates_b2r4.sh <pinned Markdown python> <out dir>
# Each gate runs in the foreground, not piped; its output goes to one file.
set -u
py=$1; out=$2
mkdir -p "$out"
sum="$out/gates.txt"
{
  echo "head $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}')"
  echo "cwd <lanes>/$(basename "$(pwd -P)") (physical path: $([ "$(pwd -P)" = "$(pwd)" ] && echo yes || echo no))"
  echo "pinned python: $("$py" -c 'import sys; print(sys.version.split()[0])'), $("$py" -m pip freeze --all 2>/dev/null | grep -E '^(cmarkgfm|html5lib)==' | tr '\n' ' ')"
  echo "uncommitted entries before: $(git status --porcelain --ignored | wc -l)"
} > "$sum"
worst=0
run() {
  local id=$1 name=$2; shift 2
  "$@" > "$out/gate-$id-$name.txt" 2>&1
  local rc=$?
  echo "$id $name rc=$rc" >> "$sum"
  [ $rc -gt $worst ] && worst=$rc
}
run 1 docs_check "$py" -B scripts/docs_check.py
run 2 check_doc_style "$py" -B scripts/check_doc_style.py
run 3 gen_toc_check "$py" -B scripts/gen_toc.py --check
run 4 check_em_dash "$py" -B scripts/check_em_dash.py --base 13eda870
run 4b check_em_dash_r3 "$py" -B scripts/check_em_dash.py --base fb4a1b89
run 5 check_doc_paths "$py" -B scripts/check_doc_paths.py
run 6 ci_scope_selftest python3 -B scripts/ci_scope.py --selftest
run 7 check_baremetal_only python3 -B scripts/check_baremetal_only.py --check
run 8 check_feature_status python3 -B scripts/check_feature_status.py --self-test
run 9 diff_check_worktree git diff --check
run 9b diff_check_base git diff --check 13eda870 HEAD
run 9c diff_check_r3 git diff --check fb4a1b89 HEAD
echo "uncommitted entries after: $(git status --porcelain --ignored | wc -l)" >> "$sum"
echo "worst rc=$worst" >> "$sum"
exit $worst
