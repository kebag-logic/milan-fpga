#!/usr/bin/env bash
# Run the static docs/registry gates on a candidate checkout, one log + rc per gate.
# usage: run_gates.sh <repo> <outdir> <base-sha>
set -u
repo=$1; out=$2; base=$3
cd "$repo"
gates=(
"docs_check.py" "check_feature_status.py" "check_feature_status.py --self-test"
"check_wire_accountability.py --self-test"
"check_em_dash.py --base $base" "check_doc_style.py" "check_doc_style.py --selftest"
"check_gptp_docs.py" "check_gptp_docs.py --selftest" "check_gptp_docs.py --with-submodule"
"check_solution_docs.py" "check_solution_docs.py --selftest"
"check_submodule_docs.py" "check_submodule_docs.py --selftest"
"check_diagram_pngs.py" "check_diagram_pngs.py --selftest"
"check_baremetal_only.py --check" "check_nvm_record_space.py" "check_nvm_capture.py"
"check_soc_sources.py" "check_soc_sources.py --selftest"
"check_rtl_source_lists.py" "check_rtl_source_lists.py --selftest"
"measure_naming.py --check" "check_port_contracts.py" "check_port_contracts.py --selftest"
"measure_fail_fast.py --check" "check_todo_ownership.py" "measure_test_evidence.py --check" "measure_test_evidence.py --selftest"
"check_hygiene.py --check" "check_sv_idiom.py" "check_cpp_idiom.py" "check_py_idiom.py" "check_py_idiom.py --selftest" "check_sh_idiom.py"
"check_doc_paths.py" "check_archive.py" "gen_toc.py --selftest" "gen_toc.py --verify-anchors" "gen_toc.py --check"
"ci_gate_workflows.py --check" "generate_ci_evidence_pins.py --check" "ci_events.py --check" "ci_events.py --selftest"
"suite_shards.py --selftest" "pp_srcs.py --check --selftest" "ci_scope.py --selftest"
)
i=0
for g in "${gates[@]}"; do
  i=$((i+1)); n=$(printf '%02d_%s' $i "$(echo "$g" | tr ' /' '__' | tr -cd 'A-Za-z0-9_.-')")
  printf '%s\0' "$n|$g"
done | xargs -0 -P 16 -I{} bash -c 'n=${1%%|*}; g=${1#*|}; ( timeout 900 python3 scripts/$g ) > "$2/$n.log" 2>&1; echo $? > "$2/$n.rc"' _ {} "$out"
for f in "$out"/*.rc; do printf '%s %s\n' "$(cat $f)" "$(basename $f .rc)"; done | sort -k2 > "$out/SUMMARY.txt"
