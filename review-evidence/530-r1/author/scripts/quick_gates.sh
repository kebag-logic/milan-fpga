#!/usr/bin/env bash
# Quick repository gates (no simulation). Usage: quick_gates.sh <receipt-file>
set -u
cd $LANES/530-crf-talker-licence
BASE=50e78097564244c124e1ec30dd8821f83951ab06
out="$1"; : > "$out"
run() { echo "=== $*" >> "$out"; "$@" >> "$out" 2>&1; rc=$?; echo "=== rc=$rc  $*" >> "$out"; printf '%-70s rc=%s\n' "$*" "$rc"; }
echo "HEAD $(git rev-parse HEAD)  tree $(git rev-parse HEAD^{tree})  dirty=$(git status --porcelain | wc -l)" | tee -a "$out"
run python3 scripts/check_submodule_docs.py
run python3 docs/diagrams/submodule_boundaries.gen.py --check
run python3 scripts/check_diagram_pngs.py
run python3 scripts/docs_check.py
run python3 scripts/check_em_dash.py --base $BASE
run python3 scripts/check_doc_style.py
run python3 scripts/gen_toc.py --check
run python3 scripts/gen_toc.py --verify-anchors
run python3 scripts/check_doc_paths.py
run python3 scripts/check_feature_status.py
run python3 docs/traceability/gen_module_matrix.py --check
run python3 docs/DOC_MAP.gen.py --check
run python3 scripts/check_hygiene.py --check
run python3 scripts/pp_srcs.py --check
run python3 scripts/check_rtl_source_lists.py
run python3 scripts/measure_naming.py --check
run python3 scripts/check_port_contracts.py
run python3 scripts/measure_fail_fast.py --check
run python3 scripts/measure_test_evidence.py --check
run python3 scripts/check_todo_ownership.py
run python3 scripts/check_sv_idiom.py
run python3 scripts/check_cpp_idiom.py
run python3 scripts/check_py_idiom.py
run python3 scripts/check_sh_idiom.py
run python3 scripts/xvlog_gate.py --check
run git diff --check $BASE
