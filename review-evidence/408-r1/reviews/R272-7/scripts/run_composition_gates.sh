#!/usr/bin/env bash
# Run the static gates that read the files PR #535 composes with live dev.
# Usage: run_composition_gates.sh <candidate-clone> <python> <receipt-dir>
# Each gate's stdout+stderr goes to <receipt-dir>/<name>.log and its exit
# code to <receipt-dir>/gates.tsv. The clone is only read.
set -u
clone=$1 py=$2 out=$3
mkdir -p "$out"
export PYTHONDONTWRITEBYTECODE=1
cd "$clone" || exit 2
parent=573f0052a0e4412e81f0845438fcec2086ce5d55
mbase=$(git merge-base "$parent" 062e89ad098806ae5def8341fcb8c2815583ca00)
: > "$out/gates.tsv"
run() {
    name=$1; shift
    start=$(date +%s)
    "$@" > "$out/$name.log" 2>&1
    rc=$?
    printf '%s\t%s\t%ss\t%s\n' "$name" "$rc" "$(( $(date +%s) - start ))" "$*" \
        >> "$out/gates.tsv"
}
run docs_check            "$py" scripts/docs_check.py
run em_dash_parent        "$py" scripts/check_em_dash.py --base "$parent"
run em_dash_mergebase     "$py" scripts/check_em_dash.py --base "$mbase"
run em_dash_selftest      "$py" scripts/check_em_dash.py --selftest
run doc_style             "$py" scripts/check_doc_style.py
run doc_style_selftest    "$py" scripts/check_doc_style.py --selftest
run gen_toc_selftest      "$py" scripts/gen_toc.py --selftest
run gen_toc_anchors       "$py" scripts/gen_toc.py --verify-anchors
run gen_toc_check         "$py" scripts/gen_toc.py --check
run doc_paths             "$py" scripts/check_doc_paths.py
run doc_map_check         "$py" docs/DOC_MAP.gen.py --check
run module_matrix_check   "$py" docs/traceability/gen_module_matrix.py --check
run feature_status        "$py" scripts/check_feature_status.py
run ci_events_check       "$py" scripts/ci_events.py --check
run ci_events_selftest    "$py" scripts/ci_events.py --selftest
run baremetal_only_check  "$py" scripts/check_baremetal_only.py --check
run baremetal_only_self   "$py" scripts/check_baremetal_only.py --selftest
run py_idiom              "$py" scripts/check_py_idiom.py
run hygiene_check         "$py" scripts/check_hygiene.py --check
run fail_fast_check       "$py" scripts/measure_fail_fast.py --check
run test_evidence_check   "$py" scripts/measure_test_evidence.py --check
run todo_ownership        "$py" scripts/check_todo_ownership.py
run archive_check         "$py" scripts/check_archive.py
run diff_check_parent     git diff --check "$parent" HEAD
run diff_check_mergebase  git diff --check "$mbase" HEAD
cat "$out/gates.tsv"
