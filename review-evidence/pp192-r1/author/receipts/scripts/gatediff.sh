#!/usr/bin/env bash
# usage: gatediff.sh <base-rec> <head-rec> <out-dir>   for every <gate>.log in both, write the
# unified diff of the two logs (scratch, lane and tree roots masked) to <out-dir>/<gate>.diff
# and print one line per gate: rc at each side and the number of differing lines
b="$1"; h="$2"; o="$3"; mkdir -p "$o"
mask() { sed -e 's#<scratch>/[a-z0-9]*#<tree>#g' -e 's#<lane>#<tree>#g' \
             -e 's#/tmp/[A-Za-z0-9._-]*#<tmp>#g' "$1"; }
for f in "$b"/*.log; do
  n=$(basename "$f" .log); [ -f "$h/$n.log" ] || { echo "$n: base only"; continue; }
  diff -u --label "base/$n.log" --label "head/$n.log" <(mask "$f") <(mask "$h/$n.log") > "$o/$n.diff"
  c=$(grep -c -E '^[-+][^-+]' "$o/$n.diff")
  echo "$n: base rc $(cat "$b/$n.rc" 2>/dev/null) ($(cat "$b/$n.secs" 2>/dev/null) s), head rc $(cat "$h/$n.rc" 2>/dev/null) ($(cat "$h/$n.secs" 2>/dev/null) s), $c differing lines"
done
