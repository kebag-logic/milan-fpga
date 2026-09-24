#!/bin/sh
# Run the doc and source-hygiene gates touched by the round-3 delta at the
# exact head, from the detached review clone, without writing bytecode.
# Usage: run_doc_gates.sh <repo>
set -u
REPO=${1:?repo}
cd "$REPO"
export PYTHONDONTWRITEBYTECODE=1
echo "HEAD $(git rev-parse HEAD)"
g() { echo "== $*"; "$@"; echo "rc=$?"; }
g python3 -B scripts/docs_check.py
g python3 -B scripts/check_em_dash.py --base f86c34fe2ddbc6cfb7c8c70ddbe0d9726f4d3c2f
g python3 -B scripts/check_em_dash.py --base 910b4fb5f
g python3 -B scripts/check_doc_style.py
g python3 -B scripts/gen_toc.py --check
g python3 -B scripts/check_doc_paths.py
g python3 -B scripts/check_sv_idiom.py
g python3 -B scripts/check_rtl_source_lists.py
g git diff --check 26d855a9176d63625e6635a029a0c44e3d57ce9a HEAD
g git diff --check 910b4fb5f HEAD
echo "== status after gates"; git status --porcelain --ignored | grep -v '^!! .*__pycache__' ; echo "status_listed"
echo "GATES_DONE"
