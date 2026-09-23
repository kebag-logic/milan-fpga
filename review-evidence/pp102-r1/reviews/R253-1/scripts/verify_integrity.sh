#!/bin/sh
# Prove a clone is byte-exact at an expected commit.
# usage: verify_integrity.sh CLONE HEAD TREE
# Checks: HEAD and tree ids; index == HEAD tree (mode, blob, path, stage 0);
# every tracked worktree file hashes to its recorded blob and has the
# recorded mode; no untracked/ignored leftovers; gitlink (160000) inventory.
set -eu
clone=$1 want_head=$2 want_tree=$3
cd "$clone"
export GIT_NO_REPLACE_OBJECTS=1
fail=0
head=$(git rev-parse HEAD); tree=$(git rev-parse 'HEAD^{tree}')
echo "HEAD $head"; echo "TREE $tree"
[ "$head" = "$want_head" ] || { echo "FAIL: HEAD"; fail=1; }
[ "$tree" = "$want_tree" ] || { echo "FAIL: tree"; fail=1; }
git ls-tree -r --full-tree HEAD | awk '{print $1, $3, $4}' | LC_ALL=C sort > /tmp/.vi_tree.$$
git ls-files -s | awk '{print $1, $2, $3, $4}' > /tmp/.vi_idx_raw.$$
awk '$3 != 0 {bad=1} END {exit bad}' /tmp/.vi_idx_raw.$$ || { echo "FAIL: non-zero index stage"; fail=1; }
awk '{print $1, $2, $4}' /tmp/.vi_idx_raw.$$ | LC_ALL=C sort > /tmp/.vi_idx.$$
if cmp -s /tmp/.vi_tree.$$ /tmp/.vi_idx.$$; then echo "index == HEAD tree: $(wc -l < /tmp/.vi_idx.$$) entries"; else echo "FAIL: index differs from HEAD tree"; fail=1; fi
n=0; while read -r mode blob path; do
  n=$((n + 1))
  case $mode in
    160000) echo "gitlink $path $blob"; continue ;;
    120000) got=$(readlink "$path" | tr -d '\n' | git hash-object --stdin) ;;
    *) got=$(git hash-object --no-filters -- "$path") ;;
  esac
  [ "$got" = "$blob" ] || { echo "FAIL: bytes $path"; fail=1; }
  if [ "$mode" = 100755 ] && [ ! -x "$path" ]; then echo "FAIL: mode $path"; fail=1; fi
  if [ "$mode" = 100644 ] && [ -x "$path" ]; then echo "FAIL: mode $path"; fail=1; fi
done < /tmp/.vi_tree.$$
echo "worktree blobs/modes checked: $n"
echo "gitlinks in HEAD: $(awk '$1 == "160000"' /tmp/.vi_tree.$$ | wc -l)"
left=$(git status --porcelain --ignored --untracked-files=all)
if [ -n "$left" ]; then echo "FAIL: worktree not pristine:"; echo "$left"; fail=1; else echo "status --ignored: pristine"; fi
flags=$(git ls-files -v | awk '$1 != "H"' | head -5)
[ -z "$flags" ] || { echo "FAIL: assume-unchanged/skip-worktree entries: $flags"; fail=1; }
rm -f /tmp/.vi_tree.$$ /tmp/.vi_idx.$$ /tmp/.vi_idx_raw.$$
[ "$fail" = 0 ] && echo "INTEGRITY: PASS" || echo "INTEGRITY: FAIL"
exit "$fail"
