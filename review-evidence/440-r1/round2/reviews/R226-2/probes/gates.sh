#!/usr/bin/env bash
# R226-2 focused gates in a scratch clone (never the review clone). Each command's
# stdout+stderr and exit status are recorded; nothing is written to tracked files.
set -uo pipefail
tree=${1:?scratch clone}
base=${2:?base rev}
cd "$tree"
export PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0
run() {
  echo "\$ $*"
  "$@" 2>&1 | tail -n 25
  echo "exit=${PIPESTATUS[0]}"
  echo
}
echo "tree: $(git rev-parse HEAD) $(git rev-parse 'HEAD^{tree}')"
echo "merge-base(base, HEAD): $(git merge-base "$base" HEAD)"
echo
run python3 -B scripts/gen_toc.py --selftest
run python3 -B scripts/gen_toc.py --check
run python3 -B scripts/gen_toc.py --verify-anchors
run python3 -B scripts/gen_toc.py --sites
run python3 -B scripts/check_em_dash.py --selftest
run python3 -B scripts/check_em_dash.py --base "$(git merge-base "$base" HEAD)"
run python3 -B scripts/docs_check.py
run python3 -B scripts/check_doc_style.py
run python3 -B scripts/check_doc_paths.py
run git diff --check "$base" HEAD
run git diff --check 0d43ff25d38917e77bb5c3d2ddb6473013cea3ba HEAD
echo "status after gates:"
git status --porcelain=v2 --untracked-files=all --ignored | head -20
echo "(end)"
