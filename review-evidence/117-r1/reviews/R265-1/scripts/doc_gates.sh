#!/usr/bin/env bash
# Run the documentation gates relevant to a docs-only change in a disposable
# checkout at the exact head (the published gate transcript's five plus the
# docs-workflow steps the hosted job never reached after its failing step).
# usage: scripts/doc_gates.sh <disposable checkout at 0abf147f>
set -uo pipefail
cd "$1"
echo "head $(git rev-parse HEAD)"
while read -r g; do
  echo "== python3 $g"
  out=$(python3 $g 2>&1); rc=$?
  printf '%s\n' "$out" | tail -3
  echo "rc=$rc"
done <<'LIST'
scripts/docs_check.py
scripts/check_doc_style.py
scripts/gen_toc.py --check
scripts/gen_toc.py --verify-anchors
scripts/gen_toc.py --selftest
scripts/check_em_dash.py --base ede8d48ecd7c7f589a14b957951f040d92c99c70
scripts/check_baremetal_only.py --check
scripts/check_baremetal_only.py --selftest
scripts/check_doc_paths.py
scripts/check_archive.py
scripts/check_feature_status.py
docs/DOC_MAP.gen.py --check
scripts/check_solution_docs.py
LIST
