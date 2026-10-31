#!/bin/sh
# Re-run the R748-3 checks from a clean clone at the reviewed head.
# Usage: verify.sh <clone> <python-with-tools/markdown/requirements.txt>
set -u
C=$1; P=$2; cd "$C" || exit 2
git rev-parse HEAD HEAD^{tree}
git merge-tree --write-tree 02ca829a 50e5d08d; git rev-parse 17fd6f73^{tree}
git diff 17fd6f73 81f78a81
git grep -n 'gate refuses'; git grep -n '0\.408' -- ':!review-evidence' ':!docs/history'
python3 -I scripts/check_doc_style.py; echo rc=$?
"$P" -I scripts/gen_toc.py --check; echo rc=$?
"$P" -I scripts/gen_toc.py --verify-anchors; echo rc=$?
python3 -I scripts/docs_check.py; echo rc=$?
python3 -I scripts/check_doc_paths.py; echo rc=$?
"$P" -I scripts/check_em_dash.py --base 17fd6f73; echo rc=$?
python3 syn/ooc/pp_resource_gate.py check-baseline; echo rc=$?
git status --porcelain --untracked-files=all
