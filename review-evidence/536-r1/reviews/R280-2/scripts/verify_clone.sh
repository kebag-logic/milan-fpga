#!/bin/sh
# Verify the review clone is byte-exact at the reviewed head after probes.
# Usage: verify_clone.sh <clone> <head> <tree>
set -u
c=$1; head=$2; tree=$3
cd "$c" || exit 2
echo "HEAD $(git rev-parse HEAD) expected $head"
echo "tree $(git rev-parse HEAD^{tree}) expected $tree"
echo "status (incl. ignored, superproject):"; git status --porcelain --ignored --untracked-files=all; echo "(end)"
echo "index vs HEAD: $(git diff --cached --quiet HEAD && echo identical || echo DIFFERS)"
echo "worktree vs index: $(git diff --quiet && echo identical || echo DIFFERS)"
echo "skip-worktree/assume-unchanged entries: $(git ls-files -v | grep -c '^[a-zS]')"
bad=0; n=0
git ls-files -s | while read mode oid stage path; do
  [ "$mode" = 160000 ] && continue
  if [ "$mode" = 120000 ]; then h=$(readlink "$path" | tr -d '\n' | git hash-object --stdin); else h=$(git hash-object --no-filters "$path"); fi
  m=$(stat -c %a "$path"); case "$mode" in 100755) want=755;; 100644) want=644;; 120000) want=$m;; esac
  if [ "$h" != "$oid" ] || { [ "$mode" != 120000 ] && [ "$(( 0$m & 0111 ))" != "$(( 0$want & 0111 ))" ]; }; then echo "MISMATCH $mode $path"; fi
done > /tmp/r280_2_blob_check.$$ 
echo "tracked blobs re-hashed: $(git ls-files -s | grep -vc '^160000'), mismatches: $(grep -c . /tmp/r280_2_blob_check.$$)"; cat /tmp/r280_2_blob_check.$$; rm -f /tmp/r280_2_blob_check.$$
echo "gitlinks:"; git ls-files -s | grep '^160000'
echo "submodule status:"; git submodule status
for s in protocol-processor gptp-processor; do
  echo "$s: HEAD $(git -C $s rev-parse HEAD), status:"; git -C $s status --porcelain --ignored --untracked-files=all; echo "(end)"
  echo "$s index vs HEAD: $(git -C $s diff --cached --quiet HEAD && echo identical || echo DIFFERS); worktree vs index: $(git -C $s diff --quiet && echo identical || echo DIFFERS)"
done
echo "protocol-processor tracked blobs re-hashed: $(git -C protocol-processor ls-files -s | grep -vc '^160000'), mismatches: $(git -C protocol-processor ls-files -s | while read mode oid st path; do [ "$mode" = 160000 ] && continue; [ "$(git -C protocol-processor hash-object --no-filters "$path")" = "$oid" ] || echo x; done | grep -c x)"
