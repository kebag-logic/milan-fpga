#!/usr/bin/env bash
# Runs the docs.yml / fast-workflow static gates that read the files this PR and
# its predecessors both change, on the checkout given as $1, with the Python
# interpreter given as $2 (a venv holding tools/markdown/requirements.txt,
# pyyaml and wavedrom 2.0.3.post3). Em-dash base is $3 (the merge's first
# parent). Each command's output goes to $4/<n>.log and its exit status to
# $4/summary.tsv. No command writes tracked files (all are --check/--selftest).
set -u
tree=$1 py=$2 base=$3 out=$4
mkdir -p "$out"
: > "$out/summary.tsv"
cd "$tree" || exit 2
export PATH="$(dirname "$py"):$PATH"
n=0
run() {
  n=$((n + 1))
  local log; log=$(printf '%s/%03d.log' "$out" "$n")
  printf '$ %s\n' "$*" > "$log"
  "$@" >> "$log" 2>&1
  local rc=$?
  printf '%03d\t%d\t%s\n' "$n" "$rc" "$*" >> "$out/summary.tsv"
}
run python3 scripts/docs_check.py
run python3 scripts/check_em_dash.py --base "$base"
run python3 scripts/check_doc_style.py
run python3 scripts/check_doc_style.py --selftest
run python3 scripts/check_gptp_docs.py
run python3 docs/DOC_MAP.gen.py --check
run python3 docs/DOC_MAP.gen.py --selftest
run python3 scripts/check_solution_docs.py
run python3 docs/diagrams/submodule_boundaries.gen.py --check
run python3 scripts/check_submodule_docs.py
run python3 scripts/check_diagram_pngs.py
run python3 scripts/check_feature_status.py --self-test
run python3 scripts/check_feature_status.py
run python3 docs/traceability/gen_module_matrix.py --check
run python3 scripts/check_baremetal_only.py --check
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
run python3 scripts/check_sh_idiom.py
run python3 scripts/ci_events.py --check
run python3 scripts/ci_events.py --selftest
run python3 scripts/check_doc_paths.py
run python3 scripts/check_archive.py
run python3 scripts/gen_toc.py --selftest
run python3 scripts/gen_toc.py --verify-anchors
run python3 scripts/gen_toc.py --check
run python3 scripts/check_wire_accountability.py --self-test
run python3 scripts/pp_srcs.py --check --selftest
run python3 syn/ooc/pp_resource_gate.py check-baseline
run python3 syn/ooc/pp_resource_gate.py --selftest
run python3 syn/ooc/pp_baseline.py --selftest
awk -F'\t' '$2 != 0 {bad++} END {printf "commands=%d nonzero=%d\n", NR, bad+0}' "$out/summary.tsv"
