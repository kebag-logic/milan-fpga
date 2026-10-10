#!/usr/bin/env bash
# Focused documentation gates for the pages this round changed.
# Usage: docs_subset.sh <tree> <receipt-dir>
# One log and rc file per command; the tree is checked for modification afterwards.
set -u
T=$1
R=$2
mkdir -p "$R"
cd "$T" || exit 2
CMDS=(
  "python3 scripts/docs_check.py"
  "python3 scripts/check_em_dash.py --base 8b61b70902f3ebf118e56967277e2686731081bd"
  "python3 scripts/check_em_dash.py --base 030eb98a12685a2ca41cf8d785bb0eb69dc32a98"
  "python3 scripts/check_doc_style.py"
  "python3 docs/DOC_MAP.gen.py --check"
  "python3 scripts/check_feature_status.py --self-test"
  "python3 docs/traceability/gen_module_matrix.py --check"
  "python3 scripts/gen_toc.py --check"
  "python3 scripts/check_solution_docs.py"
)
i=0
for c in "${CMDS[@]}"; do
  i=$((i+1)); n=$(printf '%02d' "$i")
  echo "$c" > "$R/$n.cmd"
  # shellcheck disable=SC2086
  timeout 900 $c > "$R/$n.log" 2>&1
  echo $? > "$R/$n.rc"
  printf '%s rc=%s  %s\n' "$n" "$(cat "$R/$n.rc")" "$c"
done
echo "tree status after:"
git status --porcelain
