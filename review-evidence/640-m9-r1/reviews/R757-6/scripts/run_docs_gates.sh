#!/usr/bin/env bash
# Runs the docs workflow's document gates concurrently at the checked-out head.
# Usage: run_docs_gates.sh <clone> <receipt dir>; TMPDIR is the caller's.
cd "$1" || exit 2
G=$2
export PYTHONDONTWRITEBYTECODE=1
BASE=$(git merge-base 1f29f189279f9fc0132f4918e47342b87d22f33a HEAD)
run(){ n=$1; shift; ( bash -c "$*" >"$G/$n.log" 2>&1; echo $? >"$G/$n.rc" ) & }
run docs_check "python3 scripts/docs_check.py"
run em_dash "python3 scripts/check_em_dash.py --base $BASE"
run doc_style "python3 scripts/check_doc_style.py && python3 scripts/check_doc_style.py --selftest"
run gptp_docs "python3 scripts/check_gptp_docs.py && python3 scripts/check_gptp_docs.py --selftest"
run doc_map "python3 docs/DOC_MAP.gen.py --check && python3 docs/DOC_MAP.gen.py --selftest"
run timesync "python3 docs/diagrams/timesync_chain.gen.py --check && python3 docs/diagrams/timesync_chain.gen.py --selftest"
run solution "python3 scripts/check_solution_docs.py && python3 scripts/check_solution_docs.py --selftest"
run submodule_diag "python3 docs/diagrams/submodule_boundaries.gen.py --check && python3 docs/diagrams/submodule_boundaries.gen.py --selftest"
run submodule_docs "python3 scripts/check_submodule_docs.py && python3 scripts/check_submodule_docs.py --selftest"
run wavedrom "python3 scripts/gen_wavedrom.py --selftest"
run pngs "python3 scripts/check_diagram_pngs.py && python3 scripts/check_diagram_pngs.py --selftest"
run feature "python3 scripts/check_feature_status.py --self-test"
run traceability "python3 docs/traceability/gen_module_matrix.py --check"
run baremetal "python3 scripts/check_baremetal_only.py --check && python3 scripts/check_baremetal_only.py --selftest"
run doc_paths "python3 scripts/check_doc_paths.py"
run archive "python3 scripts/check_archive.py && python3 scripts/check_archive.py --selftest"
run toc "python3 scripts/gen_toc.py --selftest && python3 scripts/gen_toc.py --verify-anchors && python3 scripts/gen_toc.py --check"
run diff_check "git diff --check $BASE HEAD"
wait
