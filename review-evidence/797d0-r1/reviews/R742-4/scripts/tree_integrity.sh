#!/bin/sh
# Usage: tree_integrity.sh <clone> <head> <tree>. Reads only; rc 0 when the clone holds the head's exact bytes and modes.
c=$1; h=$2; t=$3; rc=0
[ "$(git -C "$c" rev-parse HEAD)" = "$h" ] && echo "head ok $h" || { echo "HEAD differs"; rc=1; }
[ "$(git -C "$c" rev-parse 'HEAD^{tree}')" = "$t" ] && echo "tree ok $t" || { echo "tree differs"; rc=1; }
[ -z "$(git -C "$c" status --porcelain)" ] && echo "status clean" || { echo "status dirty"; rc=1; }
git -C "$c" diff-index --quiet HEAD -- && echo "index and bytes match HEAD, modes included" || { echo "index differs"; rc=1; }
git -C "$c" ls-files -s | awk '$1!="160000"{print $2"\t"$4}' > /tmp/ti.$$
n=0; bad=0
while IFS="$(printf '\t')" read -r sha path; do
  n=$((n+1)); [ "$(git -C "$c" hash-object --no-filters -- "$path")" = "$sha" ] || { bad=$((bad+1)); echo "BYTES $path"; }
done < /tmp/ti.$$
rm -f /tmp/ti.$$; echo "tracked blobs $n, byte mismatches $bad"; [ "$bad" = 0 ] || rc=1
git -C "$c" ls-files -s | awk '$1=="160000"{print $2" "$4}' | while read -r sha path; do
  if [ -e "$c/$path/.git" ]; then
    now=$(git -C "$c/$path" rev-parse HEAD); dirty=$(git -C "$c/$path" status --porcelain | wc -l)
    echo "gitlink $path pinned $sha at $now dirty=$dirty"; [ "$now" = "$sha" ] && [ "$dirty" = 0 ] || echo "GITLINK-BAD $path"
  else echo "gitlink $path pinned $sha not initialised"; fi
done
exit $rc
