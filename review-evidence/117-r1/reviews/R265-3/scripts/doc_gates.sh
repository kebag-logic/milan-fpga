#!/usr/bin/env bash
# Run the documentation gates relevant to a docs-only change, from the repository root.
# Usage: doc_gates.sh <repo> <out-dir> <base-rev>
set -u
repo=$1 out=$2 base=$3
cd "$repo" || exit 2
run() {
  local name=$1; shift
  local log="$out/$name.txt"
  { echo "\$ $*"; timeout 600 "$@"; echo "exit=$?"; } >"$log" 2>&1
  printf '%-40s %s\n' "$name" "$(tail -1 "$log")"
}
run docs_check python3 scripts/docs_check.py
run check_em_dash python3 scripts/check_em_dash.py --base "$base"
run check_doc_style python3 scripts/check_doc_style.py
run check_gptp_docs python3 scripts/check_gptp_docs.py
run check_baremetal_only python3 scripts/check_baremetal_only.py --check
run gen_toc_check python3 scripts/gen_toc.py --check
run gen_toc_verify_anchors python3 scripts/gen_toc.py --verify-anchors
run check_archive python3 scripts/check_archive.py
run check_hygiene python3 scripts/check_hygiene.py --check
run check_feature_status python3 scripts/check_feature_status.py
run check_solution_docs python3 scripts/check_solution_docs.py
run check_submodule_docs python3 scripts/check_submodule_docs.py
run doc_map_check python3 docs/DOC_MAP.gen.py --check
run check_todo_ownership python3 scripts/check_todo_ownership.py
if [ -f scripts/check_doc_paths.py ]; then run check_doc_paths python3 scripts/check_doc_paths.py; fi
