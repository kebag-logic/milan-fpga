#!/usr/bin/env bash
# Composition docs/registry gates on a checkout: run each, record its rc, never stop early.
# usage: docs_gates.sh <checkout> <base-sha> <outdir>
set -u
tree=$1; base=$2; out=$3
mkdir -p "$out"
cd "$tree" || exit 2
: > "$out/rc.txt"
run() {
  name=$1; shift
  "$@" > "$out/$name.log" 2>&1
  echo "$? $name :: $*" >> "$out/rc.txt"
}
run docs_check python3 scripts/docs_check.py
run feature_status python3 scripts/check_feature_status.py
run toc_check python3 scripts/gen_toc.py --check
run toc_anchors python3 scripts/gen_toc.py --verify-anchors
run em_dash python3 scripts/check_em_dash.py --base "$base"
run doc_paths python3 scripts/check_doc_paths.py
run doc_style python3 scripts/check_doc_style.py
run py_idiom python3 scripts/check_py_idiom.py
run cpp_idiom python3 scripts/check_cpp_idiom.py
run docs_inventory python3 scripts/docs_inventory.py --check
run doc_map python3 docs/DOC_MAP.gen.py --check
run ci_events_check python3 scripts/ci_events.py --check
run ci_events_selftest python3 scripts/ci_events.py --selftest
run measure_naming python3 scripts/measure_naming.py --check
run measure_test_evidence python3 scripts/measure_test_evidence.py --check
run measure_fail_fast python3 scripts/measure_fail_fast.py --check
run hygiene python3 scripts/check_hygiene.py --check
run todo_ownership python3 scripts/check_todo_ownership.py
run solution_docs python3 scripts/check_solution_docs.py
run evidence_pins python3 scripts/generate_ci_evidence_pins.py --check
run gate_workflows python3 scripts/ci_gate_workflows.py --check
run module_matrix python3 docs/traceability/gen_module_matrix.py --check
echo done > "$out/DONE"
