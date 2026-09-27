#!/usr/bin/env bash
# Verify a review clone is byte-exact at the expected head.
# Usage: verify_clone.sh <checkout> <expected-head> <expected-tree>
set -u
repo=${1:?checkout}; want_head=${2:?head}; want_tree=${3:?tree}
cd "$repo" || exit 2
fail=0
head=$(git rev-parse HEAD); tree=$(git rev-parse 'HEAD^{tree}')
echo "HEAD $head"; echo "TREE $tree"
[ "$head" = "$want_head" ] || { echo "FAIL head"; fail=1; }
[ "$tree" = "$want_tree" ] || { echo "FAIL tree"; fail=1; }
# index equals HEAD tree
itree=$(git write-tree)
echo "INDEX-TREE $itree"
[ "$itree" = "$want_tree" ] || { echo "FAIL index tree"; fail=1; }
# every tracked blob rehashes to its index entry, and the mode matches
mism=0; n=0
while IFS=$'\t' read -r meta path; do
  mode=${meta%% *}; rest=${meta#* }; oid=${rest%% *}
  n=$((n+1))
  if [ "$mode" = "160000" ]; then
    got=$(git -C "$path" rev-parse HEAD 2>/dev/null || echo uninit)
    echo "GITLINK $path $oid checkout=$got"
    continue
  fi
  if [ "$mode" = "120000" ]; then
    got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)
  else
    got=$(git hash-object --no-filters -- "$path")
    if [ "$mode" = "100755" ] && [ ! -x "$path" ]; then echo "MODE $path"; mism=$((mism+1)); fi
    if [ "$mode" = "100644" ] && [ -x "$path" ]; then echo "MODE $path"; mism=$((mism+1)); fi
  fi
  [ "$got" = "$oid" ] || { echo "BLOB $path"; mism=$((mism+1)); }
done < <(git ls-files -s)
echo "ENTRIES $n MISMATCHES $mism"
[ "$mism" -eq 0 ] || fail=1
flags=$(git ls-files -v | grep -v '^H ' | wc -l)
echo "NON-H-INDEX-FLAGS $flags"
[ "$flags" -eq 0 ] || fail=1
gl=$(git ls-tree -r HEAD | awk '$2=="commit"' | wc -l)
echo "GITLINKS-IN-TREE $gl"
st=$(git status --porcelain --ignored | wc -l)
echo "STATUS-LINES(incl ignored) $st"
[ "$st" -eq 0 ] || { git status --porcelain --ignored; fail=1; }
echo "RESULT $([ $fail -eq 0 ] && echo EXACT || echo DIRTY)"
exit $fail
