#!/usr/bin/env bash
# Run every docs.yml gate command (installs excluded) from one checkout; one log and rc per gate.
# Usage: docs_gates.sh SIDE CHECKOUT EM_DASH_BASE
set -u
side=$1; checkout=$2; emb=$3
root=$SCRATCH
out=$root/docs/$side
rm -rf "$out"; mkdir -p "$out"
export PATH=$root/venv312/bin:$PATH TMPDIR=$root/tmp PYTHONDONTWRITEBYTECODE=1
export MILAN_RV32_CC=$SDK/bin/riscv32-linux-gcc
cd "$checkout" || exit 2
n=0
gate() {
  n=$((n + 1)); local name; name=$(printf '%02d' $n)
  echo "== $*" > "$out/$name.log"
  local t0=$SECONDS
  timeout 3600 bash -c "$*" >> "$out/$name.log" 2>&1
  local rc=$?
  printf '%s\trc=%s\t%ss\t%s\n' "$name" "$rc" "$((SECONDS - t0))" "$*" >> "$out/summary.tsv"
}
: > "$out/summary.tsv"
echo "python: $(python3 --version) $(command -v python3)" > "$out/env.txt"
gate python3 scripts/gen_hdl_reference.py --selftest
gate python3 scripts/gen_hdl_reference.py --output "$out/hdlref"
gate python3 scripts/docs_check.py
gate python3 scripts/check_em_dash.py --base "$emb"
gate python3 scripts/check_doc_style.py
gate python3 scripts/check_doc_style.py --selftest
gate python3 scripts/check_gptp_docs.py
gate python3 scripts/check_gptp_docs.py --selftest
gate python3 docs/DOC_MAP.gen.py --check
gate python3 docs/DOC_MAP.gen.py --selftest
gate python3 docs/diagrams/timesync_chain.gen.py --check
gate python3 docs/diagrams/timesync_chain.gen.py --selftest
gate python3 scripts/check_solution_docs.py
gate python3 scripts/check_solution_docs.py --selftest
gate python3 docs/diagrams/submodule_boundaries.gen.py --check
gate python3 docs/diagrams/submodule_boundaries.gen.py --selftest
gate python3 scripts/check_submodule_docs.py
gate python3 scripts/check_submodule_docs.py --selftest
gate python3 scripts/gen_wavedrom.py --selftest
gate python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check
gate python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check
gate python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check
gate python3 scripts/check_diagram_pngs.py
gate python3 scripts/check_diagram_pngs.py --selftest
gate python3 scripts/check_feature_status.py --self-test
gate python3 docs/traceability/gen_module_matrix.py --check
gate python3 scripts/check_gptp_docs.py --with-submodule
gate make -C gptp-processor docs
gate python3 scripts/measure_control_flow.py --selftest
gate python3 scripts/measure_cohesion.py --selftest
gate python3 scripts/check_baremetal_only.py --check
gate python3 scripts/check_baremetal_only.py --selftest
gate python3 scripts/ci_rv32_sdk_selftest.py
gate python3 sw/builder/test_firmware_compiler.py --selftest
gate python3 sw/builder/test_firmware_compiler.py --absent --audit "$out/rv32-absent.jsonl"
gate python3 sw/builder/test_builder.py --require-rv32
gate python3 scripts/check_nvm_record_space.py
gate python3 scripts/check_nvm_record_space.py --self-test
gate python3 scripts/check_nvm_capture.py
gate python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
gate python3 scripts/check_soc_sources.py
gate python3 scripts/check_soc_sources.py --selftest
gate python3 sw/litex/iob_pack_selftest.py
gate python3 scripts/check_rtl_source_lists.py
gate python3 scripts/check_rtl_source_lists.py --selftest
gate python3 scripts/measure_naming.py --check
gate python3 scripts/measure_naming.py --selftest
gate python3 scripts/check_port_contracts.py
gate python3 scripts/check_port_contracts.py --selftest
gate python3 scripts/measure_fail_fast.py --check
gate python3 scripts/measure_fail_fast.py --selftest
gate python3 scripts/check_todo_ownership.py
gate python3 scripts/check_todo_ownership.py --selftest
gate python3 scripts/measure_test_evidence.py --check
gate python3 scripts/measure_test_evidence.py --selftest
gate python3 scripts/check_hygiene.py --check
gate python3 scripts/check_hygiene.py --selftest
gate python3 scripts/check_sv_idiom.py
gate python3 scripts/check_sv_idiom.py --selftest
gate python3 scripts/check_cpp_idiom.py
gate python3 scripts/check_cpp_idiom.py --selftest
gate python3 scripts/check_py_idiom.py
gate python3 scripts/check_py_idiom.py --selftest
gate python3 scripts/check_sh_idiom.py
gate python3 scripts/check_sh_idiom.py --selftest
gate python3 scripts/ci_events.py --check
gate python3 scripts/ci_events.py --selftest
gate python3 scripts/act_ci.py --selftest
gate python3 scripts/check_doc_paths.py
gate python3 scripts/check_archive.py
gate python3 scripts/check_archive.py --selftest
gate python3 scripts/gen_toc.py --selftest
gate python3 scripts/gen_toc.py --verify-anchors
gate python3 scripts/gen_toc.py --check
gate python3 avdecc/gen_aem_store.py --self-test
gate python3 scripts/check_sweep_shape.py --self-test
gate python3 scripts/check_deploy_shape.py --self-test
gate python3 scripts/check_entity_shape.py --self-test
gate python3 scripts/check_wire_accountability.py --self-test
nogit=$root/docs/$side-nogit; rm -rf "$nogit"; mkdir -p "$nogit"
git archive HEAD | tar -x -C "$nogit"
gate "cd '$nogit' && python3 scripts/docs_check.py"
gate "cd '$nogit' && python3 scripts/check_feature_status.py"
echo "clean=$(git status --porcelain --untracked-files=all | wc -l)" >> "$out/summary.tsv"
git status --porcelain --untracked-files=all > "$out/status-after.txt"
echo done >> "$out/summary.tsv"
