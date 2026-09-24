#!/usr/bin/env bash
# Record the review clone's state: HEAD, tree, index vs HEAD, every tracked blob rehashed with its mode,
# index flags, untracked/ignored files, and each gitlink against its checked-out submodule HEAD.
# Usage: tree_state.sh <repo-root>
set -u
cd "$1" || exit 2
echo "HEAD $(git rev-parse HEAD)"
echo "tree $(git rev-parse 'HEAD^{tree}')"
echo "write-tree $(git write-tree)"
echo "index-vs-HEAD entries: $(git diff-index --cached HEAD | wc -l)"
echo "worktree-vs-index entries: $(git diff-files | wc -l)"
echo "core.fileMode=$(git config --get core.fileMode)"
echo "index flags other than H (assume-unchanged/skip-worktree): $(git ls-files -v | grep -v -c '^H ')"
mism=0; n=0
while IFS=$'\t' read -r meta path; do
  mode=${meta%% *}; rest=${meta#* }; oid=${rest%% *}
  [ "$mode" = 160000 ] && continue
  n=$((n+1))
  if [ "$mode" = 120000 ]; then got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)
  else got=$(git hash-object --no-filters -- "$path"); fi
  fm=100644; [ -x "$path" ] && fm=100755; [ -L "$path" ] && fm=120000
  if [ "$got" != "$oid" ] || [ "$fm" != "$mode" ]; then mism=$((mism+1)); echo "MISMATCH $mode $oid $path"; fi
done < <(git ls-files -s | sed -E 's/^([0-9]+) ([0-9a-f]+) ([0-3])\t/\1 \2 \3\t/')
echo "tracked regular/symlink blobs rehashed: $n, mismatches: $mism"
echo "untracked: $(git ls-files --others --exclude-standard | wc -l)"
echo "ignored (outside submodules): $(git ls-files --others --ignored --exclude-standard --directory | wc -l)"
git ls-files -s | awk '$1==160000{print $2, $4}' | while read -r oid path; do
  if [ -e "$path/.git" ]; then sh=$(git -C "$path" rev-parse HEAD); dirty=$(git -C "$path" status --porcelain --ignored | wc -l)
  else sh=uninitialised; dirty=-; fi
  echo "gitlink $path $oid checkout=$sh dirty+ignored=$dirty"
done
