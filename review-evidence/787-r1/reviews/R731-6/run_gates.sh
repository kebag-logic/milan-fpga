#!/usr/bin/env bash
# Run the composition gates on the merge-train candidate checkout.
# Scripts that import sibling modules run without -I (they need the
# script directory on sys.path), as the workflows run them.
# usage: run_gates.sh <checkout> <out-dir> <markdown-python>
set -u
repo=$1; out=$2; mdpy=$3
mkdir -p "$out"
cd "$repo" || exit 2
run() {  # name, command...
  local name=$1; shift
  ( "$@" > "$out/$name.log" 2>&1; echo $? > "$out/$name.rc" ) &
}
run docs_check            "$mdpy" scripts/docs_check.py
run gen_toc_check         "$mdpy" scripts/gen_toc.py --check
run gen_toc_anchors       "$mdpy" scripts/gen_toc.py --verify-anchors
run gen_toc_selftest      "$mdpy" scripts/gen_toc.py --selftest
run em_dash_parent        "$mdpy" scripts/check_em_dash.py --base 125ac68006d124dd149b9161539dfaa787166e62
run em_dash_livedev       "$mdpy" scripts/check_em_dash.py --base e5b8405db4c1f7cbdafb5df92b15b580142e0232
run ci_events_check       python3 scripts/ci_events.py --check
run ci_events_selftest    python3 scripts/ci_events.py --selftest
run ci_gate_workflows     python3 scripts/ci_gate_workflows.py --check
run doc_paths             python3 -I scripts/check_doc_paths.py
run doc_style             python3 -I scripts/check_doc_style.py
run submodule_docs        python3 -I scripts/check_submodule_docs.py
run gptp_docs_sub         python3 -I scripts/check_gptp_docs.py --with-submodule
run gptp_docs             python3 -I scripts/check_gptp_docs.py
run soc_sources           python3 -I scripts/check_soc_sources.py
run solution_docs         python3 -I scripts/check_solution_docs.py
run diagram_pngs          python3 scripts/check_diagram_pngs.py
run feature_status        python3 -I scripts/check_feature_status.py
run port_contracts        python3 -I scripts/check_port_contracts.py
run hygiene               python3 -I scripts/check_hygiene.py --check
run py_idiom              python3 -I scripts/check_py_idiom.py
run rtl_source_lists      python3 -I scripts/check_rtl_source_lists.py
run todo_ownership        python3 -I scripts/check_todo_ownership.py
run diff_check_parent     git diff --check 125ac68006d124dd149b9161539dfaa787166e62 808e64e39c1007e463cf20de892e6dca73bfa2a6
run diff_check_livedev    git diff --check e5b8405db4c1f7cbdafb5df92b15b580142e0232 808e64e39c1007e463cf20de892e6dca73bfa2a6
wait
for f in "$out"/*.rc; do printf '%s rc=%s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done
