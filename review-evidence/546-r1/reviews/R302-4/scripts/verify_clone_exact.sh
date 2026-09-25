#!/bin/sh
# Verify a clone is at an exact head with tracked bytes, modes, index and gitlinks unchanged.
# Usage: verify_clone_exact.sh <clone> <head-sha> <tree-sha>
set -eu
C=$1; H=$2; T=$3
cd "$C"
[ "$(git rev-parse HEAD)" = "$H" ] || { echo "HEAD mismatch"; exit 1; }
[ "$(git rev-parse HEAD^{tree})" = "$T" ] || { echo "tree mismatch"; exit 1; }
# index entries (mode, blob, path) equal HEAD tree entries
git ls-files -s | awk '{print $1" "$2" "$4}' > /tmp/.idx.$$
git ls-tree -r --full-tree HEAD | awk '{print $1" "$3" "$4}' > /tmp/.tree.$$
cmp -s /tmp/.idx.$$ /tmp/.tree.$$ || { echo "index differs from HEAD tree"; exit 1; }
# every tracked regular file / symlink hashes to its index blob and has the index mode
bad=0; n=0
git ls-files -s | while read -r mode blob stage path; do
  case $mode in
    160000) if [ -e "$path/.git" ]; then sub=$(git -C "$path" rev-parse HEAD); else sub=absent; fi
            [ "$sub" = "$blob" ] || [ "$sub" = absent ] || { echo "gitlink checkout differs: $path $sub != $blob"; exit 1; } ;;
    120000) [ "$(readlink "$path" | tr -d '\n' | git hash-object --stdin)" = "$blob" ] || { echo "symlink differs: $path"; exit 1; } ;;
    *) [ "$(git hash-object --no-filters -- "$path")" = "$blob" ] || { echo "bytes differ: $path"; exit 1; }
       x=100644; [ -x "$path" ] && x=100755; [ "$x" = "$mode" ] || { echo "mode differs: $path"; exit 1; } ;;
  esac
done
rm -f /tmp/.idx.$$ /tmp/.tree.$$
[ -z "$(git status --porcelain --ignored)" ] || { echo "untracked/ignored/modified paths present"; git status --porcelain --ignored; exit 1; }
echo "tracked files: $(git ls-files | wc -l)"
git ls-tree HEAD protocol-processor gptp-processor third_party/verilog-axis external
git submodule status
echo "CLONE EXACT: $H $T"
