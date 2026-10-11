#!/usr/bin/env bash
# Every command of .github/workflows/docs.yml (docs-check, wire-accountability,
# docs-check-no-git) at the checked-out head, minus the package installs, each
# logged on its own with its exit status. Usage: docs_parity.sh <tree> <logs> <em-dash base>
# Run it with a HOME holding only the pinned SDK at br-milan-rv32/host, as the
# hosted runner has it, and no LiteX interpreter.
set -uo pipefail
tree="$1"; logs="$2"; base="$3"
mkdir -p "$logs" "$logs/runner-temp"
summary="$logs/summary.tsv"
: > "$summary"
n=0
run() {
  n=$((n + 1))
  local log
  log="$logs/$(printf '%02d' "$n")-$(echo "$*" | tr -c 'A-Za-z0-9._-' '_' | cut -c1-80).log"
  ( cd "$tree" && "$@" ) > "$log" 2>&1
  local rc=$?
  printf '%s\t%s\t%s\n' "$n" "$rc" "$*" >> "$summary"
  printf '%3d rc=%d %s\n' "$n" "$rc" "$*"
}
run python3 scripts/gen_hdl_reference.py --selftest
run python3 scripts/gen_hdl_reference.py --output "$logs/runner-temp/milan-hdl-reference"
run python3 scripts/docs_check.py
run python3 scripts/check_em_dash.py --base "$base"
run python3 scripts/check_doc_style.py
run python3 scripts/check_doc_style.py --selftest
run python3 scripts/check_gptp_docs.py
run python3 scripts/check_gptp_docs.py --selftest
run python3 docs/DOC_MAP.gen.py --check
run python3 docs/DOC_MAP.gen.py --selftest
run python3 docs/diagrams/timesync_chain.gen.py --check
run python3 docs/diagrams/timesync_chain.gen.py --selftest
run python3 scripts/check_solution_docs.py
run python3 scripts/check_solution_docs.py --selftest
run python3 docs/diagrams/submodule_boundaries.gen.py --check
run python3 docs/diagrams/submodule_boundaries.gen.py --selftest
run python3 scripts/check_submodule_docs.py
run python3 scripts/check_submodule_docs.py --selftest
run python3 scripts/gen_wavedrom.py --selftest
run python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check
run python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check
run python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check
run python3 scripts/check_diagram_pngs.py
run python3 scripts/check_diagram_pngs.py --selftest
run python3 scripts/check_feature_status.py --self-test
run python3 docs/traceability/gen_module_matrix.py --check
run python3 scripts/check_gptp_docs.py --with-submodule
run "$MAKE" -C gptp-processor docs
run python3 scripts/measure_control_flow.py --selftest
run python3 scripts/measure_cohesion.py --selftest
run sv2v --version
run python3 scripts/check_baremetal_only.py --check
run python3 scripts/check_baremetal_only.py --selftest
run python3 scripts/ci_rv32_sdk_selftest.py
run python3 scripts/ci_rv32_sdk.py --verify-only --destination "$HOME/br-milan-rv32/host"
run python3 sw/builder/test_firmware_compiler.py --selftest
run python3 sw/builder/test_firmware_compiler.py --absent --audit "$logs/runner-temp/rv32-absent.jsonl"
run python3 sw/builder/test_builder.py --require-rv32
run python3 scripts/check_nvm_record_space.py
run python3 scripts/check_nvm_record_space.py --self-test
run python3 scripts/check_nvm_capture.py
run python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
run python3 scripts/check_soc_sources.py
run python3 scripts/check_soc_sources.py --selftest
run python3 sw/litex/iob_pack_selftest.py
run python3 scripts/check_rtl_source_lists.py
run python3 scripts/check_rtl_source_lists.py --selftest
run python3 scripts/measure_naming.py --check
run python3 scripts/measure_naming.py --selftest
run python3 scripts/check_port_contracts.py
run python3 scripts/check_port_contracts.py --selftest
run python3 scripts/measure_fail_fast.py --check
run python3 scripts/measure_fail_fast.py --selftest
run python3 scripts/check_todo_ownership.py
run python3 scripts/check_todo_ownership.py --selftest
run python3 scripts/measure_test_evidence.py --check
run python3 scripts/measure_test_evidence.py --selftest
run python3 scripts/check_hygiene.py --check
run python3 scripts/check_hygiene.py --selftest
run python3 scripts/check_sv_idiom.py
run python3 scripts/check_sv_idiom.py --selftest
run python3 scripts/check_cpp_idiom.py
run python3 scripts/check_cpp_idiom.py --selftest
run python3 scripts/check_py_idiom.py
run python3 scripts/check_py_idiom.py --selftest
run python3 scripts/check_sh_idiom.py
run python3 scripts/check_sh_idiom.py --selftest
run python3 scripts/ci_events.py --check
run python3 scripts/ci_events.py --selftest
run python3 scripts/act_ci.py --selftest
run python3 scripts/check_doc_paths.py
run python3 scripts/check_archive.py
run python3 scripts/check_archive.py --selftest
run python3 scripts/gen_toc.py --selftest
run python3 scripts/gen_toc.py --verify-anchors
run python3 scripts/gen_toc.py --check
run python3 avdecc/gen_aem_store.py --self-test
run python3 scripts/check_sweep_shape.py --self-test
run python3 scripts/check_deploy_shape.py --self-test
run python3 scripts/check_entity_shape.py --self-test
# wire-accountability
run python3 scripts/check_wire_accountability.py --self-test
# docs-check-no-git: the committed tree without git metadata
nogit="$logs/runner-temp/no-git"
rm -rf "$nogit"; mkdir -p "$nogit"
git -C "$tree" archive HEAD | tar -x -C "$nogit"
tree="$nogit"
run python3 scripts/docs_check.py
run python3 scripts/check_feature_status.py
rm -rf "$nogit"
failed=$(awk -F'\t' '$2 != 0' "$summary" | wc -l)
echo "commands: $n, failed: $failed"
[ "$failed" -eq 0 ]
