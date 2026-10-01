#!/usr/bin/env bash
# Run the documentation gates for PR #627 at the checked-out head (round R422-3).
# usage: run_docs_gates.sh <repo> <python-with-pinned-markdown-lock-and-pyyaml> <receipt-dir>
set -u
repo=$1 py=$2 out=$3
mkdir -p "$out"
cd "$repo" || exit 2
export PYTHONDONTWRITEBYTECODE=1
summary="$out/gates-summary.txt"
: > "$summary"
printf 'head %s tree %s\n' "$(git rev-parse HEAD)" "$(git rev-parse 'HEAD^{tree}')" >> "$summary"
n=0
run() {
  n=$((n + 1))
  "$@" > "$out/gate-$n.txt" 2>&1
  rc=$?
  printf 'gate-%d rc=%d: %s\n' "$n" "$rc" "$*" >> "$summary"
}
run "$py" scripts/docs_check.py
run "$py" scripts/check_doc_style.py
run "$py" scripts/gen_toc.py --check
run "$py" scripts/gen_toc.py --verify-anchors
run "$py" scripts/check_em_dash.py --base e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b
run "$py" scripts/check_em_dash.py --base c39312b4871c8cc3ca604eb7c57f4b0b45d914e0
run "$py" scripts/check_doc_paths.py
run "$py" scripts/ci_scope.py --selftest
run "$py" scripts/check_baremetal_only.py --check
run "$py" scripts/check_feature_status.py --self-test
run git diff --check e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b HEAD
run git diff --check c39312b4871c8cc3ca604eb7c57f4b0b45d914e0 HEAD

sed -i "s#$(dirname "$py")/#<python-env>/#" "$summary"
cat "$summary"
