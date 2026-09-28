#!/usr/bin/env bash
# The pinned Markdown gates, run in one tree. Usage: docs_gates.sh <tree> <base-sha>
set -uo pipefail
cd "$1"; base=$2
for g in "scripts/docs_check.py" "scripts/check_em_dash.py --base $base" "scripts/check_doc_style.py" \
         "scripts/gen_toc.py --check" "scripts/gen_toc.py --verify-anchors" "scripts/check_doc_paths.py"; do
  echo "== $g"; python3 -B $g 2>&1 | tail -3; echo "rc=${PIPESTATUS[0]} $g"
done
echo "== GIT_DIR=/dev/null scripts/docs_check.py"
GIT_DIR=/dev/null python3 -B scripts/docs_check.py 2>&1 | tail -3; echo "rc=${PIPESTATUS[0]} GIT_DIR=/dev/null docs_check"
