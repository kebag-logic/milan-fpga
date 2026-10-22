#!/bin/sh
# Added source lines in the reviewed delta that name review rounds, reviewer
# or author IDs, bench lane labels or issue-comment IDs.
# usage: comment_rule_scan.sh <repo> <base> <head>
cd "$1" && git diff -U0 "$2" "$3" -- hdl tb sw scripts syn |
  awk '/^\+\+\+ /{f=substr($0,7);next} /^@@/{split($3,a,",");l=substr(a[1],2);next}
       /^\+/{ if ($0 ~ /R67[0-9]|R678|A659|\[A[0-9]+\]|\[R[0-9]+|issuecomment|[^A-Za-z0-9][Bb]1[0-9][^0-9]|round [0-9]|Round [0-9]/) print f":"l": "substr($0,2); l++ }'
