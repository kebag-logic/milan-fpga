#!/usr/bin/env bash
# Run the focused source-head gates for PR #735 concurrently; one log + rc per gate.
# Usage: run_gates.sh <candidate-checkout> <out-dir> <python-with-yaml-and-markdown>
set -u
cand="$1"; out="$2"; py="$3"
mkdir -p "$out"
export PYTHONDONTWRITEBYTECODE=1
run() { # name, then command (run inside $cand)
  local name="$1"; shift
  ( cd "$cand" && "$@" ) >"$out/$name.log" 2>&1; echo $? >"$out/$name.rc"
}
run ci_scope-selftest        "$py" scripts/ci_scope.py --selftest &
run ci_events-check          "$py" scripts/ci_events.py --check &
run ci_events-selftest       "$py" scripts/ci_events.py --selftest &
run docs_check               "$py" scripts/docs_check.py &
run docs_check-selftest      "$py" scripts/docs_check.py --selftest &
run check_doc_paths          "$py" scripts/check_doc_paths.py &
run check_doc_style          "$py" scripts/check_doc_style.py &
run gen_toc-check            "$py" scripts/gen_toc.py --check &
run gen_toc-selftest         "$py" scripts/gen_toc.py --selftest &
run gen_toc-anchors          "$py" scripts/gen_toc.py --verify-anchors &
run em_dash-base             "$py" scripts/check_em_dash.py --base a0f39ad4f4bfc9ed4805bac049c4f2b926a94ec0 &
run em_dash-selftest         "$py" scripts/check_em_dash.py --selftest &
run py_idiom                 "$py" scripts/check_py_idiom.py &
run py_idiom-selftest        "$py" scripts/check_py_idiom.py --selftest &
run sh_idiom                 "$py" scripts/check_sh_idiom.py &
run sh_idiom-selftest        "$py" scripts/check_sh_idiom.py --selftest &
wait
run measure_evidence         "$py" scripts/measure_test_evidence.py --check &
run measure_evidence-selftest "$py" scripts/measure_test_evidence.py --selftest &
wait
