#!/bin/sh
# Focused read-only documentation/quality gates at the reviewed head (run from the repo root).
run() { echo "### $*"; "$@" > /tmp/r877_gate.out 2>&1; rc=$?; tail -n 6 /tmp/r877_gate.out; echo "### rc=$rc :: $*"; }
run python3 scripts/docs_check.py
run python3 scripts/check_em_dash.py --base 15168e14
run python3 scripts/check_doc_paths.py
run python3 scripts/docs_inventory.py --check
run python3 scripts/check_rtl_source_lists.py
run python3 scripts/check_soc_sources.py
run python3 scripts/measure_naming.py --check
run python3 scripts/check_port_contracts.py
run python3 scripts/measure_fail_fast.py --check
run python3 scripts/check_todo_ownership.py
run python3 scripts/measure_test_evidence.py --check
run python3 scripts/check_hygiene.py --check
run python3 scripts/check_sv_idiom.py
run python3 scripts/check_cpp_idiom.py
run python3 scripts/check_py_idiom.py
run python3 scripts/lint_rtl.py --check
rm -f /tmp/r877_gate.out
