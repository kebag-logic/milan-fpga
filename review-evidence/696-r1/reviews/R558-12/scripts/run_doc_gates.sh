#!/bin/sh
# Run the documentation and registry gates that read files the composed
# candidate changes. Usage: run_doc_gates.sh <candidate checkout> <out dir> <em-dash base>...
# Each command gets its own log; summary.tsv records rc per command.
TREE=$1; OUT=$2; shift 2
mkdir -p "$OUT"
cd "$TREE" || exit 2
: > "$OUT/summary.tsv"
n=0
run() {
    n=$((n + 1))
    log=$(printf '%s/%02d.log' "$OUT" "$n")
    printf '$ %s\n' "$*" > "$log"
    "$@" >> "$log" 2>&1
    rc=$?
    printf '%d\t%s\n' "$rc" "$*" >> "$OUT/summary.tsv"
}
for base in "$@"; do
    run python3 scripts/check_em_dash.py --base "$base"
done
run python3 scripts/docs_check.py
run python3 scripts/check_doc_style.py
run python3 scripts/check_doc_style.py --selftest
run python3 scripts/check_gptp_docs.py
run python3 docs/DOC_MAP.gen.py --check
run python3 scripts/check_solution_docs.py
run python3 scripts/check_submodule_docs.py
run python3 scripts/check_diagram_pngs.py
run python3 scripts/check_feature_status.py --self-test
run python3 docs/traceability/gen_module_matrix.py --check
run python3 scripts/check_gptp_docs.py --with-submodule
run python3 scripts/check_baremetal_only.py --check
run python3 scripts/check_rtl_source_lists.py
run python3 scripts/measure_naming.py --check
run python3 scripts/check_port_contracts.py
run python3 scripts/measure_fail_fast.py --check
run python3 scripts/check_todo_ownership.py
run python3 scripts/measure_test_evidence.py --check
run python3 scripts/measure_test_evidence.py --selftest
run python3 scripts/check_hygiene.py --check
run python3 scripts/check_sv_idiom.py
run python3 scripts/check_cpp_idiom.py
run python3 scripts/check_py_idiom.py
run python3 scripts/check_sh_idiom.py
run python3 scripts/ci_events.py --check
run python3 scripts/ci_events.py --selftest
run python3 scripts/check_doc_paths.py
run python3 scripts/check_archive.py
run python3 scripts/gen_toc.py --selftest
run python3 scripts/gen_toc.py --verify-anchors
run python3 scripts/gen_toc.py --check
run python3 scripts/check_sweep_shape.py --self-test
run python3 scripts/suite_shards.py --selftest
run python3 scripts/check_wire_accountability.py --self-test
run python3 syn/ooc/pp_resource_gate.py check-baseline
run python3 scripts/lint_rtl.py --check
printf 'commands=%d failing=%d\n' "$n" "$(awk -F'\t' '$1 != 0' "$OUT/summary.tsv" | wc -l)" >> "$OUT/summary.tsv"
