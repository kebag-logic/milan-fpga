#!/usr/bin/env bash
# Run the repository gates that read docs/testing/CI_WORKFLOWS.md or
# scripts/act_ci.py on a composed candidate tree, concurrently, one log and
# one rc file per gate. Does not execute scripts/act_ci.py.
# usage: run_gates.sh <candidate clone> <receipt dir> <composed parent> <live dev> <PR base>
set -uo pipefail
repo=$1 out=$2 parent=$3 dev=$4 prbase=$5
mkdir -p "$out"
cd "$repo"
gate() {
  local name=$1; shift
  ( "$@" >"$out/$name.log" 2>&1; echo $? >"$out/$name.rc" ) &
}
gate docs_check python3 scripts/docs_check.py
gate check_doc_style python3 scripts/check_doc_style.py
gate check_doc_style_selftest python3 scripts/check_doc_style.py --selftest
gate gen_toc_check python3 scripts/gen_toc.py --check
gate gen_toc_verify_anchors python3 scripts/gen_toc.py --verify-anchors
gate check_doc_paths python3 scripts/check_doc_paths.py
gate em_dash_parent python3 scripts/check_em_dash.py --base "$parent"
gate em_dash_dev python3 scripts/check_em_dash.py --base "$dev"
gate em_dash_prbase python3 scripts/check_em_dash.py --base "$prbase"
gate ci_events_check python3 scripts/ci_events.py --check
gate ci_events_selftest python3 scripts/ci_events.py --selftest
gate check_py_idiom python3 scripts/check_py_idiom.py
gate check_py_idiom_selftest python3 scripts/check_py_idiom.py --selftest
gate check_baremetal_only python3 scripts/check_baremetal_only.py --check
gate check_baremetal_only_selftest python3 scripts/check_baremetal_only.py --selftest
gate measure_naming python3 scripts/measure_naming.py --check
gate measure_fail_fast python3 scripts/measure_fail_fast.py --check
gate measure_test_evidence python3 scripts/measure_test_evidence.py --check
gate check_hygiene python3 scripts/check_hygiene.py --check
gate check_todo_ownership python3 scripts/check_todo_ownership.py
gate doc_map_check python3 docs/DOC_MAP.gen.py --check
gate check_archive python3 scripts/check_archive.py
gate git_diff_check git -c core.pager=cat diff --check "$parent" HEAD
wait
for rc in "$out"/*.rc; do printf '%s %s\n' "$(basename "$rc" .rc)" "$(cat "$rc")"; done | tee "$out/SUMMARY.txt"
