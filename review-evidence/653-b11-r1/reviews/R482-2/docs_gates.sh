#!/bin/sh
# R482-2 docs gates at the reviewed head. Usage: docs_gates.sh <repo clone> [python]
# Prints each command, its rc and its output tail; no file in the clone is written.
repo=$1; py=${2:-python3}
cd "$repo" || exit 2
echo "HEAD $(git rev-parse HEAD) python $($py -c 'import sys;print(sys.version.split()[0])')"
run() { echo "== $*"; out=$("$@" 2>&1); rc=$?; printf '%s\n' "$out" | tail -n 4; echo "rc=$rc"; }
run $py scripts/docs_check.py
run $py scripts/check_doc_style.py
run $py scripts/gen_toc.py --check
run $py scripts/gen_toc.py --verify-anchors
run $py scripts/check_em_dash.py --base 6c22d3cad7c8c24ed3f0c5eab535922a3428c8d5
run $py scripts/check_doc_paths.py
run $py scripts/ci_scope.py --selftest
run $py scripts/check_baremetal_only.py --check
run $py scripts/check_feature_status.py --self-test
run git diff --check 6c22d3cad7c8c24ed3f0c5eab535922a3428c8d5 HEAD
run git diff --check 6f76d612a3191b77ac8a1fe2b9c66da42aeb405a HEAD
echo "== status after gates"; git status --porcelain --untracked-files=all; echo "(end status)"
