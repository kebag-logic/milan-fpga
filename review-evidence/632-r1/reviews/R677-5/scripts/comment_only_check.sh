#!/bin/sh
# Prove that the delta's edited test sources differ only in comments.
# usage: comment_only_check.sh <repo> <base> <head> <scratchdir>
set -eu
R=$1; B=$2; H=$3; S=$4
cd "$R"
echo "base $(git rev-parse $B) head $(git rev-parse $H)"
echo "-- hdl syn configs stat (must be empty):"; git diff --stat $B..$H -- hdl syn configs; echo "-- end"
echo "-- every changed +/- line in tb sources is a comment line:"
git diff -U0 $B..$H -- 'tb/*.cpp' 'tb/*.py' | grep -E '^[+-][^+-]' | grep -v -E '^[+-][[:space:]]*(//|#)' && echo "NON-COMMENT LINES ABOVE" || echo "none (all comment lines)"
for f in $(git diff --name-only $B..$H -- 'tb/*.cpp' 'tb/*.py'); do
  mkdir -p "$S/old/$(dirname $f)" "$S/new/$(dirname $f)"
  git show $B:$f > "$S/old/$f"; git show $H:$f > "$S/new/$f"
  case $f in
    *.py) python3 -I -c 'import ast,sys; a=[ast.dump(ast.parse(open(p).read()),include_attributes=False) for p in sys.argv[1:]]; print(sys.argv[2], "AST identical" if a[0]==a[1] else "AST DIFFERS")' "$S/old/$f" "$S/new/$f";;
    *.cpp) for v in old new; do g++ -fpreprocessed -dD -E -P -x c++ "$S/$v/$f" 2>/dev/null | tr -s ' \t\n' '\n' > "$S/$v/$f.tok"; done
           if cmp -s "$S/old/$f.tok" "$S/new/$f.tok"; then echo "$f comment-stripped tokens identical ($(wc -l < $S/new/$f.tok) tokens)"; else echo "$f TOKENS DIFFER"; fi;;
  esac
done
