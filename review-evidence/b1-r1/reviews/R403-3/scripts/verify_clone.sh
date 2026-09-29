#!/usr/bin/env bash
# Prove a review clone is byte-exact at the expected head: every tracked blob
# re-hashed from disk (not the stat cache) and compared with HEAD's tree, file
# modes compared, index equal to HEAD, no untracked/ignored residue, and the
# submodule gitlinks recorded plus each initialised submodule's worktree clean.
# usage: verify_clone.sh <clone> <expected-head-sha> <expected-tree-sha>
set -u
cd "$1" || exit 2
export GIT_NO_REPLACE_OBJECTS=1
rc=0
[ "$(git rev-parse HEAD)" = "$2" ] || { echo "HEAD mismatch"; rc=1; }
[ "$(git rev-parse 'HEAD^{tree}')" = "$3" ] || { echo "tree mismatch"; rc=1; }
[ "$(git write-tree)" = "$3" ] || { echo "index tree mismatch"; rc=1; }
n=0; bad=0
while IFS=$'\t' read -r meta path; do
  mode=${meta%% *}; rest=${meta#* }; type=${rest%% *}; oid=${rest#* }
  [ "$type" = blob ] || continue
  n=$((n + 1))
  if [ "$mode" = 120000 ]; then
    got=$(printf '%s' "$(readlink -- "$path")" | git hash-object --stdin)
    [ -L "$path" ] || { echo "not a symlink: $path"; bad=$((bad + 1)); continue; }
  else
    [ -f "$path" ] && [ ! -L "$path" ] || { echo "missing/not regular: $path"; bad=$((bad + 1)); continue; }
    got=$(git hash-object --no-filters -- "$path")
    if [ "$mode" = 100755 ]; then [ -x "$path" ] || { echo "mode lost +x: $path"; bad=$((bad + 1)); }
    else [ -x "$path" ] && { echo "mode gained +x: $path"; bad=$((bad + 1)); }; fi
  fi
  [ "$got" = "$oid" ] || { echo "blob differs: $path"; bad=$((bad + 1)); }
done < <(git ls-tree -r HEAD)
echo "tracked blobs re-hashed: $n, differing: $bad"
[ "$bad" = 0 ] || rc=1
res=$(git status --porcelain --ignored --untracked-files=all)
[ -z "$res" ] && echo "no untracked/ignored residue" || { echo "residue:"; echo "$res"; rc=1; }
echo "gitlinks (HEAD tree):"; git ls-tree -r HEAD | awk '$2=="commit"{print "  "$1, $3, $4}'
echo "gitlinks (index):"; git ls-files -s | awk '$1=="160000"{print "  "$1, $2, "stage", $3, $4}'
git submodule status | sed 's/^/  status: /'
git submodule foreach --quiet 'd=$(git status --porcelain --untracked-files=all); h=$(git rev-parse HEAD); echo "  $sm_path at $h clean=$([ -z "$d" ] && echo yes || echo NO)"'
echo "verify_clone rc=$rc"
exit $rc
