#!/bin/sh
# Re-run the composition gates of review R747-3 on a clone at the candidate.
# Usage: composition_gates.sh <clone> <receipt-dir> <md-python> <full-python>
# <md-python> carries only the pinned Markdown renderer (tools/markdown/requirements.txt);
# <full-python> carries that renderer plus PyYAML.
set -u
C=$1; R=$2; PY=$3; PY2=$4; mkdir -p "$R"; cd "$C" || exit 2
run() { n=$1; shift; ( timeout 590 "$@" > "$R/$n.log" 2>&1; echo $? > "$R/$n.rc" ) & }
run docs_check python3 scripts/docs_check.py
run ci_events_check python3 scripts/ci_events.py --check
run ci_events_selftest python3 scripts/ci_events.py --selftest
run gate_selftest python3 syn/ooc/pp_resource_gate.py --selftest
run gate_mutants python3 syn/ooc/pp_resource_gate_mutants.py
run gate_check_baseline python3 syn/ooc/pp_resource_gate.py check-baseline
run placement_selftest python3 syn/ooc/pp_placement_selftest.py
run em_dash_base683e597 "$PY" scripts/check_em_dash.py --base 683e59712b93b2ef9fc81d22cc21c7d96e4c3909
run gen_toc_selftest "$PY" scripts/gen_toc.py --selftest
run gen_toc_anchors "$PY" scripts/gen_toc.py --verify-anchors
run gen_toc_check "$PY" scripts/gen_toc.py --check
wait
for g in doc_style:scripts/check_doc_style.py doc_paths:scripts/check_doc_paths.py \
         submodule_docs:scripts/check_submodule_docs.py gptp_docs:scripts/check_gptp_docs.py \
         py_idiom:scripts/check_py_idiom.py feature_status:scripts/check_feature_status.py \
         todo_ownership:scripts/check_todo_ownership.py solution_docs:scripts/check_solution_docs.py; do
  run "${g%%:*}" "$PY2" "${g#*:}"
done
run doc_style_selftest "$PY2" scripts/check_doc_style.py --selftest
run hygiene "$PY2" scripts/check_hygiene.py --check
run naming "$PY2" scripts/measure_naming.py --check
run test_evidence "$PY2" scripts/measure_test_evidence.py --check
run fail_fast "$PY2" scripts/measure_fail_fast.py --check
run evidence_pins "$PY2" scripts/generate_ci_evidence_pins.py --check
run gate_workflows "$PY2" scripts/ci_gate_workflows.py --check
run doc_map "$PY2" docs/DOC_MAP.gen.py --check
wait
for f in "$R"/*.rc; do printf '%s rc=%s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done
