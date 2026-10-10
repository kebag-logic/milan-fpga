#!/usr/bin/env bash
# Run the documentation, static and resource gates that read the files the
# #696 / M0s composition touches, on a candidate checkout.
# Usage: run_gates.sh <candidate-checkout> <python-with-markdown-deps> <out-dir>
# Each gate writes <out-dir>/<name>.log and <out-dir>/<name>.rc; at most 16 run at once.
set -u
repo=$1; py=$2; out=$3
mkdir -p "$out"
export PYTHONDONTWRITEBYTECODE=1
pybin=$(dirname "$py")
gates=$(cat <<'EOF'
docs_check|python3 scripts/docs_check.py
gen_toc_check|python3 scripts/gen_toc.py
gen_toc_verify_anchors|python3 scripts/gen_toc.py --verify-anchors
gen_toc_selftest|python3 scripts/gen_toc.py --selftest
em_dash_parent_c64a9b66|python3 scripts/check_em_dash.py --base c64a9b66cf5b671964edb043cb8f205b21a5e8be
em_dash_dev_e8454e27|python3 scripts/check_em_dash.py --base e8454e2751d05b02ee8e5a571857589ab358ab86
em_dash_selftest|python3 scripts/check_em_dash.py --selftest
doc_style|python3 scripts/check_doc_style.py
doc_style_selftest|python3 scripts/check_doc_style.py --selftest
doc_paths|python3 scripts/check_doc_paths.py
doc_map_check|python3 docs/DOC_MAP.gen.py --check
doc_map_selftest|python3 docs/DOC_MAP.gen.py --selftest
solution_docs|python3 scripts/check_solution_docs.py
solution_docs_selftest|python3 scripts/check_solution_docs.py --selftest
feature_status_selftest|python3 scripts/check_feature_status.py --self-test
module_matrix_check|python3 docs/traceability/gen_module_matrix.py --check
ci_events_check|python3 scripts/ci_events.py --check
ci_events_selftest|python3 scripts/ci_events.py --selftest
rtl_source_lists|python3 scripts/check_rtl_source_lists.py
rtl_source_lists_selftest|python3 scripts/check_rtl_source_lists.py --selftest
port_contracts|python3 scripts/check_port_contracts.py
test_evidence|python3 scripts/measure_test_evidence.py --check
hygiene|python3 scripts/check_hygiene.py --check
sv_idiom|python3 scripts/check_sv_idiom.py
cpp_idiom|python3 scripts/check_cpp_idiom.py
py_idiom|python3 scripts/check_py_idiom.py
naming|python3 scripts/measure_naming.py --check
fail_fast|python3 scripts/measure_fail_fast.py --check
todo_ownership|python3 scripts/check_todo_ownership.py
resource_check_baseline|python3 syn/ooc/pp_resource_gate.py check-baseline
resource_gate_selftest|python3 syn/ooc/pp_resource_gate.py --selftest
placement_selftest|python3 syn/ooc/pp_placement_selftest.py
EOF
)
run_one() {
  name=${1%%|*}; cmd=${1#*|}
  ( cd "$repo" && PATH="$pybin:$PATH" bash -c "$cmd" ) >"$out/$name.log" 2>&1
  echo $? >"$out/$name.rc"
}
export -f run_one
export repo out pybin
printf '%s\n' "$gates" | xargs -P 16 -I{} bash -c 'run_one "$@"' _ {}
for f in "$out"/*.rc; do printf '%s %s\n' "$(cat "$f")" "$(basename "$f" .rc)"; done | sort -k2
