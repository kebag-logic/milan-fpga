#!/bin/sh
# Verify a checkout against its HEAD: raw bytes and modes of every tracked
# blob, index entries, a clean status, and every submodule gitlink.
# Usage: tree_integrity.sh <checkout> <expected-head>
set -eu
cd "$1"
head=$(git rev-parse HEAD)
[ "$head" = "$2" ] || { echo "HEAD $head != $2"; exit 1; }
echo "head $head tree $(git rev-parse 'HEAD^{tree}')"
# index entries equal the commit's tree entries (mode, object, path)
git ls-tree -r HEAD | awk '{print $1, $3, $4}' | sort > /tmp/r663-tree.$$
git ls-files -s | awk '{print $1, $2, $4}' | sort > /tmp/r663-index.$$
if cmp -s /tmp/r663-tree.$$ /tmp/r663-index.$$; then echo "index == HEAD tree: yes"; else echo "index == HEAD tree: NO"; fi
rm -f /tmp/r663-tree.$$ /tmp/r663-index.$$
# raw working-tree bytes and modes of every tracked blob
git ls-tree -r HEAD | while read -r mode type oid path; do
  [ "$type" = blob ] || continue
  if [ "$mode" = 120000 ]; then
    got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)
  else
    got=$(git hash-object --no-filters "$path")
    if [ "$mode" = 100755 ]; then [ -x "$path" ] || echo "MODE $path"; else [ ! -x "$path" ] || echo "MODE $path"; fi
  fi
  [ "$got" = "$oid" ] || echo "BYTES $path"
done > /tmp/r663-blobs.$$
echo "tracked blobs: $(git ls-tree -r HEAD | grep -c ' blob ')"
echo "blob byte/mode mismatches: $(wc -l < /tmp/r663-blobs.$$)"; cat /tmp/r663-blobs.$$; rm -f /tmp/r663-blobs.$$
echo "status (untracked included, ignored excluded):"; git status --porcelain --untracked-files=all | head -20; echo "end status"
echo "gitlinks:"
git ls-tree -r HEAD | awk '$2 == "commit" {print $3, $4}' | while read -r oid path; do
  if [ -e "$path/.git" ]; then got=$(git -C "$path" rev-parse HEAD); else got=uninitialised; fi
  echo "$path recorded $oid checked-out $got"
done
