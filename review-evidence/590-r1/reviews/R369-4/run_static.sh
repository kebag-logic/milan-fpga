#!/usr/bin/env bash
# Run the docs-workflow static gates on the checkout in $PWD, one log per gate.
# Usage: run_static.sh <out-dir> <em-dash-base-rev>
# `python3` must be the interpreter carrying tools/markdown/requirements.txt.
set -uo pipefail
out="$1"; base="$2"
mkdir -p "$out"
summary="$out/SUMMARY.txt"
: > "$summary"
run() {
    local name="$1"; shift
    local start=$SECONDS
    "$@" > "$out/$name.log" 2>&1
    local rc=$?
    printf '%-44s rc=%d %4ds  %s\n' "$name" "$rc" "$((SECONDS - start))" "$*" >> "$summary"
}
run docs_check            python3 scripts/docs_check.py
run em_dash_base          python3 scripts/check_em_dash.py --base "$base"
run em_dash_selftest      python3 scripts/check_em_dash.py --selftest
run doc_style             python3 scripts/check_doc_style.py
run doc_style_selftest    python3 scripts/check_doc_style.py --selftest
run doc_paths             python3 scripts/check_doc_paths.py
run gen_toc_check         python3 scripts/gen_toc.py --check
run gen_toc_anchors       python3 scripts/gen_toc.py --verify-anchors
run gen_toc_selftest      python3 scripts/gen_toc.py --selftest
run doc_map_check         python3 docs/DOC_MAP.gen.py --check
run solution_docs         python3 scripts/check_solution_docs.py
run feature_status        python3 scripts/check_feature_status.py
run ci_events_check       python3 scripts/ci_events.py --check
run ci_events_selftest    python3 scripts/ci_events.py --selftest
run ci_scope_selftest     python3 scripts/ci_scope.py --selftest
run baremetal_only        python3 scripts/check_baremetal_only.py --check
run baremetal_only_self   python3 scripts/check_baremetal_only.py --selftest
run nvm_record_space      python3 scripts/check_nvm_record_space.py
run nvm_capture           python3 scripts/check_nvm_capture.py
run soc_sources           python3 scripts/check_soc_sources.py
run rtl_source_lists      python3 scripts/check_rtl_source_lists.py
run naming_check          python3 scripts/measure_naming.py --check
run port_contracts        python3 scripts/check_port_contracts.py
run fail_fast_check       python3 scripts/measure_fail_fast.py --check
run todo_ownership        python3 scripts/check_todo_ownership.py
run test_evidence_check   python3 scripts/measure_test_evidence.py --check
run hygiene_check         python3 scripts/check_hygiene.py --check
run sv_idiom              python3 scripts/check_sv_idiom.py
run cpp_idiom             python3 scripts/check_cpp_idiom.py
run py_idiom              python3 scripts/check_py_idiom.py
run sh_idiom              python3 scripts/check_sh_idiom.py
run archive               python3 scripts/check_archive.py
run fw_compiler_selftest  python3 sw/builder/test_firmware_compiler.py --selftest
run fw_compiler_absent    python3 sw/builder/test_firmware_compiler.py --absent --audit "$out/rv32-absent.jsonl"
run diff_check_vs_dev     git diff --check "$base" HEAD
cat "$summary"
