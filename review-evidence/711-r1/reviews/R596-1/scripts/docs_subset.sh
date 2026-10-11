#!/usr/bin/env bash
# Documentation gates relevant to the changed Markdown, diagrams and pin records,
# run in one head checkout ($1) with the pinned Markdown environment's Python ($2).
# One line per command in receipts/docs/subset.tsv: rc, command.
set -uo pipefail
TREE=$1; PY=$2
OUT=$REVIEWS/711-r596-1-packet/receipts/docs
cd "$TREE" || exit 2
: > "$OUT/subset.tsv"
while IFS= read -r cmd; do
  [ -z "$cmd" ] && continue
  name=$(printf '%s' "$cmd" | tr -c 'A-Za-z0-9._-' '_' | cut -c1-90)
  timeout 900 $PY $cmd > "$OUT/subset-$name.log" 2>&1
  printf '%s\t%s\n' "$?" "$cmd" >> "$OUT/subset.tsv"
done <<'LIST'
scripts/check_doc_style.py
scripts/check_doc_style.py --selftest
docs/DOC_MAP.gen.py --check
docs/DOC_MAP.gen.py --selftest
scripts/check_solution_docs.py
scripts/check_solution_docs.py --selftest
scripts/check_diagram_pngs.py --selftest
scripts/check_feature_status.py --self-test
docs/traceability/gen_module_matrix.py --check
scripts/check_nvm_capture.py
scripts/gen_toc.py --selftest
scripts/gen_toc.py --verify-anchors
scripts/gen_toc.py --check
scripts/ci_events.py --check
LIST
cat "$OUT/subset.tsv"
