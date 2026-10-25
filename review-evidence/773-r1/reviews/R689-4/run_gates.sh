#!/usr/bin/env bash
# Run the composition gates on the candidate clone concurrently; one log and rc per gate.
set -u
PY=${PY:-python3}
REPO=${1:?repo}; OUT=${2:?outdir}; BASE=${3:?base}
cd "$REPO" || exit 2
mkdir -p "$OUT"
run() { local n=$1; shift; ( "$@" >"$OUT/$n.log" 2>&1; echo $? >"$OUT/$n.rc" ) & }
run docs_check            "$PY" scripts/docs_check.py
run gen_toc_check         "$PY" scripts/gen_toc.py --check --verify-anchors
run em_dash               "$PY" scripts/check_em_dash.py --base "$BASE"
run ci_events_check       "$PY" scripts/ci_events.py --check
run ci_events_selftest    "$PY" scripts/ci_events.py --selftest
run suite_shards_selftest "$PY" scripts/suite_shards.py --selftest
run ci_gate_workflows     "$PY" scripts/ci_gate_workflows.py --check
run ci_gate_wf_selftest   "$PY" scripts/ci_gate_workflows_selftest.py
run doc_paths             "$PY" scripts/check_doc_paths.py
run doc_style             "$PY" scripts/check_doc_style.py
run measure_evidence_chk  "$PY" scripts/measure_test_evidence.py --check
run measure_evidence_self "$PY" scripts/measure_test_evidence.py --selftest
run em_dash_selftest      "$PY" scripts/check_em_dash.py --selftest
run docs_check_selftest   "$PY" scripts/docs_check.py --selftest
wait
for f in "$OUT"/*.rc; do printf '%-24s rc=%s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done
