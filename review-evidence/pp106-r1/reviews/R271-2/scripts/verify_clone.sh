#!/usr/bin/env bash
# Verify that a review clone still sits at the exact reviewed head with every
# tracked blob byte- and mode-identical to the commit, the index equal to the
# head tree, no untracked or ignored leftovers, and every gitlink recorded.
# usage: verify_clone.sh <clone> <expected-head> <expected-tree>
set -euo pipefail
clone=${1:?clone}; want_head=${2:?head}; want_tree=${3:?tree}
cd "$clone"
fail=0
head=$(git rev-parse HEAD); tree=$(git rev-parse 'HEAD^{tree}'); itree=$(git write-tree)
echo "HEAD       $head"; echo "HEAD tree  $tree"; echo "index tree $itree"
[ "$head" = "$want_head" ] || { echo "MISMATCH head"; fail=1; }
[ "$tree" = "$want_tree" ] || { echo "MISMATCH tree"; fail=1; }
[ "$itree" = "$want_tree" ] || { echo "MISMATCH index tree"; fail=1; }
n=0; bad=0
while IFS=$'\t' read -r meta path; do
  mode=${meta%% *}; rest=${meta#* }; type=${rest%% *}; oid=${rest#* }
  n=$((n + 1))
  if [ "$type" = commit ]; then
    echo "gitlink $path $oid"; continue
  fi
  got=$(git hash-object --no-filters -- "$path")
  if [ "$mode" = 120000 ]; then
    [ -L "$path" ] || { echo "MODE $path not a symlink"; bad=$((bad + 1)); continue; }
    got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)
  elif [ -x "$path" ]; then fmode=100755; else fmode=100644; fi
  if [ "$mode" != 120000 ] && [ "$fmode" != "$mode" ]; then echo "MODE $path $fmode != $mode"; bad=$((bad + 1)); fi
  [ "$got" = "$oid" ] || { echo "BYTES $path $got != $oid"; bad=$((bad + 1)); }
done < <(git ls-tree -r --full-tree HEAD)
echo "tracked entries checked: $n, byte/mode mismatches: $bad"
[ "$bad" -eq 0 ] || fail=1
if [ -f .gitmodules ]; then echo ".gitmodules present:"; cat .gitmodules; else echo "no .gitmodules: no submodule gitlink is required in this repository"; fi
extra=$(git status --porcelain --ignored --untracked-files=all)
if [ -n "$extra" ]; then echo "status not clean:"; echo "$extra"; fail=1; else echo "status: clean (no modified, untracked or ignored files)"; fi
echo "verdict: $([ $fail -eq 0 ] && echo INTACT || echo NOT-INTACT)"
exit $fail
