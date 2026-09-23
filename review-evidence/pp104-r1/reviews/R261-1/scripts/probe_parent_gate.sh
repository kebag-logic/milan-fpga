#!/bin/sh
# Run the parent's Rule 12 (and C++ idiom) gates with protocol-processor staged
# at a given commit, in a disposable parent clone.
# Usage: probe_parent_gate.sh <parent-clone> <pp-rev> [--full]
# The parent clone must hold protocol-processor and gptp-processor as nested
# checkouts; this script moves protocol-processor to <pp-rev>, stages that
# gitlink, prints the pin evidence, then runs check_py_idiom.py (and, with
# --full, its --list, --selftest and check_cpp_idiom.py). Exit codes are
# printed verbatim; the script itself exits 0 unless setup fails.
set -u
PARENT=$1; REV=$2; FULL=${3:-}
cd "$PARENT" || exit 2
git -C protocol-processor checkout -q --detach "$REV" || exit 2
git add protocol-processor || exit 2
echo "# parent HEAD $(git rev-parse HEAD)"
echo "# staged gitlinks:"; git ls-files -s protocol-processor gptp-processor | sed 's/^/#   /'
echo "# git submodule status:"; git submodule status -- protocol-processor gptp-processor | sed 's/^/#   /'
echo "# protocol-processor worktree clean: $(test -z "$(git -C protocol-processor status --porcelain)" && echo yes || echo NO)"
echo "\$ python3 scripts/check_py_idiom.py"
python3 scripts/check_py_idiom.py; echo "exit=$?"
if [ "$FULL" = --full ]; then
    echo "\$ python3 scripts/check_py_idiom.py --list | grep -E 'protocol-processor/tb/pp_top|unannotated|undocumented'"
    python3 scripts/check_py_idiom.py --list 2>&1 | grep -E 'protocol-processor/tb/pp_top|unannotated public|undocumented public'; echo "(grep exit=$?)"
    echo "\$ python3 scripts/check_py_idiom.py --selftest | tail -3"
    out=$(python3 scripts/check_py_idiom.py --selftest 2>&1); rc=$?; printf '%s\n' "$out" | tail -3; echo "exit=$rc"
    echo "\$ python3 scripts/check_cpp_idiom.py"
    python3 scripts/check_cpp_idiom.py; echo "exit=$?"
fi
