#!/bin/sh
# Whole-tree sweep for current-state statements of the pre-#502 pending
# trigger. Usage: sweep.sh <repo> <rev>. Prints one block per pattern with
# every hit (git grep over tracked files at <rev>, gitlinks not recursed).
set -u
repo=$1
rev=$2
n=0
for pat in \
  'aecp_mark_pend' \
  'mark_pend' \
  'every commit beat' \
  'conservative duplicate' \
  '[Cc]onservative' \
  'late-mark|late mark|mark-tail|mark tail' \
  "program's tail|program tail|programs' tail" \
  'class-6/7|class 6 or( class)? 7|class-6 and class-7|class-6 or class-7|class-6 bit|class-7 bit|sticky class' \
  'commit marks?\b.*(pend|trigger|sticky)|(pend|trigger|sticky).*commit marks?\b' \
  'NVM_MARK.*(pend|trigger|sticky|durable)|(pend|trigger|sticky|durable).*NVM_MARK' \
  '#502|issue 502|issues/502' \
  'reads? durable over' \
  ; do
  echo "=== PATTERN: $pat"
  git -C "$repo" grep -n -I -E -e "$pat" "$rev" -- . \
    | sed "s/^$rev://"
  c=$(git -C "$repo" grep -n -I -E -e "$pat" "$rev" -- . | wc -l)
  echo "--- count: $c"
  n=$((n + c))
done
echo "=== TOTAL hit lines (patterns overlap): $n"
