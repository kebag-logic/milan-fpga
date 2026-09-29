#!/usr/bin/env bash
# Run the documentation and scope gates the lane claims, at the reviewed head, in the
# pinned Markdown environment. usage: run_gates.sh <repo-root> <python-with-pinned-markdown-lock>
# check_baremetal_only needs PyYAML, which the Markdown lock does not carry: it runs with python3.
# Prints each command, its full output and its exit status; sequential, foreground.
set -u
R=$1; PY=$2
cd "$R" || exit 2
echo "HEAD $(git rev-parse HEAD) TREE $(git rev-parse HEAD^{tree})"
"$PY" -m pip freeze 2>/dev/null | sed 's/^/env: /'
run() {
  echo "=== $*"
  "$@"
  echo "=== rc=$? : $*"
}
run "$PY" -B scripts/docs_check.py
run "$PY" -B scripts/check_doc_style.py
run "$PY" -B scripts/gen_toc.py --check
run "$PY" -B scripts/check_em_dash.py --base 13eda870d1a6cf3f946fc228a98862366b08d102
run "$PY" -B scripts/check_em_dash.py --selftest
run "$PY" -B scripts/check_doc_paths.py
run "$PY" -B scripts/ci_scope.py --selftest
run python3 -B scripts/check_baremetal_only.py --check
run "$PY" -B scripts/check_feature_status.py --self-test
run git diff --check 13eda870d1a6cf3f946fc228a98862366b08d102 HEAD
run git diff --check f9eab5bf55ca4471e6e48ae3d38018d7e804505b HEAD
run git status --porcelain --untracked-files=all
