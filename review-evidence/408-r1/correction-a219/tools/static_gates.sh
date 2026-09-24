#!/bin/sh
# Evidence runner for the #408/#409 lane: each command's exit status is
# recorded; nothing stops at the first failure so every result is visible.
cd $LANES/408-409-boot-gate-retire || exit 2
BASE=759da623072358afdb0e9d570a7b4b6a788492c9
run() {
  out=$("$@" 2>&1); rc=$?
  printf 'rc=%s  %s\n' "$rc" "$*"
  [ "$rc" -ne 0 ] && printf '%s\n' "$out" | tail -n 25 | sed 's/^/    | /'
  return 0
}
run git diff --check "$BASE"
run python3 -B scripts/docs_check.py
run python3 -B scripts/check_em_dash.py --base "$BASE"
run python3 -B scripts/check_em_dash.py --selftest
run python3 -B scripts/check_doc_style.py
run python3 -B scripts/check_doc_style.py --selftest
run python3 -B scripts/check_gptp_docs.py
run python3 -B scripts/check_solution_docs.py
run python3 -B scripts/check_solution_docs.py --selftest
run python3 -B scripts/check_feature_status.py --self-test
run python3 -B docs/traceability/gen_module_matrix.py --check
run python3 -B scripts/check_baremetal_only.py --check
run python3 -B scripts/check_baremetal_only.py --selftest
run python3 -B sw/builder/test_firmware_compiler.py --selftest
run python3 -B scripts/check_nvm_record_space.py
run python3 -B sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
run python3 -B scripts/check_todo_ownership.py
run python3 -B scripts/check_todo_ownership.py --selftest
run python3 -B scripts/check_hygiene.py --check
run python3 -B scripts/check_hygiene.py --selftest
run python3 -B scripts/check_py_idiom.py
run python3 -B scripts/check_py_idiom.py --selftest
run python3 -B scripts/ci_events.py --check
run python3 -B scripts/ci_events.py --selftest
run python3 -B scripts/check_doc_paths.py
run python3 -B scripts/gen_toc.py --selftest
run python3 -B scripts/gen_toc.py --verify-anchors
run python3 -B scripts/gen_toc.py --check
run python3 -B scripts/docs_check.py
run python3 -B scripts/check_feature_status.py
# the ratchets LAST
run python3 -B scripts/measure_control_flow.py --selftest
run python3 -B scripts/measure_cohesion.py --selftest
run python3 -B scripts/measure_naming.py --check
run python3 -B scripts/measure_naming.py --selftest
run python3 -B scripts/measure_fail_fast.py --check
run python3 -B scripts/measure_fail_fast.py --selftest
run python3 -B scripts/measure_test_evidence.py --check
run python3 -B scripts/measure_test_evidence.py --selftest
