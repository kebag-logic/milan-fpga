#!/usr/bin/env bash
# Replay the docs-check job's tool-light commands (docs.yml order, before its submodule fetch) in a tree
# whose submodules are NOT initialised; one rc line per command. usage: docs_replay.sh TREE BASE_SHA
T=$1; BASE=$2; cd "$T" || exit 2
run() { "$@" > /dev/null 2>"$OUT.err.tmp"; rc=$?; echo "rc=$rc :: $*"; [ $rc -ne 0 ] && sed 's/^/    /' "$OUT.err.tmp" | tail -n 4; }
OUT=$(mktemp)
run python3 scripts/docs_check.py
run python3 scripts/check_em_dash.py --base "$BASE"
run python3 scripts/check_doc_style.py
run python3 scripts/check_doc_style.py --selftest
run python3 scripts/check_gptp_docs.py
run python3 scripts/check_gptp_docs.py --selftest
run python3 docs/DOC_MAP.gen.py --check
run python3 docs/DOC_MAP.gen.py --selftest
run python3 docs/diagrams/timesync_chain.gen.py --check
run python3 docs/diagrams/timesync_chain.gen.py --selftest
run python3 scripts/check_solution_docs.py
run python3 scripts/check_solution_docs.py --selftest
run python3 docs/diagrams/submodule_boundaries.gen.py --check
run python3 docs/diagrams/submodule_boundaries.gen.py --selftest
run python3 scripts/check_submodule_docs.py
run python3 scripts/check_submodule_docs.py --selftest
run python3 scripts/check_diagram_pngs.py
run python3 scripts/check_diagram_pngs.py --selftest
run python3 scripts/check_feature_status.py --self-test
run python3 docs/traceability/gen_module_matrix.py --check
run python3 scripts/check_baremetal_only.py --check
run python3 scripts/check_baremetal_only.py --selftest
run python3 scripts/check_nvm_record_space.py
run python3 scripts/check_nvm_capture.py
run python3 scripts/check_rtl_source_lists.py
run python3 scripts/measure_naming.py --check
run python3 scripts/check_port_contracts.py
run python3 scripts/measure_fail_fast.py --check
run python3 scripts/check_todo_ownership.py
run python3 scripts/measure_test_evidence.py --check
run python3 scripts/check_hygiene.py --check
run python3 scripts/check_sv_idiom.py
run python3 scripts/check_cpp_idiom.py
run python3 scripts/check_py_idiom.py
run python3 scripts/check_sh_idiom.py
run python3 scripts/ci_events.py --check
run python3 scripts/check_doc_paths.py
run python3 scripts/check_archive.py
run python3 scripts/gen_toc.py --verify-anchors
run python3 scripts/gen_toc.py --check
run python3 scripts/ci_scope.py --selftest
run python3 scripts/pp_srcs.py --check
rm -f "$OUT" "$OUT.err.tmp"
