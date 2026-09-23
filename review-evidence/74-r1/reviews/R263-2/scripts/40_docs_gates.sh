#!/bin/sh
# Docs-lens gates at the exact head, read-only modes only, no bytecode caches.
# Usage: 40_docs_gates.sh <clone>
set -u
clone=$1
cd "$clone"
BASE=ede8d48ecd7c7f589a14b957951f040d92c99c70
OLD=553edeb86b9144f7b15721255fbe5ad11ef1fe36
export PYTHONDONTWRITEBYTECODE=1
run() {
  echo "== $*"
  "$@" > /tmp/r263-2-gate.$$ 2>&1
  rc=$?
  tail -6 /tmp/r263-2-gate.$$ | sed 's/^/  /'
  echo "  rc=$rc"
  rm -f /tmp/r263-2-gate.$$
}
echo "HEAD $(git rev-parse HEAD)"
run python3 -B scripts/docs_check.py
run python3 -B scripts/check_doc_style.py
run python3 -B scripts/gen_toc.py --check
run python3 -B scripts/gen_toc.py --verify-anchors
run python3 -B scripts/check_em_dash.py --base "$BASE"
run python3 -B scripts/check_em_dash.py --base "$OLD"
run python3 -B docs/traceability/gen_module_matrix.py --check
run git diff --check "$BASE" HEAD
run git diff --check "$OLD" HEAD
echo "== U+2014 in lines ADDED by $OLD..HEAD (any file)"
n=$(git diff -U0 "$OLD" HEAD | grep '^+' | grep -v '^+++' | grep -c "$(printf '\342\200\224')" || true)
echo "  $n"
echo "== added-line count by file, $OLD..HEAD"
git diff --numstat "$OLD" HEAD | sed 's/^/  /'
