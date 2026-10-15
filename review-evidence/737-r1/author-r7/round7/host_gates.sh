#!/bin/bash
# Host doc and contract gates at the lane worktree; one log per gate, never piped.
set -uo pipefail
label="$1"
out=$VALIDATION_STORAGE/737-a614/r7/gates/$label
rm -rf "$out"; mkdir -p "$out"
cd $LANES/737-ci30
P=$VALIDATION_STORAGE/737-a614/venv/bin/python3
fail=0
gate() {
  name="$1"; shift
  start=$(date +%s.%N)
  "$@" > "$out/$name.log" 2>&1
  rc=$?
  printf '%-24s rc=%s %6.1fs\n' "$name" "$rc" "$(echo "$(date +%s.%N) - $start" | bc)"
  [ "$rc" -eq 0 ] || fail=1
}
gate docs-check $P scripts/docs_check.py
gate em-dash-r6 $P scripts/check_em_dash.py --base 47fd0d3c510000e9412a1613a723b61d4ef2ae4a
gate doc-style $P scripts/check_doc_style.py
gate gptp-docs $P scripts/check_gptp_docs.py
gate doc-paths $P scripts/check_doc_paths.py
gate toc-anchors $P scripts/gen_toc.py --verify-anchors
gate toc-check $P scripts/gen_toc.py --check
gate events-check $P scripts/ci_events.py --check
gate generator-check $P scripts/ci_gate_workflows.py --check
gate gate-selftest $P scripts/ci_gate_workflows_selftest.py
gate evidence-pins $P scripts/generate_ci_evidence_pins.py --check
gate runtime-evidence $P scripts/ci_runtime_evidence_selftest.py
gate baremetal-only $P scripts/check_baremetal_only.py --check
gate baremetal-selftest $P scripts/check_baremetal_only.py --selftest
gate py-idiom $P scripts/check_py_idiom.py
gate hygiene $P scripts/check_hygiene.py --check
gate diff-check git diff --check 47fd0d3c510000e9412a1613a723b61d4ef2ae4a
echo "overall fail=$fail"
exit "$fail"
