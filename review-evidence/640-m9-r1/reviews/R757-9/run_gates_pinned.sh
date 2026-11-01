#!/usr/bin/env bash
# Runs the renderer-dependent and submodule-dependent gates with the pinned Markdown renderer.
# usage: run_gates_pinned.sh <clone_with_submodules> <python> <out_dir> <base_rev>
clone=$1; py=$2; out=$3; base=$4
cd "$clone" || exit 2
export PYTHONDONTWRITEBYTECODE=1
run() { local n=$1; shift; ( "$@" >"$out/$n.log" 2>&1; echo $? >"$out/$n.rc" ) & }
run em_dash_parent      "$py" scripts/check_em_dash.py --base "$base"
run em_dash_self        "$py" scripts/check_em_dash.py --selftest
run toc_check           "$py" scripts/gen_toc.py --check
run toc_anchors         "$py" scripts/gen_toc.py --verify-anchors
run toc_self            "$py" scripts/gen_toc.py --selftest
run hygiene             "$py" scripts/check_hygiene.py --check
run todo_ownership      "$py" scripts/check_todo_ownership.py
run wire_accountability "$py" scripts/check_wire_accountability.py
run wire_account_self   "$py" scripts/check_wire_accountability.py --self-test
run gptp_docs_sub       "$py" scripts/check_gptp_docs.py --with-submodule
wait
