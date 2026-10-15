#!/bin/sh
# Verify a review clone is at the exact head with committed bytes, modes, index
# and submodule gitlinks.  Usage: verify_clone.sh <repo> <head> <tree>
set -u
repo=$1; head=$2; tree=$3
cd "$repo" || exit 2
fail=0
[ "$(git rev-parse HEAD)" = "$head" ] || { echo "HEAD differs"; fail=1; }
[ "$(git rev-parse 'HEAD^{tree}')" = "$tree" ] || { echo "tree differs"; fail=1; }
[ "$(git write-tree)" = "$tree" ] || { echo "index tree differs"; fail=1; }
git diff --quiet HEAD -- || { echo "worktree differs from HEAD"; fail=1; }
git diff --cached --quiet HEAD -- || { echo "index differs from HEAD"; fail=1; }
untracked=$(git status --porcelain --untracked-files=all | wc -l)
[ "$untracked" -eq 0 ] || { echo "status not clean: $untracked entries"; git status --porcelain | head; fail=1; }
# Index entries (mode, oid, path) equal the committed tree, including gitlinks.
a=$(git ls-files -s | awk '{print $1, $2, $4}' | sha256sum)
b=$(git ls-tree -r --full-tree HEAD | awk '{print $1, $3, $4}' | sha256sum)
[ "$a" = "$b" ] || { echo "index entries differ from tree"; fail=1; }
# Gitlinks and checked-out submodule heads.
git ls-tree -r HEAD | awk '$2 == "commit" {print $3, $4}' | while read -r oid path; do
    if [ -e "$path/.git" ]; then
        sub=$(git -C "$path" rev-parse HEAD)
        state="checked out at $sub"
        [ "$sub" = "$oid" ] || state="$state MISMATCH"
        git -C "$path" diff --quiet HEAD -- || state="$state DIRTY"
    else
        state="not initialised"
    fi
    echo "gitlink $path $oid: $state"
done
# Hash every tracked regular file's bytes against its blob id.
bad=0
git ls-tree -r HEAD | awk '$2 == "blob" {print $1, $3, $4}' | while read -r mode oid path; do
    if [ "$mode" = 120000 ]; then
        got=$(readlink "$path" | tr -d '\n' | git hash-object --stdin)
    else
        got=$(git hash-object --no-filters "$path")
        x=0; [ -x "$path" ] && x=1
        if [ "$mode" = 100755 ] && [ $x -ne 1 ]; then echo "mode differs: $path"; fi
        if [ "$mode" = 100644 ] && [ $x -ne 0 ]; then echo "mode differs: $path"; fi
    fi
    [ "$got" = "$oid" ] || echo "bytes differ: $path"
done > /tmp/verify_clone_$$.txt
if [ -s /tmp/verify_clone_$$.txt ]; then cat /tmp/verify_clone_$$.txt; fail=1; fi
echo "blobs checked: $(git ls-tree -r HEAD | awk '$2 == "blob"' | wc -l)"
rm -f /tmp/verify_clone_$$.txt
[ $fail -eq 0 ] && echo "CLONE EXACT" || echo "CLONE NOT EXACT"
exit $fail
