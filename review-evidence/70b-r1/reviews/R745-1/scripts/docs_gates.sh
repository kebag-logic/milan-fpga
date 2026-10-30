#!/usr/bin/env bash
# docs_gates.sh BASE : the documentation-workflow gates this PR's files reach, each with its rc
cd "$(git rev-parse --show-toplevel)" || exit 2
base=$1; fail=0
run() { echo "### $*"; "$@"; rc=$?; echo "### rc=$rc :: $*"; [ $rc = 0 ] || fail=1; }
run python3 scripts/docs_check.py
run python3 scripts/check_feature_status.py
run python3 scripts/check_feature_status.py --self-test
run python3 scripts/check_em_dash.py --base "$base"
run python3 scripts/check_doc_style.py
run python3 scripts/check_doc_paths.py
run python3 scripts/gen_toc.py --verify-anchors
run python3 scripts/gen_toc.py --check
run python3 scripts/check_nvm_record_space.py
run python3 scripts/check_baremetal_only.py --check
run python3 scripts/measure_test_evidence.py --check
run python3 scripts/measure_fail_fast.py --check
run python3 scripts/check_hygiene.py --check
run python3 scripts/check_cpp_idiom.py
run python3 scripts/check_py_idiom.py
run python3 scripts/check_todo_ownership.py
run python3 scripts/measure_naming.py --check
run python3 scripts/ci_gate_workflows.py --check
run python3 scripts/ci_command_table.py --check
run python3 docs/traceability/gen_module_matrix.py --check
echo "### overall fail=$fail"; exit $fail
