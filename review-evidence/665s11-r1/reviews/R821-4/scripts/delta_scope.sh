#!/bin/sh
# usage: delta_scope.sh <clone> <scratch-dir>: the round-4 delta's file list, and proof that its C++ and
# Python edits change comments only (comment-stripped C++ and the Python AST equal at both commits).
set -eu
C=$1; S=$2; mkdir -p "$S"; cd "$C"
git diff --name-status 6171d654 049f0e4d
for c in 6171d654 049f0e4d; do
  git show $c:sw/firmware/ctrl/test/test_plat_boot.cpp | g++ -x c++ -fpreprocessed -dD -E -P - 2>/dev/null | tr -s ' \n' > "$S/tpb.$c.nc"
  git show $c:sw/firmware/ctrl/test/plat_mutants.py > "$S/pm.$c.py"
  python3 -I -c "import ast,sys;print(ast.dump(ast.parse(open(sys.argv[1]).read())))" "$S/pm.$c.py" > "$S/pm.$c.ast"
done
cmp "$S/tpb.6171d654.nc" "$S/tpb.049f0e4d.nc" && echo "test_plat_boot.cpp: comment-stripped text identical"
cmp "$S/pm.6171d654.ast" "$S/pm.049f0e4d.ast" && echo "plat_mutants.py: AST identical"
git diff --stat 6171d654 049f0e4d -- hdl tb protocol-processor gptp-processor sw/firmware/ctrl/aecp sw/firmware/ctrl/plat/*.c sw/firmware/ctrl/plat/*.h | tail -1
echo "non-comment source files in delta: $(git diff --name-only 6171d654 049f0e4d | grep -Ev '\.md$|test_plat_boot\.cpp$|plat_mutants\.py$' | wc -l)"
git diff --check 1d6bf555 049f0e4d && echo "git diff --check vs merge base: clean"
printf 'max added code-file line width: '; git diff -U0 6171d654 049f0e4d -- '*.py' '*.cpp' | grep '^+[^+]' | awk '{print length($0)-1}' | sort -n | tail -1
printf 'em dashes added: '; git diff 6171d654 049f0e4d | grep '^+' | grep -c "$(printf '\342\200\224')" || true
