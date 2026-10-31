#!/usr/bin/env bash
# Composition gates for PR #820 (#818) on merge-train candidate 125ac680.
# Usage: composition_gates.sh <candidate-clone> <receipt-dir> <markdown-renderer-python>
# Runs each gate concurrently with its own log and rc file, then waits.
set -u
clone=$1; out=$2; md=$3
parent=7f4d7eeaa1773099f72edb3830bd9f8ab2b5c22c
srcbase=02ca829ad821f4233ab66f59978c65d3c3c9de70
cd "$clone" || exit 2
mkdir -p "$out"
run() { n=$1; shift; ( "$@" > "$out/$n.log" 2>&1; echo $? > "$out/$n.rc" ) & }
run docs_check python3 scripts/docs_check.py
run doc_style python3 scripts/check_doc_style.py
run doc_paths python3 scripts/check_doc_paths.py
run submodule_docs python3 scripts/check_submodule_docs.py
run gen_toc_check "$md" scripts/gen_toc.py --check
run gen_toc_anchors "$md" scripts/gen_toc.py --verify-anchors
run gen_toc_selftest "$md" scripts/gen_toc.py --selftest
run em_dash_base_parent "$md" scripts/check_em_dash.py --base "$parent"
run em_dash_base_srcbase "$md" scripts/check_em_dash.py --base "$srcbase"
run ci_events_check python3 scripts/ci_events.py --check
run ci_events_selftest python3 scripts/ci_events.py --selftest
run hygiene_check python3 scripts/check_hygiene.py --check
run py_idiom python3 scripts/check_py_idiom.py
run evidence_pins python3 scripts/generate_ci_evidence_pins.py --check
run gate_selftest python3 syn/ooc/pp_resource_gate_selftest.py
run gate_selftest_documented python3 syn/ooc/pp_resource_gate.py --selftest
run gate_check_baseline python3 syn/ooc/pp_resource_gate.py check-baseline
run gate_mutants python3 syn/ooc/pp_resource_gate_mutants.py
wait
for f in "$out"/*.rc; do echo "$(basename "$f" .rc) rc=$(cat "$f")"; done
# Restore: drop interpreter caches the gates leave behind.
find scripts syn -name __pycache__ -type d -prune -exec rm -rf {} +
git status --short --ignored
