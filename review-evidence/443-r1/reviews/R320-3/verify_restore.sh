#!/usr/bin/env bash
# Usage: verify_restore.sh <clone> <expected-head> <expected-tree>
# Verifies HEAD/tree, index == HEAD, every tracked regular/symlink blob's bytes
# and mode in the worktree, the required submodule gitlinks, and a clean status.
set -u; c=$1; eh=$2; et=$3; bad=0
cd "$c"
h=$(git rev-parse HEAD); t=$(git rev-parse HEAD^{tree})
echo "HEAD $h"; echo "TREE $t"
[ "$h" = "$eh" ] || { echo "FAIL head"; bad=1; }
[ "$t" = "$et" ] || { echo "FAIL tree"; bad=1; }
git update-index -q --really-refresh >/dev/null
git diff --cached --quiet HEAD && echo "PASS index == HEAD" || { echo "FAIL index"; bad=1; }
[ "$(git write-tree)" = "$et" ] && echo "PASS index tree == $et" || { echo "FAIL write-tree"; bad=1; }
n=0; m=0
while IFS=$'\t' read -r meta path; do
  mode=${meta%% *}; sha=${meta##* }
  case $mode in
    160000) continue;;
    120000) got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin);;
    *) got=$(git hash-object --no-filters -- "$path")
       x=100644; [ -x "$path" ] && x=100755
       [ "$x" = "$mode" ] || { echo "MODE MISMATCH $path $x != $mode"; m=$((m+1)); };;
  esac
  [ "$got" = "$sha" ] || { echo "BYTES MISMATCH $path"; m=$((m+1)); }
  n=$((n+1))
done < <(git ls-tree -r --full-tree HEAD)
echo "checked $n tracked blobs, $m mismatches"; [ $m -eq 0 ] || bad=1
for s in external gptp-processor protocol-processor third_party/verilog-axis; do
  want=$(git ls-tree HEAD "$s" | awk '{print $3}')
  if [ -e "$s/.git" ]; then have=$(git -C "$s" rev-parse HEAD); else have=uninitialized; fi
  echo "gitlink $s recorded=$want checkout=$have"
  if [ "$have" != "uninitialized" ] && [ "$have" != "$want" ]; then echo "FAIL gitlink $s"; bad=1; fi
done
st=$(git status --porcelain --ignored | wc -l); echo "status entries (incl. ignored): $st"
[ "$st" -eq 0 ] || bad=1
echo "RESULT $([ $bad -eq 0 ] && echo PASS || echo FAIL)"; exit $bad
