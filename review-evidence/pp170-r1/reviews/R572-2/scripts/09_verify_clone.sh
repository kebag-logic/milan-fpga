#!/bin/bash
# Verify the review clone is at exact-head bytes: HEAD, tree, index tree,
# every tracked blob's bytes and mode, no untracked or ignored files, gitlinks.
set -u; . "$(dirname "$0")/env.sh"
cd "$SRC" || exit 2
echo "HEAD $(git rev-parse HEAD) (want $HEAD_SHA)"
echo "tree $(git rev-parse HEAD^{tree}) index-tree $(git write-tree)"
echo "tracked entries $(git ls-files | wc -l); gitlinks $(git ls-files -s | awk '$1==160000' | wc -l)"
echo "diff-index: $(git diff-index --name-only HEAD | wc -l) changed"
echo "untracked+ignored: $(git ls-files --others | wc -l)"
git status --porcelain --ignored | head
cnt=0; mism=0
while read -r mode sha path; do
  cnt=$((cnt+1))
  [ "$(git hash-object --no-filters -- "$path")" = "$sha" ] || { mism=$((mism+1)); echo "bytes $path"; }
  fm=$(stat -c %a -- "$path")
  case "$mode:$fm" in 100755:7??|100644:6??) ;; *) mism=$((mism+1)); echo "mode $path $mode $fm";; esac
done < <(git ls-files -s | awk '$1!="160000"{print $1" "$2" "$4}')
echo "blobs checked $cnt, byte/mode mismatches $mism"
