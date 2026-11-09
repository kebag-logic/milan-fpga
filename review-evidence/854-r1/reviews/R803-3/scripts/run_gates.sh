#!/usr/bin/env bash
# Run docs.yml gates whose inputs the round-3 delta touches, one receipt per gate.
# Usage: run_gates.sh <clone> <receipt-dir> <base-sha>
set -u
clone=$1; out=$2; base=$3
mkdir -p "$out"
cd "$clone" || exit 2
g() { name=$1; shift; "$@" >"$out/$name.log" 2>&1; rc=$?; echo $rc >"$out/$name.rc"; printf '%-34s rc=%s\n' "$name" "$rc"; }
g docs_check            python3 scripts/docs_check.py
g check_feature_status  python3 scripts/check_feature_status.py
g em_dash               python3 scripts/check_em_dash.py --base "$base"
g doc_style             python3 scripts/check_doc_style.py
g doc_style_selftest    python3 scripts/check_doc_style.py --selftest
g gptp_docs             python3 scripts/check_gptp_docs.py
g doc_paths             python3 scripts/check_doc_paths.py
g archive               python3 scripts/check_archive.py
g toc_anchors           python3 scripts/gen_toc.py --verify-anchors
g toc_check             python3 scripts/gen_toc.py --check
g docs_inventory_check  python3 scripts/docs_inventory.py --check
g docs_inventory_selftest python3 scripts/docs_inventory.py --selftest
g doc_map_check         python3 docs/DOC_MAP.gen.py --check
g traceability_check    python3 docs/traceability/gen_module_matrix.py --check
g hygiene_check         python3 scripts/check_hygiene.py --check
g py_idiom              python3 scripts/check_py_idiom.py
g fail_fast_check       python3 scripts/measure_fail_fast.py --check
g test_evidence_check   python3 scripts/measure_test_evidence.py --check
g naming_check          python3 scripts/measure_naming.py --check
g todo_ownership        python3 scripts/check_todo_ownership.py
g solution_docs         python3 scripts/check_solution_docs.py
g diff_check            git diff --check "$base" HEAD
