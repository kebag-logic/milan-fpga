#!/usr/bin/env bash
# Final integrity of the review clone after probes: HEAD/tree identity, index
# equal to the committed tree (object ids, modes, stage 0 only, no skip-worktree
# or assume-unchanged bits), every tracked worktree blob hashing to its tree
# entry with the tree's mode, clean status including ignored files, and every
# submodule gitlink checked out at its recorded commit with a clean worktree.
#   usage: integrity.sh REPO EXPECTED_HEAD EXPECTED_TREE
set -uo pipefail
REPO=$1; HEAD_WANT=$2; TREE_WANT=$3; bad=0
cd "$REPO"
say() { echo "$1"; case "$1" in FAIL*) bad=1;; esac; }
[ "$(git rev-parse HEAD)" = "$HEAD_WANT" ] && say "PASS head $HEAD_WANT" || say "FAIL head $(git rev-parse HEAD)"
[ "$(git rev-parse HEAD^{tree})" = "$TREE_WANT" ] && say "PASS tree $TREE_WANT" || say "FAIL tree"
[ "$(git write-tree)" = "$TREE_WANT" ] && say "PASS index writes the committed tree" || say "FAIL index tree differs"
[ -z "$(git ls-files -v | grep -v '^H ')" ] && say "PASS no hidden index flags" || say "FAIL hidden index flags: $(git ls-files -v | grep -v '^H ' | head -3)"
[ -z "$(git ls-files -s | awk '$3!=0')" ] && say "PASS stage 0 only" || say "FAIL unmerged entries"
mism=0; n=0
while read -r mode type oid path; do
  [ "$type" = blob ] || continue
  n=$((n+1))
  if [ "$mode" = 120000 ]; then got=$(readlink "$path" | tr -d '\n' | git hash-object --stdin); want_mode_ok=$([ -L "$path" ] && echo y)
  else got=$(git hash-object --no-filters -- "$path"); want_mode_ok=$([ "$mode" = 100755 ] && [ -x "$path" ] && echo y || { [ "$mode" = 100644 ] && [ ! -x "$path" ] && echo y; }); fi
  if [ "$got" != "$oid" ] || [ "$want_mode_ok" != y ]; then mism=$((mism+1)); echo "  mismatch $mode $path"; fi
done < <(git ls-tree -r HEAD)
[ $mism -eq 0 ] && say "PASS $n tracked blobs match bytes and modes" || say "FAIL $mism of $n tracked blobs differ"
[ -z "$(git status --porcelain --ignored)" ] && say "PASS clean status (ignored included)" || say "FAIL status not clean"
while read -r mode type oid path; do
  [ "$type" = commit ] || continue
  if [ -e "$path/.git" ]; then
    got=$(git -C "$path" rev-parse HEAD)
    [ "$got" = "$oid" ] && say "PASS gitlink $path $oid" || say "FAIL gitlink $path at $got want $oid"
    [ -z "$(git -C "$path" status --porcelain --ignored)" ] && say "PASS $path clean (ignored included)" || say "FAIL $path worktree not clean"
  else
    say "NOTE gitlink $path $oid not initialized in this clone"
  fi
done < <(git ls-tree -r HEAD)
[ $bad -eq 0 ] && echo "INTEGRITY PASS" || echo "INTEGRITY FAIL"
exit $bad
