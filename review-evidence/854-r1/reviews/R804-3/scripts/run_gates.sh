#!/usr/bin/env bash
# Run the round 3 gates at the checked-out head: drops-mutant (concurrently) and
# the docs.yml steps that read the changed files, each with its own rc.
# Usage: run_gates.sh <clone> <receipts dir> <python with the pinned renderer> <verilator>
set -u
C=$1; R=$2; PY=$3; V=$4
cd "$C"
( cd tb/verilator/pp_shadow && VERILATOR="$V" timeout 3000 python3 drops_mutant.py > "$R/drops_mutant.log" 2>&1; echo $? > "$R/drops_mutant.rc" ) &
step() { name=$1; shift; out=$("$@" 2>&1); rc=$?; printf '== %s (rc %d): %s\n%s\n' "$name" "$rc" "$*" "$(printf '%s' "$out" | tail -n 4)" >> "$R/docs_gates.log"; echo "$rc $name" >> "$R/docs_gates.rc"; }
: > "$R/docs_gates.log"; : > "$R/docs_gates.rc"
step docs_check $PY scripts/docs_check.py
step em_dash $PY scripts/check_em_dash.py --base ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36
step doc_style $PY scripts/check_doc_style.py
step doc_style_selftest $PY scripts/check_doc_style.py --selftest
step gptp_docs $PY scripts/check_gptp_docs.py
step doc_map $PY docs/DOC_MAP.gen.py --check
step solution_docs $PY scripts/check_solution_docs.py
step feature_status $PY scripts/check_feature_status.py
step feature_status_selftest $PY scripts/check_feature_status.py --self-test
step traceability $PY docs/traceability/gen_module_matrix.py --check
step test_evidence $PY scripts/measure_test_evidence.py --check
step hygiene $PY scripts/check_hygiene.py --check
step py_idiom $PY scripts/check_py_idiom.py
step doc_paths $PY scripts/check_doc_paths.py
step archive $PY scripts/check_archive.py
step toc_anchors $PY scripts/gen_toc.py --verify-anchors
step toc_check $PY scripts/gen_toc.py --check
step docs_inventory $PY scripts/docs_inventory.py --check
step diff_check_base git diff --check ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36 HEAD
step diff_check_delta git diff --check de71984e4fc1b568065dffec483ea3ff51518604 HEAD
step resource_check_baseline $PY syn/ooc/pp_resource_gate.py check-baseline
wait
