#!/bin/sh
# Run the parent's Python and C++ idiom gates with gptp-processor at a given
# commit, as the parent's consumer gate runs them (gitlink moved to match).
# usage: parent_idiom.sh <parent-clone> <gptp-commit> <out-prefix>
set -u
parent=$1; commit=$2; out=$3
cd "$parent/gptp-processor" || exit 9
git fetch -q origin "$commit" 2>/dev/null || true
git checkout -q --detach "$commit" || exit 9
cd "$parent" || exit 9
git update-index --cacheinfo "160000,$(git -C gptp-processor rev-parse HEAD),gptp-processor"
git submodule status -- protocol-processor gptp-processor > "$out.submodules"
python3 scripts/check_py_idiom.py > "$out.py.log" 2>&1; echo "rc=$?" > "$out.py.rc"
python3 scripts/check_cpp_idiom.py > "$out.cpp.log" 2>&1; echo "rc=$?" > "$out.cpp.rc"
python3 scripts/check_py_idiom.py --list > "$out.py-list.log" 2>&1
git diff --stat -- scripts/py_idiom.budget scripts/cpp_idiom.budget > "$out.budget-diff"
