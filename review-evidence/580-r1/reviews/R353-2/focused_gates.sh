#!/bin/bash
# Focused head gates, each through rr.py with its own receipt.
# Usage: focused_gates.sh <repo> <markdown-python>
set -u
R=$1; MD=$2; P=$(cd "$(dirname "$0")" && pwd)
run() { local n=$1; shift; (cd "$R" && timeout 3000 python3 "$P/rr.py" "$n" "$R" -- "$@"); }
run test-declarations python3 sw/builder/test_declarations.py
run docs-check python3 scripts/docs_check.py
run doc-style python3 scripts/check_doc_style.py
run submodule-docs python3 scripts/check_submodule_docs.py
run doc-paths python3 scripts/check_doc_paths.py
run boundaries-diagram-check python3 docs/diagrams/submodule_boundaries.gen.py --check
run diagram-pngs python3 scripts/check_diagram_pngs.py
run doc-map-check python3 docs/DOC_MAP.gen.py --check
run port-contracts python3 scripts/check_port_contracts.py
run test-evidence-check python3 scripts/measure_test_evidence.py --check
run gen-toc-check "$MD" scripts/gen_toc.py --check
run gen-toc-anchors "$MD" scripts/gen_toc.py --verify-anchors
run em-dash-vs-dev "$MD" scripts/check_em_dash.py --base 2a2a7bb655e528edc3087c88033cd3a47546feb4
run em-dash-vs-source-base "$MD" scripts/check_em_dash.py --base 682ecf0cb995473b72d5b4921088053ba753fc93
run diff-check-vs-dev git diff --check 2a2a7bb655e528edc3087c88033cd3a47546feb4 HEAD
run diff-check-vs-lane git diff --check d02db63c367daf9adc7d709840bd81077e781d80 HEAD
