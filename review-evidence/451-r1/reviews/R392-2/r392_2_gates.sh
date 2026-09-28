#!/usr/bin/env bash
# Reviewer gate runner (R392-2). Runs the documentation and scope gates at the
# checked-out head, one receipt per gate, unpiped, return code recorded.
# Usage: r392_2_gates.sh <clone> <pinned-markdown-python> <receipt-dir>
set -u
clone=$1; py=$2; out=$3
base=6d5ebd7357c1e468e446f18a61527c5be6118a04
head=$(git -C "$clone" rev-parse HEAD)
mkdir -p "$out"
i=0
run() {
  i=$((i + 1))
  local shown=${*//$py/<pinned-markdown-python>}
  { echo "\$ $shown"; (cd "$clone" && PYTHONDONTWRITEBYTECODE=1 "$@") 2>&1; echo "rc=$?"; } > "$out/gate-$i.txt"
  tail -1 "$out/gate-$i.txt" | sed "s|^|gate-$i $1 ${2:-} ${3:-}: |"
}
run "$py" scripts/docs_check.py
run "$py" scripts/check_doc_style.py
run "$py" scripts/gen_toc.py --check
run "$py" scripts/check_em_dash.py --base "$base"
run "$py" scripts/check_em_dash.py --selftest
run "$py" scripts/check_doc_paths.py
run "$py" scripts/ci_scope.py --selftest
run "$py" scripts/check_baremetal_only.py --check
run git diff --check "$base" "$head"
run git diff --check
run "$py" scripts/check_feature_status.py
run "$py" scripts/gen_toc.py --verify-anchors
run "$py" scripts/check_archive.py
run "$py" scripts/check_hygiene.py --check
run "$py" scripts/check_gptp_docs.py
run "$py" scripts/check_solution_docs.py
run "$py" docs/DOC_MAP.gen.py --check
