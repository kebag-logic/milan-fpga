#!/usr/bin/env bash
# Run the docs-workflow gates touched by the round-2 delta, in parallel.
# Usage: doc_gates.sh <clone> <outdir>
set -u
clone=$1; out=$2; mkdir -p "$out"; cd "$clone" || exit 2
run() { name=$1; shift; ( "$@" >"$out/$name.log" 2>&1; echo $? >"$out/$name.rc" ) & }
run docs_check              python3 scripts/docs_check.py
run em_dash                 python3 scripts/check_em_dash.py --base cdf49d1a28527562888f0a903de51b6b15b1244f
run em_dash_r1              python3 scripts/check_em_dash.py --base 3370c6cbd
run doc_style               python3 scripts/check_doc_style.py
run doc_style_selftest      python3 scripts/check_doc_style.py --selftest
run submodule_docs          python3 scripts/check_submodule_docs.py
run submodule_docs_selftest python3 scripts/check_submodule_docs.py --selftest
run submodule_diagram       python3 docs/diagrams/submodule_boundaries.gen.py --check
run doc_paths               python3 scripts/check_doc_paths.py
run hygiene                 python3 scripts/check_hygiene.py
run sv_idiom                python3 scripts/check_sv_idiom.py
run port_contracts          python3 scripts/check_port_contracts.py
run feature_status          python3 scripts/check_feature_status.py --self-test
run doc_map                 python3 docs/DOC_MAP.gen.py --check
wait
for f in "$out"/*.rc; do printf '%s rc=%s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done
