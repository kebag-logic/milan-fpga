#!/bin/sh
# Light static/docs gates in the exact-head clone (read-only), each rc recorded.
set -u
. "$(dirname "$0")/env.sh"
cd "$CLONE"
echo "HEAD $(git rev-parse HEAD)"
run() { echo "=== $*"; "$@"; echo "rc=$?"; }
run python3 scripts/docs_check.py
run python3 scripts/check_em_dash.py --base f86c34fe2ddbc6cfb7c8c70ddbe0d9726f4d3c2f
run python3 scripts/check_doc_style.py
run python3 scripts/check_doc_paths.py
run python3 scripts/gen_toc.py --check
run python3 scripts/check_rtl_source_lists.py
run python3 scripts/check_sv_idiom.py
run python3 scripts/check_cpp_idiom.py
run git diff --check f86c34fe2ddbc6cfb7c8c70ddbe0d9726f4d3c2f HEAD
echo "=== status after gates"; git status --porcelain; echo "status-lines=$(git status --porcelain | wc -l)"
