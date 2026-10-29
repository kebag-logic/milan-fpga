#!/usr/bin/env bash
# Second pass: gates that need the pinned Markdown renderer (private venv), behave
# from tests/ as the workflow runs it, and the release mutants alone.
# Usage: composition_gates_2.sh <clone> <outdir> <venv-python>
set -u
clone=$1; out=$2; py=$3; mkdir -p "$out"; cd "$clone" || exit 2
run() { local name=$1; shift; ( "$@" >"$out/$name.log" 2>&1; echo $? >"$out/$name.rc" ) & }
run behave_full            sh -c 'cd tests && behave --no-capture -f plain'
run torture_release_mut    python3 -B tb/tools/torture_release_mutants.py
run gen_toc                sh -c "$py scripts/gen_toc.py --selftest && $py scripts/gen_toc.py --verify-anchors && $py scripts/gen_toc.py --check"
run em_dash_vs_dev         $py scripts/check_em_dash.py --base 5fcec84b1aa72c43048eff28bb63a982add830dd
run em_dash_vs_mergebase   $py scripts/check_em_dash.py --base 97aab1d0f28bd753a3e11df6278d5cac54f964dd
run docs_check_venv        $py scripts/docs_check.py
wait
for f in "$out"/*.rc; do printf '%s %s\n' "$(cat "$f")" "$(basename "$f" .rc)"; done | sort -k2 > "$out/SUMMARY.txt"
cat "$out/SUMMARY.txt"
