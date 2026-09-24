#!/bin/sh
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Round R302-3 clone integrity check. Usage: clone_integrity.sh <clone>
# Prints PASS/FAIL per property; exit 0 only if every property holds.
set -u
C="$1"
HEAD_EXP=0c61d458941088f3847513b7c6fe6589c75b4270
TREE_EXP=88a5ce9545a23561beae21d3e0323a9d1fb0d051
export GIT_NO_REPLACE_OBJECTS=1
rc=0
chk() { if [ "$2" = "$3" ]; then echo "PASS $1: $2"; else echo "FAIL $1: got '$2' want '$3'"; rc=1; fi; }
chk head "$(git -C "$C" rev-parse HEAD)" "$HEAD_EXP"
chk tree "$(git -C "$C" rev-parse 'HEAD^{tree}')" "$TREE_EXP"
chk status-porcelain-lines "$(git -C "$C" status --porcelain=v1 --ignored=no | wc -l)" 0
chk index-vs-tree "$(git -C "$C" write-tree)" "$TREE_EXP"
chk skip-or-assume-flags "$(git -C "$C" ls-files -v | grep -c -v '^H ')" 0
chk unmerged-entries "$(git -C "$C" ls-files -u | wc -l)" 0
# gitlinks recorded in the head tree versus the index
chk gitlinks "$(git -C "$C" ls-files -s | awk '$1=="160000"{print $2, $4}' | sort | sha256sum | cut -c1-16)" \
             "$(git -C "$C" ls-tree -r HEAD | awk '$1=="160000"{print $3, $4}' | sort | sha256sum | cut -c1-16)"
git -C "$C" ls-tree -r HEAD | awk '$1=="160000"{print "  gitlink", $4, $3}'
git -C "$C" submodule status 2>&1 | sed 's/^/  submodule-status /'
# every tracked regular file / symlink: on-disk bytes re-hash to the tree blob, mode matches
bad=0; n=0
tmp=$(mktemp)
git -C "$C" ls-tree -r HEAD | awk '$1!="160000"' > "$tmp"
while IFS="$(printf '\t')" read -r meta path; do
  mode=$(echo "$meta" | cut -d' ' -f1); blob=$(echo "$meta" | cut -d' ' -f3)
  n=$((n + 1))
  f="$C/$path"
  if [ "$mode" = 120000 ]; then
    got=$(printf '%s' "$(readlink "$f")" | git hash-object --stdin)
  else
    got=$(git hash-object --no-filters "$f" 2>/dev/null)
    if [ "$mode" = 100755 ] && [ ! -x "$f" ]; then bad=$((bad + 1)); echo "  MODE $path"; fi
    if [ "$mode" = 100644 ] && [ -x "$f" ]; then bad=$((bad + 1)); echo "  MODE $path"; fi
  fi
  [ "$got" = "$blob" ] || { bad=$((bad + 1)); echo "  BLOB $path"; }
done < "$tmp"
rm -f "$tmp"
echo "rehash-files: $n checked, $bad mismatches"
[ "$bad" -eq 0 ] || rc=1
echo "overall: $([ $rc -eq 0 ] && echo PASS || echo FAIL)"
exit $rc
