#!/usr/bin/env bash
# Runs the Markdown-reading docs-workflow gates at the checked-out head.
# Usage: run_docs_gates.sh <repo> <venv-bin> <outdir> <base>
set -u
R=$1; V=$2; O=$3; B=$4
export PATH="$V:$PATH"
cd "$R" || exit 2
git rev-parse HEAD > "$O/HEAD.txt"
run() { n=$1; shift; "$@" > "$O/$n.log" 2>&1; echo $? > "$O/$n.rc"; }
run baremetal_check python3 scripts/check_baremetal_only.py --check
run baremetal_selftest python3 scripts/check_baremetal_only.py --selftest
run docs_check python3 scripts/docs_check.py
run em_dash python3 scripts/check_em_dash.py --base "$B"
run em_dash_selftest python3 scripts/check_em_dash.py --selftest
run doc_style python3 scripts/check_doc_style.py
run doc_style_selftest python3 scripts/check_doc_style.py --selftest
run gptp_docs python3 scripts/check_gptp_docs.py
run gptp_docs_selftest python3 scripts/check_gptp_docs.py --selftest
run doc_map python3 docs/DOC_MAP.gen.py --check
run doc_map_selftest python3 docs/DOC_MAP.gen.py --selftest
run solution_docs python3 scripts/check_solution_docs.py
run submodule_docs python3 scripts/check_submodule_docs.py
run feature_status python3 scripts/check_feature_status.py
run feature_status_selftest python3 scripts/check_feature_status.py --self-test
run module_matrix python3 docs/traceability/gen_module_matrix.py --check
run doc_paths python3 scripts/check_doc_paths.py
run archive python3 scripts/check_archive.py
run archive_selftest python3 scripts/check_archive.py --selftest
run toc_selftest python3 scripts/gen_toc.py --selftest
run toc_anchors python3 scripts/gen_toc.py --verify-anchors
run toc_check python3 scripts/gen_toc.py --check
echo done > "$O/ALL_DONE"
