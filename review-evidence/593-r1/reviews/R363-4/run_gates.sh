#!/usr/bin/env bash
# Composition gates for the #593 merge-train candidate. Usage: run_gates.sh <clone> <outdir>
set -u
C="$1"; O="$2"; mkdir -p "$O"; cd "$C" || exit 2
run() { n="$1"; shift; "$@" > "$O/$n.log" 2>&1; rc=$?; printf '%s\trc=%s\t%s\n' "$n" "$rc" "$*" | tee -a "$O/summary.tsv"; }
: > "$O/summary.tsv"
run head git rev-parse HEAD HEAD^{tree}
run docs_check python3 -B scripts/docs_check.py
run gen_toc_check python3 -B scripts/gen_toc.py --check
run gen_toc_anchors python3 -B scripts/gen_toc.py --verify-anchors
run gen_toc_selftest python3 -B scripts/gen_toc.py --selftest
run em_dash_vs_train python3 -B scripts/check_em_dash.py --base 1304205cfc9fa4c9e69a32130fb366895c5f883b
run em_dash_vs_prbase python3 -B scripts/check_em_dash.py --base 6d5ebd7357c1e468e446f18a61527c5be6118a04
run em_dash_selftest python3 -B scripts/check_em_dash.py --selftest
run doc_style python3 -B scripts/check_doc_style.py
run doc_paths python3 -B scripts/check_doc_paths.py
run archive python3 -B scripts/check_archive.py
run feature_status_selftest python3 -B scripts/check_feature_status.py --self-test
run gptp_docs python3 -B scripts/check_gptp_docs.py
run solution_docs python3 -B scripts/check_solution_docs.py
run submodule_docs python3 -B scripts/check_submodule_docs.py
run py_idiom python3 -B scripts/check_py_idiom.py
run hygiene python3 -B scripts/check_hygiene.py
run todo_ownership python3 -B scripts/check_todo_ownership.py
run ci_scope_selftest python3 -B scripts/ci_scope.py --selftest
run baremetal_check python3 -B scripts/check_baremetal_only.py --check
run ci_events_check python3 -B scripts/ci_events.py --check
run diff_check_train git diff --check 1304205cfc9fa4c9e69a32130fb366895c5f883b HEAD
run planner_selftest python3 -B tb/tools/torture_campaign.py --self-test
run release_mutants python3 -B tb/tools/torture_release_mutants.py
run behave_plan python3 -B -m behave tests/features/torture_campaign_plan.feature -f progress
