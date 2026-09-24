#!/usr/bin/env bash
# Run the offline repository gates that read the files this composition
# touches, on the candidate clone, one receipt per gate plus a summary.
# The pinned simulator directory is put first on PATH for the gates that
# call `verilator` (lint ratchet). No gate here writes to the tree: every
# gate is run in its check/self-test mode.
# Usage: run_gates.sh <repo> <out-dir> <pinned-tool-bin-dir> <dev-parent> <merge-base>
set -uo pipefail
repo=$1 out=$2 pin=$3 devp=$4 mb=$5
mkdir -p "$out"
export PATH="$pin:$PATH"
summary="$out/SUMMARY.txt"
: > "$summary"
echo "verilator on PATH: $(command -v verilator) -> $(verilator --version)" >> "$summary"
echo "head: $(git -C "$repo" rev-parse HEAD)" >> "$summary"
i=0
run() {
  i=$((i+1))
  local name; name=$(printf '%02d_%s' "$i" "$(echo "$*" | tr -c 'A-Za-z0-9._-' '_' | cut -c1-80)")
  local log="$out/$name.log"
  echo "\$ $*" > "$log"
  ( cd "$repo" && timeout 1800 "$@" ) >> "$log" 2>&1
  local rc=$?
  echo "exit=$rc" >> "$log"
  printf '%-4s %s\n' "$rc" "$*" >> "$summary"
}
run python3 scripts/docs_check.py
run python3 scripts/check_em_dash.py --base "$devp"
run python3 scripts/check_em_dash.py --base "$mb"
run python3 scripts/check_em_dash.py --selftest
run python3 scripts/check_doc_style.py
run python3 scripts/check_doc_style.py --selftest
run python3 scripts/check_gptp_docs.py
run python3 scripts/check_gptp_docs.py --with-submodule
run python3 docs/DOC_MAP.gen.py --check
run python3 docs/diagrams/timesync_chain.gen.py --check
run python3 scripts/check_solution_docs.py
run python3 docs/diagrams/submodule_boundaries.gen.py --check
run python3 scripts/check_submodule_docs.py
run python3 scripts/check_diagram_pngs.py
run python3 scripts/check_feature_status.py
run python3 scripts/check_feature_status.py --self-test
run python3 docs/traceability/gen_module_matrix.py --check
run python3 scripts/check_baremetal_only.py --check
run python3 scripts/check_baremetal_only.py --selftest
run python3 scripts/check_rtl_source_lists.py
run python3 scripts/measure_naming.py --check
run python3 scripts/check_port_contracts.py
run python3 scripts/check_port_contracts.py --selftest
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
run python3 avdecc/gen_aem_store.py --self-test
run python3 scripts/check_sweep_shape.py --self-test
run python3 scripts/check_deploy_shape.py --self-test
run python3 scripts/check_entity_shape.py --self-test
run python3 scripts/check_wire_accountability.py --self-test
run python3 scripts/check_nvm_record_space.py
run python3 scripts/check_soc_sources.py
run python3 scripts/lint_rtl.py --check
run python3 scripts/pp_srcs.py --check
run python3 scripts/xvlog_gate.py --check
run python3 scripts/ci_scope.py --selftest
