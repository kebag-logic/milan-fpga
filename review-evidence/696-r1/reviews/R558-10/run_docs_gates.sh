#!/bin/sh
# Run the documentation gates of .github/workflows/docs.yml that need no network,
# SDK, container or hosted service, plus the resource-gate baseline check, at a
# checkout of the head under review. Usage: run_docs_gates.sh <checkout> <base-rev>
# Prints one "rc=<n> <command>" line per gate after the gate's own output.
cd "$1" || exit 2
BASE="$2"
run() {
  echo "---- $*"
  "$@"
  echo "rc=$? $*"
}
run python3 scripts/docs_check.py
run python3 scripts/check_em_dash.py --base "$BASE"
run python3 scripts/check_doc_style.py
run python3 scripts/check_gptp_docs.py
run python3 docs/DOC_MAP.gen.py --check
run python3 docs/diagrams/timesync_chain.gen.py --check
run python3 scripts/check_solution_docs.py
run python3 docs/diagrams/submodule_boundaries.gen.py --check
run python3 scripts/check_submodule_docs.py
run python3 scripts/check_diagram_pngs.py
run python3 scripts/check_feature_status.py
run python3 scripts/gen_toc.py --verify-anchors
run python3 scripts/gen_toc.py --check
run python3 scripts/check_archive.py
run python3 scripts/check_hygiene.py --check
run python3 scripts/check_py_idiom.py
run python3 scripts/check_cpp_idiom.py
run python3 scripts/measure_test_evidence.py --check
run python3 scripts/check_todo_ownership.py
run python3 syn/ooc/pp_resource_gate.py check-baseline
