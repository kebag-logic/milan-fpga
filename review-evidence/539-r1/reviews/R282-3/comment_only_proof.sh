#!/bin/sh
# Usage: comment_only_proof.sh <repo> <old> <new> <path>
set -eu
R=$1; O=$2; N=$3; F=$4; D=$(dirname "$0")
git -C "$R" show "$O:$F" | python3 "$D/strip_comments.py" > /tmp/co_old.$$
git -C "$R" show "$N:$F" | python3 "$D/strip_comments.py" > /tmp/co_new.$$
echo "old blob $(git -C "$R" rev-parse "$O:$F") new blob $(git -C "$R" rev-parse "$N:$F")"
echo "comment-stripped sha256 old $(sha256sum < /tmp/co_old.$$ | cut -c1-64)"
echo "comment-stripped sha256 new $(sha256sum < /tmp/co_new.$$ | cut -c1-64)"
if cmp -s /tmp/co_old.$$ /tmp/co_new.$$; then echo "RESULT: comment-free text IDENTICAL"; rc=0; else echo "RESULT: DIFFERS"; diff /tmp/co_old.$$ /tmp/co_new.$$ || true; rc=1; fi
echo "raw diff numstat:"; git -C "$R" diff --numstat "$O" "$N" -- "$F"
rm -f /tmp/co_old.$$ /tmp/co_new.$$; exit $rc
