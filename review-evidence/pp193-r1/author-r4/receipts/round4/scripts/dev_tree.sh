#!/usr/bin/env bash
# usage: dev_tree.sh <name> [patch ...]: export the lane's HEAD plus its
# uncommitted diff into r4/dev/<name>, then apply each patch there
set -eu
S=<scratch>/r4; L=<lane>
t=$S/dev/$1; shift
rm -rf "$t"; mkdir -p "$t"
git -C $L archive HEAD | tar -x -C "$t"
git -C $L diff HEAD > "$t.diff"
[ -s "$t.diff" ] && git -C "$t" apply "$t.diff" 2>/dev/null || ( cd "$t" && patch -p1 -s < "$t.diff" )
git -C $L ls-files --others --exclude-standard -z | (cd $L && xargs -0 -r cp --parents -t "$t")
for p in "$@"; do ( cd "$t" && patch -p1 -s < "$p" ); done
echo "tree $t ready"
