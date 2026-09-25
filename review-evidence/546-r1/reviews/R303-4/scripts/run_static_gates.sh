#!/usr/bin/env bash
# Composition static gates for the issue 546 merge-train candidate.
# Usage: run_static_gates.sh <candidate-clone> <out-dir> <md-python>
#   <md-python> is an interpreter with the hash-locked tools/markdown lock.
# Each gate's stdout+stderr goes to <out-dir>/<name>.log; rc to summary.tsv.
set -u
clone=$1 out=$2 mdpy=$3
mkdir -p "$out"
cd "$clone" || exit 2
head=$(git rev-parse HEAD)
p1=$(git rev-parse HEAD^1)
: > "$out/summary.tsv"
run() {
  local name=$1; shift
  local t0=$SECONDS
  "$@" > "$out/$name.log" 2>&1
  local rc=$?
  printf '%s\t%s\t%ss\t%s\n' "$name" "$rc" "$((SECONDS - t0))" "$*" >> "$out/summary.tsv"
}
echo "head $head parent1 $p1" > "$out/head.txt"
run docs_check            python3 scripts/docs_check.py
run docs_check_selftest   python3 scripts/docs_check.py --selftest
run feature_status        python3 scripts/check_feature_status.py
run em_dash_base_parent1  "$mdpy" scripts/check_em_dash.py --base "$p1"
run em_dash_base_dev      "$mdpy" scripts/check_em_dash.py --base c266432dcb0cdd464205823a3d82cad260eedde2
run em_dash_selftest      "$mdpy" scripts/check_em_dash.py --selftest
run doc_style             python3 scripts/check_doc_style.py
run doc_style_selftest    python3 scripts/check_doc_style.py --selftest
run gptp_docs             python3 scripts/check_gptp_docs.py
run doc_paths             python3 scripts/check_doc_paths.py
run doc_map_check         python3 docs/DOC_MAP.gen.py --check
run timesync_chain_check  python3 docs/diagrams/timesync_chain.gen.py --check
run solution_docs         python3 scripts/check_solution_docs.py
run submodule_bound_check python3 docs/diagrams/submodule_boundaries.gen.py --check
run submodule_docs        python3 scripts/check_submodule_docs.py
run module_matrix_check   python3 docs/traceability/gen_module_matrix.py --check
run gen_toc_check         "$mdpy" scripts/gen_toc.py --check
run gen_toc_anchors       "$mdpy" scripts/gen_toc.py --verify-anchors
run gen_toc_selftest      "$mdpy" scripts/gen_toc.py --selftest
run measure_evidence      python3 scripts/measure_test_evidence.py --check
run measure_evidence_st   python3 scripts/measure_test_evidence.py --selftest
run nvm_record_space      python3 scripts/check_nvm_record_space.py
run nvm_record_space_st   python3 scripts/check_nvm_record_space.py --self-test
run rtl_source_lists      python3 scripts/check_rtl_source_lists.py
run port_contracts        python3 scripts/check_port_contracts.py
run naming_check          python3 scripts/measure_naming.py --check
run fail_fast_check       python3 scripts/measure_fail_fast.py --check
run todo_ownership        python3 scripts/check_todo_ownership.py
run hygiene_check         python3 scripts/check_hygiene.py --check
run sv_idiom              python3 scripts/check_sv_idiom.py
run cpp_idiom             python3 scripts/check_cpp_idiom.py
run py_idiom              python3 scripts/check_py_idiom.py
run sh_idiom              python3 scripts/check_sh_idiom.py
run ci_events_check       python3 scripts/ci_events.py --check
run ci_events_selftest    python3 scripts/ci_events.py --selftest
run archive_check         python3 scripts/check_archive.py
run baremetal_only        python3 scripts/check_baremetal_only.py --check
run xvlog_gate_check      python3 scripts/xvlog_gate.py --check
run lint_rtl_check        python3 scripts/lint_rtl.py --check
run diff_check_parent1    git diff --check "$p1" "$head"
# The no-Git mode: the tracked tree exported without .git (docs-check-no-git).
exp="${SCRATCH_DIR:?set SCRATCH_DIR}/export"
rm -rf "$exp"; mkdir -p "$exp"
git archive "$head" | tar -x -C "$exp"
( cd "$exp" && python3 scripts/docs_check.py ) > "$out/docs_check_no_git.log" 2>&1
printf '%s\t%s\t-\t%s\n' docs_check_no_git "$?" "exported tree, no .git: python3 scripts/docs_check.py" >> "$out/summary.tsv"
( cd "$exp" && python3 scripts/check_feature_status.py ) > "$out/feature_status_no_git.log" 2>&1
printf '%s\t%s\t-\t%s\n' feature_status_no_git "$?" "exported tree, no .git: python3 scripts/check_feature_status.py" >> "$out/summary.tsv"
rm -rf "$exp"
cat "$out/summary.tsv"
