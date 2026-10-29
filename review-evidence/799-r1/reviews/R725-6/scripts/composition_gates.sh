#!/usr/bin/env bash
# Run the gates that read the files both the PR and the dev predecessor changed,
# concurrently, each with its own log and rc file. Usage: composition_gates.sh <clone> <outdir>
set -u
clone=$1; out=$2; mkdir -p "$out"; cd "$clone" || exit 2
run() { local name=$1; shift; ( "$@" >"$out/$name.log" 2>&1; echo $? >"$out/$name.rc" ) & }
run behave_full            behave --no-capture -f plain
run torture_selftest       python3 -B tb/tools/torture_campaign.py --self-test
run torture_release_mut    python3 -B tb/tools/torture_release_mutants.py
run torture_audio_mut      python3 -B tb/tools/torture_release_audio_mutants.py
run docs_check             python3 scripts/docs_check.py
run doc_style              sh -c 'python3 scripts/check_doc_style.py && python3 scripts/check_doc_style.py --selftest'
run doc_paths              python3 scripts/check_doc_paths.py
run gen_toc                sh -c 'python3 scripts/gen_toc.py --selftest && python3 scripts/gen_toc.py --verify-anchors && python3 scripts/gen_toc.py --check'
run em_dash_vs_dev         python3 scripts/check_em_dash.py --base 5fcec84b1aa72c43048eff28bb63a982add830dd
run em_dash_vs_mergebase   python3 scripts/check_em_dash.py --base 97aab1d0f28bd753a3e11df6278d5cac54f964dd
run feature_status         sh -c 'python3 scripts/check_feature_status.py && python3 scripts/check_feature_status.py --self-test'
run naming                 python3 scripts/measure_naming.py --check
run fail_fast              python3 scripts/measure_fail_fast.py --check
run test_evidence          python3 scripts/measure_test_evidence.py --check
run hygiene                python3 scripts/check_hygiene.py --check
run py_idiom               python3 scripts/check_py_idiom.py
run todo_ownership         python3 scripts/check_todo_ownership.py
run ci_gate_workflows      python3 scripts/ci_gate_workflows.py --check
run ci_events              sh -c 'python3 scripts/ci_events.py --check && python3 scripts/ci_events.py --selftest'
run suite_shards           python3 scripts/suite_shards.py --selftest
run solution_docs          python3 scripts/check_solution_docs.py
run traceability           python3 docs/traceability/gen_module_matrix.py --check
run doc_map                python3 docs/DOC_MAP.gen.py --check
wait
for f in "$out"/*.rc; do printf '%s %s\n' "$(cat "$f")" "$(basename "$f" .rc)"; done | sort -k2 > "$out/SUMMARY.txt"
cat "$out/SUMMARY.txt"
