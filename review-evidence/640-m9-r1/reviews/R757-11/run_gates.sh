#!/usr/bin/env bash
# Runs the documentation gates and page readers for this delta, concurrently, in the exact-head clone.
# Usage: run_gates.sh <clone> <log-dir> <dir-with-pinned-markdown-renderer>
set -u
clone=$1; logs=$2; md=$3; cd "$clone" || exit 2
export PYTHONDONTWRITEBYTECODE=1
base=1f29f189279f9fc0132f4918e47342b87d22f33a
run() { local n=$1; shift; ( "$@" >"$logs/$n.log" 2>&1; echo $? >"$logs/$n.rc" ) & }
run doc_style python3 scripts/check_doc_style.py
run docs_check env PYTHONPATH="$md" python3 scripts/docs_check.py
run gptp_docs python3 scripts/check_gptp_docs.py
run gen_toc env PYTHONPATH="$md" python3 scripts/gen_toc.py --check
run toc_anchors env PYTHONPATH="$md" python3 scripts/gen_toc.py --verify-anchors
run em_dash env PYTHONPATH="$md" python3 scripts/check_em_dash.py --base "$base"
run feature_status python3 scripts/check_feature_status.py
run doc_paths python3 scripts/check_doc_paths.py
run baremetal python3 scripts/check_baremetal_only.py --check
run solution_docs python3 scripts/check_solution_docs.py
run module_matrix python3 docs/traceability/gen_module_matrix.py --check
run ctrl_bounds env PYTHONPATH=sw/firmware/gtest python3 sw/firmware/ctrl/test/ctrl_service_bounds.py
run resource_baseline python3 syn/ooc/pp_resource_gate.py check-baseline
run diff_check git diff --check "$base" HEAD
wait
for f in "$logs"/*.rc; do printf '%s rc=%s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done
