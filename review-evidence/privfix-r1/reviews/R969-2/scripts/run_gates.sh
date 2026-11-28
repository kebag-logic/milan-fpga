#!/usr/bin/env bash
# Run focused reviewer gates at the checked-out head concurrently; one log and rc per gate.
# MDPY: interpreter carrying the pinned renderer (tools/markdown/requirements.txt); the renderer gates refuse without it.
# Usage: run_gates.sh <repo> <outdir> <base>
set -u
repo=$1 out=$2 base=$3
mkdir -p "$out"
cd "$repo" || exit 2
run() { local name=$1; shift; ( "$@" >"$out/$name.log" 2>&1; echo $? >"$out/$name.rc" ) & }
run em_dash        "${MDPY:-python3}" scripts/check_em_dash.py --base "$base"
run em_dash_self   "${MDPY:-python3}" scripts/check_em_dash.py --selftest
run doc_style      python3 scripts/check_doc_style.py
run docs_check     python3 scripts/docs_check.py
run toc_check      "${MDPY:-python3}" scripts/gen_toc.py --check
run toc_anchors    "${MDPY:-python3}" scripts/gen_toc.py --verify-anchors
run doc_paths      python3 scripts/check_doc_paths.py
run docs_inventory python3 scripts/docs_inventory.py --check
run hygiene        python3 scripts/check_hygiene.py --check
run py_idiom       python3 scripts/check_py_idiom.py
run sh_syntax      bash -n tb/tools/check_tu_on_wire.sh
run avtp_wire_truth python3 tb/tools/avtp_wire_truth.py --self-test
run torture        python3 tb/tools/torture_campaign.py --self-test
run baremetal_check python3 scripts/check_baremetal_only.py --check
run baremetal_self python3 scripts/check_baremetal_only.py --selftest
run behave_touched sh -c 'cd tests && behave --no-capture -f progress features/milan_streaming_licence.feature features/torture_campaign_plan.feature features/wire_truth_avtp.feature'
run behave_full    sh -c 'cd tests && behave -f progress'
run doc_map "${MDPY:-python3}" docs/DOC_MAP.gen.py --check
run register_reference "${MDPY:-python3}" scripts/gen_register_reference.py --check
wait
for f in "$out"/*.rc; do printf '%s\t%s\t%s\n' "$(basename "$f" .rc)" "$(cat "$f")" "$(grep -v '^\s*$' "${f%.rc}.log" | tail -1 | cut -c1-200)"; done
