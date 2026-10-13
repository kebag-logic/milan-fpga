#!/usr/bin/env bash
# Gates that need the git repository: run in the exact-head clone bound
# read-only inside the sandbox. Usage: run_git_gates.sh PACKET CLONE OUT ALTERNATES MDVENV
set -uo pipefail
P=$1; C=$2; O=$3; ALT=$4; MD=$5
SB="$P/scripts/sandbox.sh"
export SANDBOX_TREE_RO=1 SANDBOX_RO="$ALT:$MD"
run() { name=$1; shift; ( "$SB" "$C" "$@" >"$O/$name.log" 2>&1; echo $? >"$O/$name.rc" ) & }
run baremetal-check /usr/bin/python3 -B scripts/check_baremetal_only.py --check
run py-idiom /usr/bin/python3 -B scripts/check_py_idiom.py
run py-idiom-selftest /usr/bin/python3 -B scripts/check_py_idiom.py --selftest
run doc-paths $MD/bin/python -B scripts/check_doc_paths.py
run toc-check $MD/bin/python -B scripts/gen_toc.py --check
run toc-anchors $MD/bin/python -B scripts/gen_toc.py --verify-anchors
run em-dash $MD/bin/python -B scripts/check_em_dash.py --base dc4d06cb
run diff-check git diff --check dc4d06cb 73b8dcd667aa5bf1254e828dd1dd7217c8a103ce
run docs-check-git $MD/bin/python -B scripts/docs_check.py
run doc-style-git $MD/bin/python -B scripts/check_doc_style.py
wait
