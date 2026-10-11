#!/usr/bin/env bash
# Run the documentation and record gates that read the composed files, on the
# candidate tree, recording each command's output and exit code.
# Usage: run_gates.sh <candidate-clone> <receipt-dir> <python-with-pinned-markdown-renderer>
set -u
clone="$1"; out="$2"; py="$3"
mkdir -p "$out"
cd "$clone" || exit 2
run() {
    local name="$1"; shift
    { echo "\$ $*"; "$@"; } >"$out/$name.log" 2>&1
    local rc=$?
    echo "$rc" >"$out/$name.rc"
    printf '%-36s rc=%s\n' "$name" "$rc"
}
run docs_check            "$py" -I scripts/docs_check.py
run gen_toc_check         "$py" -I scripts/gen_toc.py --check
run gen_toc_anchors       "$py" -I scripts/gen_toc.py --verify-anchors
run em_dash_vs_dev        "$py" -I scripts/check_em_dash.py --base ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5
run em_dash_vs_srcbase    "$py" -I scripts/check_em_dash.py --base e8454e2751d05b02ee8e5a571857589ab358ab86
run em_dash_selftest      "$py" -I scripts/check_em_dash.py --selftest
run doc_style             "$py" -I scripts/check_doc_style.py
run doc_paths             "$py" -I scripts/check_doc_paths.py
# ci_events needs pyyaml, which the pinned renderer environment does not carry.
run ci_events_check       python3 -I scripts/ci_events.py --check
run ci_scope_selftest     "$py" -I scripts/ci_scope.py --selftest
run test_evidence_check   "$py" -I scripts/measure_test_evidence.py --check
run doc_map_check         "$py" -I docs/DOC_MAP.gen.py --check
git -C "$clone" status --porcelain >"$out/status_after.txt"
git -C "$clone" rev-parse HEAD 'HEAD^{tree}' >"$out/head_after.txt"
