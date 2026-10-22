#!/usr/bin/env bash
# sv_comment_only.sh BASE HEAD: every changed line in the delta's .sv files is a
# // comment line, and the files with // comments stripped are identical.
set -u
b=$1; h=$2; rc=0
for f in $(git diff --name-only "$b" "$h" -- '*.sv'); do
  n=$(git diff -U0 "$b" "$h" -- "$f" | grep -E '^[-+][^-+]' | grep -v -E '^[-+][[:space:]]*//' | wc -l)
  s=$(diff <(git show "$b:$f" | sed -E 's://.*$::' | sed -E 's/[[:space:]]+$//' | grep -v '^$') \
           <(git show "$h:$f" | sed -E 's://.*$::' | sed -E 's/[[:space:]]+$//' | grep -v '^$') | wc -l)
  echo "$f non-comment-changed-lines=$n stripped-diff-lines=$s"
  [ "$n" = 0 ] && [ "$s" = 0 ] || rc=1
done
exit $rc
