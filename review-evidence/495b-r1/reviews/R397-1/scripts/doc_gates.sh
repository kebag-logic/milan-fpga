#!/bin/bash
# Markdown, documentation and code-quality gates of docs.yml at the head,
# run in the pinned renderer venv (first on PATH). act_ci.py --selftest is
# excluded by the review's rules. Each gate prints one RESULT line.
# Usage: doc_gates.sh <clone> <base-rev>
set -u
cd "$1"; base=$2
fail=0
g() { local out; out=$("$@" 2>&1); local rc=$?; echo "RESULT rc=$rc :: $*"; [ $rc -ne 0 ] && { echo "$out" | tail -15; fail=1; }; echo "$out" | tail -2 | sed 's/^/    /'; }
g python3 scripts/docs_check.py
g python3 scripts/check_em_dash.py --base "$base"
g python3 scripts/check_em_dash.py --selftest
g python3 scripts/gen_toc.py --check
g python3 scripts/check_doc_style.py
g python3 scripts/check_doc_style.py --selftest
g python3 scripts/check_gptp_docs.py
g python3 scripts/check_gptp_docs.py --selftest
g python3 scripts/check_gptp_docs.py --with-submodule
g python3 docs/DOC_MAP.gen.py --check
g python3 docs/DOC_MAP.gen.py --selftest
g python3 docs/diagrams/timesync_chain.gen.py --check
g python3 docs/diagrams/timesync_chain.gen.py --selftest
g python3 scripts/check_solution_docs.py
g python3 scripts/check_solution_docs.py --selftest
g python3 docs/diagrams/submodule_boundaries.gen.py --check
g python3 docs/diagrams/submodule_boundaries.gen.py --selftest
g python3 scripts/check_submodule_docs.py
g python3 scripts/check_submodule_docs.py --selftest
g python3 scripts/check_feature_status.py --self-test
g python3 docs/traceability/gen_module_matrix.py --check
g python3 scripts/check_doc_paths.py
g python3 scripts/measure_control_flow.py --selftest
g python3 scripts/measure_cohesion.py --selftest
g python3 scripts/check_baremetal_only.py --check
g python3 scripts/check_baremetal_only.py --selftest
g python3 scripts/check_port_contracts.py
g python3 scripts/check_port_contracts.py --selftest
g python3 scripts/measure_fail_fast.py --check
g python3 scripts/measure_fail_fast.py --selftest
g python3 scripts/check_todo_ownership.py
g python3 scripts/check_todo_ownership.py --selftest
g python3 scripts/measure_test_evidence.py --check
g python3 scripts/measure_test_evidence.py --selftest
g python3 scripts/check_hygiene.py --check
g python3 scripts/check_hygiene.py --selftest
g python3 scripts/check_py_idiom.py
g python3 scripts/check_py_idiom.py --selftest
g python3 scripts/check_sh_idiom.py
g python3 scripts/check_sh_idiom.py --selftest
g python3 scripts/check_cpp_idiom.py
g python3 scripts/check_cpp_idiom.py --selftest
g python3 scripts/check_sv_idiom.py
g python3 scripts/check_sv_idiom.py --selftest
g python3 scripts/measure_naming.py --check
g python3 scripts/measure_naming.py --selftest
g python3 scripts/ci_events.py --check
g python3 scripts/ci_events.py --selftest
g python3 scripts/ci_scope.py --selftest
g python3 scripts/pp_srcs.py --check
g python3 scripts/pp_srcs.py --selftest
g bash -n sw/litex/sweep_extra.sh
echo "OVERALL fail=$fail"
