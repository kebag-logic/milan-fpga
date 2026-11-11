#!/usr/bin/env bash
# verify_restore.sh CLONE BASELINE_INDEX BASELINE_SUBMODULES: the clone is back at the exact head with every
# tracked blob, mode and index entry and every submodule gitlink as recorded before the probes.
set -u
clone=$1; index=$2; subs=$3
cd "$clone" || exit 2
head=$(git rev-parse HEAD); tree=$(git rev-parse HEAD^{tree})
echo "HEAD $head"; echo "tree $tree"
[ "$head" = a91fb27dd39483e4694e193504da1dbe06208807 ] || { echo "HEAD MISMATCH"; exit 1; }
[ "$tree" = 29f1691c9d5b4fee0d316940754187bae737b137 ] || { echo "TREE MISMATCH"; exit 1; }
git ls-files -s | diff -q - "$index" >/dev/null && echo "index entries (mode, blob, stage, path): identical to baseline" \
  || { echo "INDEX DIFFERS"; exit 1; }
git submodule status | diff -q - "$subs" >/dev/null && echo "submodule gitlinks: identical to baseline" \
  || { echo "SUBMODULES DIFFER"; exit 1; }
git diff --quiet && git diff --cached --quiet && echo "worktree and index: no tracked change against HEAD" \
  || { echo "TRACKED CHANGE"; git status --porcelain; exit 1; }
# every tracked file's bytes against its blob (catches a change git's stat cache could miss)
bad=0
while IFS=$'\t' read -r meta path; do
  set -- $meta; mode=$1; blob=$2
  [ "$mode" = 160000 ] && continue
  [ "$mode" = 120000 ] && { [ "$(git hash-object --stdin < <(printf %s "$(readlink "$path")"))" = "$blob" ] || bad=$((bad+1)); continue; }
  [ "$(git hash-object "$path")" = "$blob" ] || { echo "BYTES DIFFER: $path"; bad=$((bad+1)); }
done < <(git ls-files -s)
echo "tracked files whose bytes differ from their blob: $bad"
untracked=$(git status --porcelain --untracked-files=all | grep -c '^??')
echo "untracked (non-ignored) files: $untracked"
[ $bad -eq 0 ] && [ "$untracked" -eq 0 ]
