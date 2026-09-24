#!/bin/sh
# Record the checkout's integrity: HEAD, tree, index, tracked bytes and modes,
# gitlinks and submodule checkouts. Usage: integrity.sh <repo> <out-file>
set -eu
repo=$1
out=$2
cd "$repo"
{
  echo "HEAD $(git rev-parse HEAD)"
  echo "TREE $(git rev-parse 'HEAD^{tree}')"
  echo "INDEX_TREE $(git write-tree)"
  echo "INDEX_STAGE_SHA256 $(git ls-files -s | sha256sum | cut -d' ' -f1)"
  # hash every tracked regular file's working bytes and compare to HEAD blobs
  bad=0
  git ls-tree -r HEAD | while read -r mode type obj path; do
    [ "$type" = blob ] || continue
    wobj=$(git hash-object --no-filters -- "$path")
    if [ "$wobj" != "$obj" ]; then echo "BYTES_MISMATCH $path"; fi
    if [ "$mode" = 100755 ] && [ ! -x "$path" ]; then echo "MODE_MISMATCH $path"; fi
    if [ "$mode" = 100644 ] && [ -x "$path" ]; then echo "MODE_MISMATCH $path"; fi
  done
  echo "TRACKED_BLOBS $(git ls-tree -r HEAD | awk '$2=="blob"' | wc -l)"
  echo "STATUS_PORCELAIN_BEGIN"
  git status --porcelain=v1 --untracked-files=all
  echo "STATUS_PORCELAIN_END"
  echo "GITLINKS"
  git ls-tree -r HEAD | awk '$2=="commit"{print $3, $4}'
  echo "SUBMODULE_STATUS"
  git submodule status
}  > "$out"
