#!/usr/bin/env bash
# Runs the documentation gates named in the author handoff, concurrently, from a clone at the reviewed head.
# Usage: PYTHONPATH=<pinned renderer from tools/markdown/requirements.txt> run_doc_gates.sh <clone> <receipt-dir>
set -u
clone=$1; out=$2; mkdir -p "$out"; cd "$clone" || exit 9
run() { n=$1; shift; ( "$@" >"$out/$n.log" 2>&1; echo $? >"$out/$n.rc" ) & }
run check_doc_style python3 scripts/check_doc_style.py
run docs_check python3 scripts/docs_check.py
run check_gptp_docs python3 scripts/check_gptp_docs.py
run gen_toc python3 scripts/gen_toc.py --check
run check_em_dash python3 scripts/check_em_dash.py --base 1f29f189279f9fc0132f4918e47342b87d22f33a
run check_feature_status python3 scripts/check_feature_status.py
run check_doc_paths python3 scripts/check_doc_paths.py
run check_baremetal_only python3 scripts/check_baremetal_only.py --check
run ctrl_service_bounds python3 sw/firmware/ctrl/test/ctrl_service_bounds.py
run pp_resource_gate python3 syn/ooc/pp_resource_gate.py check-baseline
run git_diff_check git diff --check d63b378d27..HEAD
wait
cd "$out"; for f in *.rc; do printf '%s %s\n' "${f%.rc}" "$(cat "$f")"; done
