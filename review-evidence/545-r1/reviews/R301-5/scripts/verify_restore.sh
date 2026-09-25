#!/usr/bin/env bash
# Prove a review clone is at its exact head: HEAD and tree, the index tree,
# every tracked entry's mode and blob id against HEAD (worktree bytes hashed
# directly, so assume-unchanged / skip-worktree cannot hide an edit), the
# submodule gitlinks against each checkout, and no untracked or ignored
# entries anywhere.
#
# usage: verify_restore.sh <repo> <expected-head> <expected-tree>
set -uo pipefail
cd "$1" || exit 2
want_head=$2 want_tree=$3
fail=0
note() { echo "$*"; }
bad() { echo "FAIL: $*"; fail=1; }

head=$(git rev-parse HEAD); tree=$(git rev-parse HEAD^{tree}); itree=$(git write-tree)
note "HEAD $head"; note "tree $tree"; note "index tree $itree"
[ "$head" = "$want_head" ] || bad "HEAD is not $want_head"
[ "$tree" = "$want_tree" ] || bad "tree is not $want_tree"
[ "$itree" = "$tree" ] || bad "index tree differs from HEAD tree"

flags=$(git ls-files -v | grep -cv '^H ' || true)
note "index entries flagged other than H (assume-unchanged/skip-worktree/etc.): $flags"
[ "$flags" -eq 0 ] || bad "index carries flagged entries"

mism=0; n=0
while IFS=$'\t' read -r meta path; do
  mode=${meta%% *}; rest=${meta#* }; type=${rest%% *}; oid=${rest#* }
  n=$((n + 1))
  case "$mode" in
    160000)
      if [ ! -e "$path/.git" ]; then
        # Uninitialised: acceptable only as an empty directory, which is how
        # the clone was delivered for submodules no gate here reads.
        if [ -z "$(ls -A "$path" 2>/dev/null)" ]; then
          note "gitlink $path $oid uninitialised and empty (as delivered)"
        else
          bad "gitlink $path uninitialised but not empty"; mism=$((mism+1))
        fi
        continue
      fi
      got=$(git -C "$path" rev-parse HEAD 2>/dev/null)
      [ "$got" = "$oid" ] || { bad "gitlink $path at ${got:-none}, pinned $oid"; mism=$((mism+1)); }
      d=$(git -C "$path" status --porcelain --ignored | wc -l)
      [ "$d" -eq 0 ] || { bad "submodule $path has $d dirty/untracked/ignored entries"; mism=$((mism+1)); }
      note "gitlink $path $oid ok" ;;
    120000)
      got=$(readlink "$path" | tr -d '\n' | git hash-object --stdin)
      [ -L "$path" ] && [ "$got" = "$oid" ] || { bad "symlink $path"; mism=$((mism+1)); } ;;
    100644|100755)
      got=$(git hash-object --no-filters -- "$path" 2>/dev/null)
      if [ -x "$path" ]; then fm=100755; else fm=100644; fi
      [ "$got" = "$oid" ] && [ "$fm" = "$mode" ] && [ ! -L "$path" ] || { bad "file $path (mode $fm vs $mode, blob $got vs $oid)"; mism=$((mism+1)); } ;;
    *) bad "unexpected mode $mode at $path"; mism=$((mism+1)) ;;
  esac
done < <(git ls-tree -r --full-tree HEAD)
note "tracked entries checked: $n, mismatches: $mism"

extra=$(git status --porcelain --ignored | wc -l)
note "untracked/ignored/modified entries (superproject): $extra"
[ "$extra" -eq 0 ] || { git status --porcelain --ignored; bad "superproject not pristine"; }
echo "restore verdict: $([ "$fail" -eq 0 ] && echo EXACT || echo NOT-EXACT)"
exit $fail
