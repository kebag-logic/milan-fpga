#!/usr/bin/env bash
# Run, at the merge-train candidate, every static gate that reads a file
# this PR or a predecessor changed, or a registry/table/anchor both sides
# feed. Each command's output goes to <out>/<n>-<label>.log and its exit
# status to <out>/gates.tsv. Nothing here writes tracked files.
# usage: composition_gates.sh <clone> <out-dir>
set -u
clone=$1; out=$2
mkdir -p "$out"
cd "$clone" || exit 2
: > "$out/gates.tsv"
n=0
run() {
  local label=$1; shift
  n=$((n + 1))
  local log; log=$(printf '%s/%02d-%s.log' "$out" "$n" "$label")
  { echo "\$ $*"; "$@"; } > "$log" 2>&1
  local rc=$?
  printf '%02d\t%s\t%s\t%s\n' "$n" "$rc" "$label" "$*" >> "$out/gates.tsv"
}
DEV=759da623072358afdb0e9d570a7b4b6a788492c9
MB=ede8d48ecd7c7f589a14b957951f040d92c99c70
run em_dash_vs_dev          python3 scripts/check_em_dash.py --base "$DEV"
run em_dash_vs_mergebase    python3 scripts/check_em_dash.py --base "$MB"
run em_dash_ci_derived      bash -c 'python3 scripts/check_em_dash.py --base "$(git merge-base '"$DEV"' HEAD)"'
run em_dash_selftest        python3 scripts/check_em_dash.py --selftest
run docs_check              python3 scripts/docs_check.py
run doc_style               python3 scripts/check_doc_style.py
run doc_style_selftest      python3 scripts/check_doc_style.py --selftest
run gptp_docs               python3 scripts/check_gptp_docs.py
run doc_map_check           python3 docs/DOC_MAP.gen.py --check
run timesync_chain_check    python3 docs/diagrams/timesync_chain.gen.py --check
run solution_docs           python3 scripts/check_solution_docs.py
run submodule_boundaries    python3 docs/diagrams/submodule_boundaries.gen.py --check
run submodule_docs          python3 scripts/check_submodule_docs.py
run feature_status          python3 scripts/check_feature_status.py
run feature_status_selftest python3 scripts/check_feature_status.py --self-test
run module_matrix_check     python3 docs/traceability/gen_module_matrix.py --check
run doc_paths               python3 scripts/check_doc_paths.py
run archive                 python3 scripts/check_archive.py
run toc_verify_anchors      python3 scripts/gen_toc.py --verify-anchors
run toc_check               python3 scripts/gen_toc.py --check
run toc_selftest            python3 scripts/gen_toc.py --selftest
run rtl_source_lists        python3 scripts/check_rtl_source_lists.py
run soc_sources             python3 scripts/check_soc_sources.py
run measure_naming          python3 scripts/measure_naming.py --check
run port_contracts          python3 scripts/check_port_contracts.py
run fail_fast               python3 scripts/measure_fail_fast.py --check
run todo_ownership          python3 scripts/check_todo_ownership.py
run test_evidence           python3 scripts/measure_test_evidence.py --check
run test_evidence_selftest  python3 scripts/measure_test_evidence.py --selftest
run hygiene                 python3 scripts/check_hygiene.py --check
run sv_idiom                python3 scripts/check_sv_idiom.py
run cpp_idiom               python3 scripts/check_cpp_idiom.py
run py_idiom                python3 scripts/check_py_idiom.py
run sh_idiom                python3 scripts/check_sh_idiom.py
run ci_events_check         python3 scripts/ci_events.py --check
run ci_events_selftest      python3 scripts/ci_events.py --selftest
run baremetal_only          python3 scripts/check_baremetal_only.py --check
run pp_srcs_check           python3 scripts/pp_srcs.py --check
run lint_rtl_check          env PATH="$VERILATOR_BIN_DIR:$PATH" python3 scripts/lint_rtl.py --check
run xvlog_gate_check        python3 scripts/xvlog_gate.py --check
run suite_list              bash scripts/run_all_suites.sh --list
run suite_shards_selftest   python3 scripts/suite_shards.py --selftest
run diff_check_vs_dev       git diff --check "$DEV" HEAD
run diff_check_vs_mb        git diff --check "$MB" HEAD
