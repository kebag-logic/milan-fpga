#!/bin/bash
# Run the static/documentation/inventory gates that read the files the #548
# composition changes, on the candidate checkout, at most 8 in parallel.
# Usage: gates.sh <repo> <out-dir> <python-with-pinned-markdown-renderer> <verilator-bin-dir>
set -u
repo=$1
out=$2
vpy=$3
vbin=$4
parent=e1333a144115f074f8e3bdcd1de2d3a29d7f9dfd   # composition parent (predecessor candidate)
srcbase=573f0052a0e4412e81f0845438fcec2086ce5d55  # source PR base
mkdir -p "$out/logs"
list="$out/gate_list.tsv"
cat > "$list" <<EOF
docs_check_git	python3 scripts/docs_check.py
docs_check_fs	env GIT_DIR=/dev/null python3 scripts/docs_check.py
em_dash_parent	$vpy scripts/check_em_dash.py --base $parent
em_dash_srcbase	$vpy scripts/check_em_dash.py --base $srcbase
em_dash_selftest	$vpy scripts/check_em_dash.py --selftest
gen_toc_verify_anchors	$vpy scripts/gen_toc.py --verify-anchors
gen_toc_check	$vpy scripts/gen_toc.py --check
gen_toc_selftest	$vpy scripts/gen_toc.py --selftest
ci_events_check	python3 scripts/ci_events.py --check
ci_events_selftest	python3 scripts/ci_events.py --selftest
doc_style	python3 scripts/check_doc_style.py
doc_paths	python3 scripts/check_doc_paths.py
gptp_docs	python3 scripts/check_gptp_docs.py
gptp_docs_submodule	python3 scripts/check_gptp_docs.py --with-submodule
solution_docs	python3 scripts/check_solution_docs.py
submodule_docs	python3 scripts/check_submodule_docs.py
doc_map	python3 docs/DOC_MAP.gen.py --check
module_matrix	python3 docs/traceability/gen_module_matrix.py --check
feature_status	python3 scripts/check_feature_status.py
hygiene	python3 scripts/check_hygiene.py --check
port_contracts	python3 scripts/check_port_contracts.py
soc_sources	python3 scripts/check_soc_sources.py
rtl_source_lists	python3 scripts/check_rtl_source_lists.py
sv_idiom	python3 scripts/check_sv_idiom.py
cpp_idiom	python3 scripts/check_cpp_idiom.py
py_idiom	python3 scripts/check_py_idiom.py
naming	python3 scripts/measure_naming.py --check
fail_fast	python3 scripts/measure_fail_fast.py --check
test_evidence	python3 scripts/measure_test_evidence.py --check
todo_ownership	python3 scripts/check_todo_ownership.py
archive	python3 scripts/check_archive.py
pp_srcs	python3 scripts/pp_srcs.py --check
lint_rtl	env PATH=$vbin:\$PATH python3 scripts/lint_rtl.py --check
xvlog_gate	python3 scripts/xvlog_gate.py --check
tied_inputs	bash scripts/check_tied_inputs.sh
diff_check_parent	git diff --check $parent HEAD
EOF
run_one() {
  # the command is read verbatim from the list, so nothing in it is expanded
  # before the gate's own shell runs it
  name=$1
  cmd=$(awk -F'\t' -v n="$name" '$1==n {sub(/^[^\t]*\t/, ""); print; exit}' "$list")
  start=$(date +%s)
  ( cd "$repo" && PYTHONDONTWRITEBYTECODE=1 bash -c "$cmd" ) > "$out/logs/$name.log" 2>&1
  rc=$?
  printf '%s\t%s\t%ss\t%s\n' "$name" "$rc" "$(( $(date +%s) - start ))" "$cmd" > "$out/logs/$name.rc"
}
export -f run_one
export repo out list
cut -f1 "$list" | xargs -P 8 -I{} bash -c 'run_one "$1"' _ {}
cat "$out"/logs/*.rc | sort > "$out/gates_summary.tsv"
cat "$out/gates_summary.tsv"
