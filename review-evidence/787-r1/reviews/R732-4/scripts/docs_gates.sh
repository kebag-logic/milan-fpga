#!/usr/bin/env bash
# Run the docs-workflow gates that cover PR #822's round-6 delta, at the checked-out head.
# usage: docs_gates.sh <repo> <base-commit> <logdir>
set -u
repo=$1 base=$2 out=$3
mkdir -p "$out"; cd "$repo" || exit 2
run() { local id=$1; shift; local t0=$SECONDS; ( set -e; eval "$*" ) >"$out/$id.log" 2>&1; local rc=$?
        printf 'rc=%s %4ss %s\n' "$rc" "$((SECONDS-t0))" "$id" | tee -a "$out/summary.txt"; }
: >"$out/summary.txt"
echo "head $(git rev-parse HEAD) base $base python $(python3 --version 2>&1)" | tee -a "$out/summary.txt"
run gate_7  'python3 scripts/docs_check.py'
run gate_8  "python3 scripts/check_em_dash.py --base $base"
run gate_9  'python3 scripts/check_doc_style.py; python3 scripts/check_doc_style.py --selftest; python3 scripts/check_gptp_docs.py; python3 scripts/check_gptp_docs.py --selftest'
run gate_10 'python3 docs/DOC_MAP.gen.py --check; python3 docs/DOC_MAP.gen.py --selftest; python3 docs/diagrams/timesync_chain.gen.py --check; python3 docs/diagrams/timesync_chain.gen.py --selftest'
run gate_12 'python3 docs/diagrams/submodule_boundaries.gen.py --check; python3 docs/diagrams/submodule_boundaries.gen.py --selftest; python3 scripts/check_submodule_docs.py; python3 scripts/check_submodule_docs.py --selftest'
run gate_14 'python3 scripts/check_diagram_pngs.py; python3 scripts/check_diagram_pngs.py --selftest'
run gate_36 'python3 scripts/check_hygiene.py --check; python3 scripts/check_hygiene.py --selftest'
run gate_39 'python3 scripts/check_py_idiom.py; python3 scripts/check_py_idiom.py --selftest'
run gate_43 'python3 scripts/check_doc_paths.py'
run gate_45 'python3 scripts/gen_toc.py --selftest; python3 scripts/gen_toc.py --verify-anchors; python3 scripts/gen_toc.py --check'
run diff_check "git diff --check $base HEAD"
