#!/bin/bash
# Runs the docs-workflow gates that need no submodule at the reviewed clone, concurrently, one log and rc per gate.
# Usage: run_gates_r4.sh <clone> <venv> <receipt dir>
C=$1; V=$2; R=$3; mkdir -p "$R"; cd "$C" || exit 2
export PATH="$V/bin:$PATH" PYTHONDONTWRITEBYTECODE=1
run() { n=$1; shift; ( "$@" > "$R/$n.log" 2>&1; echo $? > "$R/$n.rc" ) & }
run docs_check python3 scripts/docs_check.py
run em_dash python3 scripts/check_em_dash.py --base 1f29f189279f9fc0132f4918e47342b87d22f33a
run em_dash_self python3 scripts/check_em_dash.py --selftest
run doc_style python3 scripts/check_doc_style.py
run doc_style_self python3 scripts/check_doc_style.py --selftest
run gptp_docs python3 scripts/check_gptp_docs.py
run gptp_docs_self python3 scripts/check_gptp_docs.py --selftest
run doc_map python3 docs/DOC_MAP.gen.py --check
run doc_map_self python3 docs/DOC_MAP.gen.py --selftest
run timesync python3 docs/diagrams/timesync_chain.gen.py --check
run solution python3 scripts/check_solution_docs.py
run submodule_docs python3 scripts/check_submodule_docs.py
run feature python3 scripts/check_feature_status.py --self-test
run traceability python3 docs/traceability/gen_module_matrix.py --check
run doc_paths python3 scripts/check_doc_paths.py
run archive python3 scripts/check_archive.py
run archive_self python3 scripts/check_archive.py --selftest
run toc_self python3 scripts/gen_toc.py --selftest
run toc_anchors python3 scripts/gen_toc.py --verify-anchors
run toc_check python3 scripts/gen_toc.py --check
run baremetal python3 scripts/check_baremetal_only.py --check
run baremetal_self python3 scripts/check_baremetal_only.py --selftest
run diff_check git diff --check 1f29f189279f9fc0132f4918e47342b87d22f33a HEAD
wait
for f in "$R"/*.rc; do printf '%s\t%s\t%s\n' "$(basename "$f" .rc)" "$(cat "$f")" "$(tail -1 "${f%.rc}.log" | cut -c1-150)"; done
