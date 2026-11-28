#!/bin/sh
# Usage: restore_check.sh <clone> <head> <tree>. Confirms HEAD and its tree, an index equal to the tree
# (paths, modes, blobs), a working tree whose every tracked file hashes to its index blob with its mode,
# no untracked or ignored files, and lists the gitlinks (submodules) the tree records.
set -u
C=$1; H=$2; T=$3; ok=0
cd "$C" || exit 2
[ "$(git rev-parse HEAD)" = "$H" ] && echo "HEAD $H" || { echo "HEAD mismatch"; ok=1; }
[ "$(git rev-parse HEAD^{tree})" = "$T" ] && echo "tree $T" || { echo "tree mismatch"; ok=1; }
[ "$(git write-tree)" = "$T" ] && echo "index writes tree $T" || { echo "index differs from tree"; ok=1; }
git ls-files -s | while read -r mode blob stage path; do
  [ "$mode" = 160000 ] && continue
  [ "$(git hash-object -- "$path")" = "$blob" ] || echo "BLOB MISMATCH $path"
  if [ "$mode" = 100755 ]; then [ -x "$path" ] || echo "MODE MISMATCH $path"; else [ ! -x "$path" ] || echo "MODE MISMATCH $path"; fi
done > /tmp/restore_check.$$ ; if [ -s /tmp/restore_check.$$ ]; then cat /tmp/restore_check.$$; ok=1; else echo "every tracked file matches its blob and mode ($(git ls-files | wc -l) files)"; fi; rm -f /tmp/restore_check.$$
st=$(git status --porcelain --ignored --untracked-files=all); [ -z "$st" ] && echo "no modified, untracked or ignored files" || { echo "$st"; ok=1; }
g=$(git ls-tree -r HEAD | awk '$1=="160000"'); [ -z "$g" ] && echo "gitlinks: none recorded in the tree (no submodule to verify)" || echo "gitlinks: $g"
echo "restore check: $([ $ok -eq 0 ] && echo pass || echo FAIL)"
