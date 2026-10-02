#!/usr/bin/env bash
# Local replica of .github/workflows/docs.yml's docs-check and
# wire-accountability gate steps at the checked-out head, one rc line per
# command. Install steps are omitted; two steps are deliberately not run here:
# `make -C gptp-processor docs` (it writes into the submodule checkout) and
# `scripts/act_ci.py --selftest` (the candidate's runner may self-test only
# inside the disposable CI job). Markdown-renderer gates use the pinned venv.
# Usage: docs_check_replica.sh <repo> <base> <logdir>
set -u
repo=$1; base=$2; logs=$3
MD=$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python
# wavedrom==2.0.3.post3, the version the workflow installs, in a scratch venv
WD=${WD_PY:-python3}
mkdir -p "$logs"
cd "$repo" || exit 2
n=0; fails=0
step() {
  n=$((n + 1))
  local log; log=$(printf '%s/%02d.log' "$logs" "$n")
  "$@" > "$log" 2>&1
  local rc=$?
  [ "$rc" -eq 0 ] || fails=$((fails + 1))
  printf 'rc=%d  %s\n' "$rc" "$*"
}
step "$MD" scripts/docs_check.py
step "$MD" scripts/check_em_dash.py --base "$base"
step "$MD" scripts/check_em_dash.py --selftest
step "$MD" scripts/check_doc_style.py
step "$MD" scripts/check_doc_style.py --selftest
step python3 scripts/check_gptp_docs.py
step python3 scripts/check_gptp_docs.py --selftest
step python3 docs/DOC_MAP.gen.py --check
step python3 docs/DOC_MAP.gen.py --selftest
step python3 docs/diagrams/timesync_chain.gen.py --check
step python3 docs/diagrams/timesync_chain.gen.py --selftest
step python3 scripts/check_solution_docs.py
step python3 scripts/check_solution_docs.py --selftest
step python3 docs/diagrams/submodule_boundaries.gen.py --check
step python3 docs/diagrams/submodule_boundaries.gen.py --selftest
step python3 scripts/check_submodule_docs.py
step python3 scripts/check_submodule_docs.py --selftest
step "$WD" scripts/gen_wavedrom.py --selftest
step "$WD" scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check
step "$WD" scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check
step "$WD" scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check
step python3 scripts/check_diagram_pngs.py
step python3 scripts/check_diagram_pngs.py --selftest
step python3 scripts/check_feature_status.py --self-test
step python3 docs/traceability/gen_module_matrix.py --check
step python3 scripts/check_gptp_docs.py --with-submodule
step python3 scripts/measure_control_flow.py --selftest
step python3 scripts/measure_cohesion.py --selftest
step python3 scripts/check_baremetal_only.py --check
step python3 scripts/check_baremetal_only.py --selftest
step python3 sw/builder/test_firmware_compiler.py --selftest
step python3 scripts/check_nvm_record_space.py
step python3 scripts/check_nvm_record_space.py --self-test
step python3 scripts/check_nvm_capture.py
step python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
step python3 scripts/check_soc_sources.py
step python3 scripts/check_soc_sources.py --selftest
step python3 sw/litex/iob_pack_selftest.py
step python3 scripts/check_rtl_source_lists.py
step python3 scripts/check_rtl_source_lists.py --selftest
step python3 scripts/measure_naming.py --check
step python3 scripts/measure_naming.py --selftest
step python3 scripts/check_port_contracts.py
step python3 scripts/check_port_contracts.py --selftest
step python3 scripts/measure_fail_fast.py --check
step python3 scripts/measure_fail_fast.py --selftest
step python3 scripts/check_todo_ownership.py
step python3 scripts/check_todo_ownership.py --selftest
step python3 scripts/measure_test_evidence.py --check
step python3 scripts/measure_test_evidence.py --selftest
step python3 scripts/check_hygiene.py --check
step python3 scripts/check_hygiene.py --selftest
step python3 scripts/check_sv_idiom.py
step python3 scripts/check_sv_idiom.py --selftest
step python3 scripts/check_cpp_idiom.py
step python3 scripts/check_cpp_idiom.py --selftest
step python3 scripts/check_py_idiom.py
step python3 scripts/check_py_idiom.py --selftest
step python3 scripts/check_sh_idiom.py
step python3 scripts/check_sh_idiom.py --selftest
step python3 scripts/ci_events.py --check
step python3 scripts/ci_events.py --selftest
step "$MD" scripts/check_doc_paths.py
step python3 scripts/check_archive.py
step python3 scripts/check_archive.py --selftest
step "$MD" scripts/gen_toc.py --selftest
step "$MD" scripts/gen_toc.py --verify-anchors
step "$MD" scripts/gen_toc.py --check
step python3 avdecc/gen_aem_store.py --self-test
step python3 scripts/check_sweep_shape.py --self-test
step python3 scripts/check_deploy_shape.py --self-test
step python3 scripts/check_entity_shape.py
step python3 scripts/check_entity_shape.py --self-test
step python3 scripts/check_wire_accountability.py --self-test
step python3 scripts/check_feature_status.py
step git diff --check
step git diff --check "$base" HEAD
echo "steps: $n  failing: $fails"
[ "$fails" -eq 0 ]
