#!/bin/sh
# verify_clone.sh CLONE HEAD TREE : prove the review clone holds exact head bytes.
# Checks HEAD, the index tree, that every tracked file rehashes to its index
# blob with its index mode, no untracked or ignored entries, and each
# initialised submodule at its gitlink and clean.
set -u
C=$1; H=$2; T=$3; rc=0
cd "$C" || exit 2
[ "$(git rev-parse HEAD)" = "$H" ] && echo "HEAD $H ok" || { echo "HEAD mismatch"; rc=1; }
[ "$(git write-tree)" = "$T" ] && echo "index tree $T ok" || { echo "index tree mismatch"; rc=1; }
git update-index -q --really-refresh >/dev/null 2>&1
if git diff-files --quiet && git diff-index --cached --quiet HEAD; then
  echo "worktree and index equal HEAD (content and mode)"
else
  echo "worktree/index differ from HEAD"; git diff-files --name-status | head; rc=1
fi
n=$(git ls-files -s | awk '$1!="160000"' | wc -l)
bad=0
git ls-files -s | awk '$1!="160000"{print $1" "$2" "$4}' | while read -r mode blob path; do
  [ "$(git hash-object -- "$path")" = "$blob" ] || { echo "BLOB MISMATCH $path"; exit 1; }
  m=$(stat -c %a -- "$path"); case "$mode:$m" in 100644:6[04][04]|100755:7[05][05]|120000:*) ;; *) echo "MODE MISMATCH $path $mode $m"; exit 1;; esac
done || bad=1
[ $bad = 0 ] && echo "rehashed $n tracked files: blobs and modes match" || rc=1
u=$(git status --short --ignored | wc -l)
[ "$u" = 0 ] && echo "no untracked or ignored entries" || { echo "$u untracked/ignored entries"; rc=1; }
git ls-tree -r HEAD | awk '$2=="commit"{print $3" "$4}' | while read -r sha path; do
  if [ -e "$path/.git" ]; then
    got=$(git -C "$path" rev-parse HEAD); st=$(git -C "$path" status --short --ignored | wc -l)
    [ "$got" = "$sha" ] && [ "$st" = 0 ] && echo "gitlink $path $sha ok, clean" || { echo "gitlink $path got $got want $sha dirty=$st"; exit 1; }
  else
    echo "gitlink $path $sha (not initialised, as at start)"
  fi
done || rc=1
echo "rc=$rc"; exit $rc
