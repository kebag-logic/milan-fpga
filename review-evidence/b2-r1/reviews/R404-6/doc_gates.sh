#!/usr/bin/env bash
# Run the repository's documentation gates at the checked-out head.
# Usage: doc_gates.sh <repo> <python-with-cmarkgfm-2025.10.22-and-html5lib-1.1>
set -u
R=$1; PY=$2
cd "$R"
echo "head $(git rev-parse HEAD) tree $(git rev-parse HEAD^{tree})"
"$PY" -c "import cmarkgfm,html5lib,importlib.metadata as m;print('cmarkgfm',m.version('cmarkgfm'),'html5lib',m.version('html5lib'))"
run() { echo "### $*"; "$@"; echo "rc=$?"; }
run "$PY" scripts/docs_check.py
run "$PY" scripts/check_doc_style.py
run "$PY" scripts/gen_toc.py --check
run "$PY" scripts/check_em_dash.py --base 79c36963660c10e4c1c11a744fb5bff41a552b8b
run "$PY" scripts/check_em_dash.py --base 13eda870d1a6cf3f946fc228a98862366b08d102
run "$PY" scripts/check_doc_paths.py
run "$PY" scripts/ci_scope.py --selftest
run "$PY" scripts/check_baremetal_only.py --check
run "$PY" scripts/check_feature_status.py --self-test
echo "### git diff --check 79c36963..HEAD"; git diff --check 79c36963660c10e4c1c11a744fb5bff41a552b8b HEAD; echo "rc=$?"
echo "### git diff --check 5c579274..HEAD"; git diff --check 5c57927413e0dae279f06a75d2a58e3fec8a2bb0 HEAD; echo "rc=$?"
echo "### worktree clean"; git status --porcelain --untracked-files=all | head; echo "end"
