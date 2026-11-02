#!/usr/bin/env bash
# Pre-commit checks on a tree: idiom, doc style, docs check, bare-metal scope, diff check.
# usage: quick.sh <tree> <log dir>
set -u
tree=$1; out=$2; mkdir -p "$out"
cd "$tree" || exit 2
rc=0
for gate in "check_py_idiom.py" "check_doc_style.py" "docs_check.py" "check_baremetal_only.py --check"; do
  name=${gate%% *}; name=${name%.py}
  PYTHONDONTWRITEBYTECODE=1 python3 scripts/$gate > "$out/$name.log" 2>&1
  r=$?; echo $r > "$out/$name.rc"; echo "$name rc $r"; [ $r -eq 0 ] || rc=1
done
git diff --check 1f29f189 > "$out/diffcheck.log" 2>&1; r=$?; echo $r > "$out/diffcheck.rc"; echo "diffcheck rc $r"; [ $r -eq 0 ] || rc=1
exit $rc
