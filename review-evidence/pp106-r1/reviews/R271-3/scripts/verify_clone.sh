#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Verify a review clone is byte-exact at the reviewed head, without writing it.
# usage: verify_clone.sh CLONE HEAD_SHA TREE_SHA
# Checks: HEAD and HEAD^{tree}; the index's tree (git write-tree is avoided:
# it writes objects) via ls-files -s against ls-tree -r; every tracked path's
# on-disk bytes re-hashed (hash-object without -w) and its mode; gitlinks and
# .gitmodules; and an empty `status --porcelain --ignored`.
set -euo pipefail
clone=$1; want_head=$2; want_tree=$3
export GIT_NO_REPLACE_OBJECTS=1 GIT_OPTIONAL_LOCKS=0
g() { /usr/bin/git -C "$clone" "$@"; }
rc=0
head=$(g rev-parse HEAD); tree=$(g rev-parse 'HEAD^{tree}')
echo "HEAD $head"; echo "tree $tree"
[ "$head" = "$want_head" ] || { echo "HEAD MISMATCH"; rc=1; }
[ "$tree" = "$want_tree" ] || { echo "TREE MISMATCH"; rc=1; }
# index entries (mode, blob, path) must equal the commit tree's entries
idx=$(g ls-files -s | awk '{print $1, $2, $4}' | sort)
com=$(g ls-tree -r HEAD | awk '{print $1, $3, $4}' | sort)
if [ "$idx" = "$com" ]; then echo "index == HEAD tree ($(wc -l <<<"$idx") entries)"; else echo "INDEX DIFFERS FROM HEAD"; rc=1; fi
# every tracked path: bytes and mode on disk
bad=0; n=0
while read -r mode blob path; do
  n=$((n + 1))
  f="$clone/$path"
  case "$mode" in
    160000) echo "gitlink $path $blob"; continue ;;
    120000) [ -L "$f" ] || { echo "NOT A SYMLINK: $path"; bad=$((bad + 1)); continue; }
            got=$(printf '%s' "$(readlink "$f")" | /usr/bin/git hash-object --stdin) ;;
    100755) [ -f "$f" ] && [ ! -L "$f" ] && [ -x "$f" ] || { echo "MODE/TYPE: $path"; bad=$((bad + 1)); continue; }
            got=$(/usr/bin/git hash-object --no-filters -- "$f") ;;
    100644) [ -f "$f" ] && [ ! -L "$f" ] && [ ! -x "$f" ] || { echo "MODE/TYPE: $path"; bad=$((bad + 1)); continue; }
            got=$(/usr/bin/git hash-object --no-filters -- "$f") ;;
    *) echo "UNKNOWN MODE $mode $path"; bad=$((bad + 1)); continue ;;
  esac
  [ "$got" = "$blob" ] || { echo "BYTES DIFFER: $path"; bad=$((bad + 1)); }
done < <(g ls-tree -r HEAD | awk '{print $1, $3, $4}')
echo "tracked entries re-hashed: $n, mismatches: $bad"
[ "$bad" -eq 0 ] || rc=1
gl=$(g ls-files -s | awk '$1 == "160000"' | wc -l)
echo "gitlinks in index: $gl; .gitmodules: $([ -e "$clone/.gitmodules" ] && echo present || echo absent)"
st=$(g status --porcelain=v1 --ignored --untracked-files=all)
if [ -z "$st" ]; then echo "status: clean (no modified, untracked or ignored entries)"; else echo "STATUS NOT CLEAN:"; echo "$st" | head -20; rc=1; fi
echo "index sha256 $(sha256sum "$clone/.git/index" | cut -d' ' -f1)"
echo "exit $rc"
exit "$rc"
