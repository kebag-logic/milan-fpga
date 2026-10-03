#!/usr/bin/env bash
# R449-3: the parent consumer set's light gates (and the self-tests that read
# run.sh or a processor budget) in a scratch parent at milan-fpga 1269cdaf +
# c8 + p2-p1 + c10, the processor gitlink at the head under review.
# usage: parent_light.sh <parent-tree>
# Prints one "GATE <label> rc=<n>" line per command followed by its last lines.
set -u
cd "$1" || exit 2
run() {
  local label=$1; shift
  local out rc
  out="$("$@" 2>&1)"; rc=$?
  echo "GATE $label rc=$rc :: $*"
  printf '%s\n' "$out" | tail -n 6 | sed 's/^/    /'
}
run 1-cpp-idiom           python3 scripts/check_cpp_idiom.py
run 2-py-idiom            python3 scripts/check_py_idiom.py
run 3-rtl-source-lists    python3 scripts/check_rtl_source_lists.py
run 3-rtl-source-lists-st python3 scripts/check_rtl_source_lists.py --selftest
run 4-pp-srcs             python3 scripts/pp_srcs.py --check --selftest
run 5-port-contracts      python3 scripts/check_port_contracts.py
run 6-naming              python3 scripts/measure_naming.py --check
run 7-test-evidence       python3 scripts/measure_test_evidence.py --check
run 8-docs-check          python3 scripts/docs_check.py
run 9-xvlog-gate          python3 scripts/xvlog_gate.py --check
run 9-xvlog-gate-st       python3 scripts/xvlog_gate.py --selftest
run 10-test-builder       python3 sw/builder/test_builder.py
run 11-lint-rtl           python3 scripts/lint_rtl.py --check
run 17-sh-idiom           python3 scripts/check_sh_idiom.py
run st-sh-idiom           python3 scripts/check_sh_idiom.py --selftest
run st-hygiene-check      python3 scripts/check_hygiene.py --check
run st-hygiene            python3 scripts/check_hygiene.py --selftest
run st-todo               python3 scripts/check_todo_ownership.py
run st-todo-st            python3 scripts/check_todo_ownership.py --selftest
run st-fail-fast          python3 scripts/measure_fail_fast.py --check
run st-fail-fast-st       python3 scripts/measure_fail_fast.py --selftest
run st-entity-shape       python3 scripts/check_entity_shape.py --self-test
