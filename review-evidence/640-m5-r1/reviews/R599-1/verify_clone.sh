#!/bin/sh
# Verify a review clone holds exactly the reviewed head: commit, tree, index
# records (mode, blob, stage 0), on-disk blob bytes and modes, no hidden index
# flags, and the required submodule gitlinks at their pinned commits.
# usage: verify_clone.sh <clone> <expected-head> <expected-tree>
set -eu
clone=$1; head=$2; tree=$3
cd "$clone"
fail=0
[ "$(git rev-parse HEAD)" = "$head" ] || { echo "FAIL head $(git rev-parse HEAD)"; fail=1; }
[ "$(git rev-parse 'HEAD^{tree}')" = "$tree" ] || { echo "FAIL tree"; fail=1; }
# index records equal the head tree (mode, blob, path), every record stage 0
git ls-tree -r --full-tree HEAD | awk '{print $1, $3, $4}' | sort > /tmp/r599_tree.$$
git ls-files -s | awk '{ if ($3 != 0) bad=1; print $1, $2, $4 } END { exit bad }' | sort > /tmp/r599_index.$$ \
  || { echo "FAIL nonzero index stage"; fail=1; }
cmp -s /tmp/r599_tree.$$ /tmp/r599_index.$$ || { echo "FAIL index differs from head tree"; fail=1; }
# no assume-unchanged / skip-worktree flags hiding a change
if git ls-files -v | grep -q '^[a-zS]'; then echo "FAIL hidden index flags"; fail=1; fi
# on-disk bytes and modes of every tracked regular file and symlink
git ls-files -s | awk '$1 != "160000" {print $1, $2, $4}' | while read -r mode blob path; do
  if [ "$mode" = "120000" ]; then
    [ -L "$path" ] && [ "$(printf %s "$(readlink "$path")" | git hash-object --stdin)" = "$blob" ] \
      || { echo "FAIL symlink $path"; exit 1; }
  else
    [ -f "$path" ] && [ ! -L "$path" ] || { echo "FAIL not a file $path"; exit 1; }
    [ "$(git hash-object --no-filters "$path")" = "$blob" ] || { echo "FAIL bytes $path"; exit 1; }
    if [ "$mode" = "100755" ]; then [ -x "$path" ] || { echo "FAIL mode $path"; exit 1; }
    else [ ! -x "$path" ] || { echo "FAIL mode $path"; exit 1; }; fi
  fi
done || fail=1
# untracked or ignored leftovers
[ -z "$(git status --porcelain --ignored --untracked-files=all)" ] || { echo "FAIL leftovers"; git status --porcelain --ignored | head; fail=1; }
# submodule gitlinks: checked-out ones must sit at their pin with clean trees
git ls-files -s | awk '$1 == "160000" {print $2, $4}' | while read -r pin path; do
  if [ -e "$path/.git" ]; then
    [ "$(git -C "$path" rev-parse HEAD)" = "$pin" ] || { echo "FAIL submodule $path"; exit 1; }
    [ -z "$(git -C "$path" status --porcelain --ignored)" ] || { echo "FAIL submodule dirty $path"; exit 1; }
    echo "submodule $path at pin $pin, clean"
  else
    echo "submodule $path not initialised (pin $pin)"
  fi
done || fail=1
rm -f /tmp/r599_tree.$$ /tmp/r599_index.$$
[ "$fail" = 0 ] && echo "CLONE VERIFIED: head $head tree $tree" || { echo "CLONE NOT VERIFIED"; exit 1; }
