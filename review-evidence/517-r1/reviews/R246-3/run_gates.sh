#!/bin/sh
# Static/documentation/tooling gates that read the files this PR changes,
# run on the composed candidate. usage: run_gates.sh <clone> <parent-rev>
# Prints one "GATE rc=<n> <command>" line per gate; exit 0 only if all pass.
C="$1"; BASE="$2"
cd "$C" || exit 2
fail=0
gate() {
    out=$("$@" 2>&1); rc=$?
    printf 'GATE rc=%s %s\n' "$rc" "$*"
    printf '%s\n' "$out" | tail -n 4 | sed 's/^/    | /'
    [ "$rc" -eq 0 ] || fail=1
}
gate python3 scripts/docs_check.py
gate python3 scripts/check_em_dash.py --base "$BASE"
gate python3 scripts/check_em_dash.py --selftest
gate python3 scripts/gen_toc.py --selftest
gate python3 scripts/gen_toc.py --verify-anchors
gate python3 scripts/gen_toc.py --check
gate python3 scripts/check_doc_style.py
gate python3 scripts/check_doc_paths.py
gate python3 scripts/check_baremetal_only.py --check
gate python3 scripts/check_baremetal_only.py --selftest
gate python3 scripts/measure_test_evidence.py --check
gate python3 scripts/measure_test_evidence.py --selftest
gate python3 scripts/check_py_idiom.py
gate python3 scripts/check_hygiene.py --check
gate python3 scripts/measure_fail_fast.py --check
gate python3 scripts/measure_naming.py --check
gate python3 scripts/check_todo_ownership.py
gate python3 scripts/ci_events.py --check
gate python3 scripts/ci_events.py --selftest
gate python3 scripts/check_archive.py
gate python3 scripts/check_solution_docs.py
gate python3 docs/DOC_MAP.gen.py --check
gate python3 scripts/check_sweep_shape.py --self-test
gate python3 scripts/check_feature_status.py
gate python3 tb/verilator/milan_dp/test_sim_pool.py
gate python3 tb/verilator/milan_dp/test_sim_pool_backpressure.py
gate python3 tb/verilator/milan_dp/test_render_phase_observation.py
echo "ALL_GATES_FAIL=$fail"
exit "$fail"
