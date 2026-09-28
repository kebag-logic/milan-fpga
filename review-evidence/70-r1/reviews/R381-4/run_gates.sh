#!/usr/bin/env bash
# Composition gates for the #70 / PR #610 merge-train candidate.
# Usage: run_gates.sh <candidate-clone> <python-with-locked-markdown-renderer> <receipt-dir>
# Each gate's stdout+stderr goes to <receipt-dir>/gate_<name>.log and its rc to
# <receipt-dir>/gates.tsv. Gates run in the foreground, one at a time.
set -u
repo=$1 py=$2 out=$3
parent1=c1fa4183f99293f8ee0777cda454d9d77855ca09
srcbase=c07232228c12b72805dd20e6852bf93f25794da0
mkdir -p "$out"
cd "$repo" || exit 2
: > "$out/gates.tsv"
run() {
  local name=$1; shift
  "$@" > "$out/gate_$name.log" 2>&1
  local rc=$?
  printf '%s\t%s\t%s\n' "$rc" "$name" "$*" >> "$out/gates.tsv"
}
run docs_check              "$py" scripts/docs_check.py
run check_doc_paths         "$py" scripts/check_doc_paths.py
run check_doc_style         "$py" scripts/check_doc_style.py
run check_doc_style_self    "$py" scripts/check_doc_style.py --selftest
run gen_toc_check           "$py" scripts/gen_toc.py --check
run gen_toc_anchors         "$py" scripts/gen_toc.py --verify-anchors
run gen_toc_self            "$py" scripts/gen_toc.py --selftest
run em_dash_parent1         "$py" scripts/check_em_dash.py --base "$parent1"
run em_dash_srcbase         "$py" scripts/check_em_dash.py --base "$srcbase"
run em_dash_self            "$py" scripts/check_em_dash.py --selftest
run doc_map_check           "$py" docs/DOC_MAP.gen.py --check
run feature_status          "$py" scripts/check_feature_status.py
run solution_docs           "$py" scripts/check_solution_docs.py
run baremetal_only          "$py" scripts/check_baremetal_only.py --check
run baremetal_only_self     "$py" scripts/check_baremetal_only.py --selftest
run nvm_record_space        "$py" scripts/check_nvm_record_space.py
run ci_scope_self           "$py" scripts/ci_scope.py --selftest
run ci_events_check         "$py" scripts/ci_events.py --check
run ci_events_self          "$py" scripts/ci_events.py --selftest
run todo_ownership          "$py" scripts/check_todo_ownership.py
run hygiene                 "$py" scripts/check_hygiene.py --check
run test_evidence           "$py" scripts/measure_test_evidence.py --check
run archive                 "$py" scripts/check_archive.py
run diff_check_parent1      git -c core.commitGraph=false diff --check "$parent1" HEAD
run diff_check_srcbase      git -c core.commitGraph=false diff --check "$srcbase" HEAD
cat "$out/gates.tsv"
