#!/usr/bin/env bash
# R300-4 static/documentation gates at the exact head.
# Usage: run_static.sh <clone> <packet>
# Writes one receipt per command (stdout+stderr, rc) under <packet>/receipts/static/.
set -u
CLONE=${1:?clone}
PKT=${2:?packet}
OUT="$PKT/receipts/static"
mkdir -p "$OUT"
cd "$CLONE" || exit 2
echo "head $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}')" > "$OUT/HEAD.txt"

run() {
  local name=$1; shift
  { echo "\$ $*"; "$@"; echo "rc=$?"; } > "$OUT/$name.txt" 2>&1
  tail -n 1 "$OUT/$name.txt" | sed "s/^/$name: /"
}

run measure_test_evidence_check   python3 scripts/measure_test_evidence.py --check
run measure_test_evidence_selftest python3 scripts/measure_test_evidence.py --selftest
run docs_check_git                python3 -B scripts/docs_check.py
run gen_toc_check                 python3 scripts/gen_toc.py --check
run gen_toc_verify_anchors        python3 scripts/gen_toc.py --verify-anchors
run check_em_dash_base_dev        python3 scripts/check_em_dash.py --base 5c78ce2e9d831e588e759b696ed549804327e4d8
run check_doc_style               python3 scripts/check_doc_style.py
run check_doc_paths               python3 scripts/check_doc_paths.py
run check_py_idiom                python3 scripts/check_py_idiom.py
run diff_check_dev_head           git diff --check 5c78ce2e9d831e588e759b696ed549804327e4d8 HEAD

# No-Git mode: exact committed tree without Git metadata or submodule content,
# as the hosted docs-check-no-git job sees it after checkout and rm -rf .git.
NG="$PKT/scratch/nogit-tree"
rm -rf "$NG"; mkdir -p "$NG"
git archive --format=tar HEAD | tar -x -C "$NG"
( cd "$NG" && { echo "\$ python3 -B scripts/docs_check.py (no .git)"; test ! -e .git && echo "no .git present"; python3 -B scripts/docs_check.py; echo "rc=$?"; } ) > "$OUT/docs_check_nogit.txt" 2>&1
tail -n 1 "$OUT/docs_check_nogit.txt" | sed "s/^/docs_check_nogit: /"
