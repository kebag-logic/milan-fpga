#!/bin/sh
# usage: verify_clone.sh <clone> <expected head>
# Proves the clone is the exact head: HEAD and tree, index == HEAD tree (paths, modes, object ids, stage 0),
# no assume-unchanged/skip-worktree flags, every tracked regular file and symlink hashed from disk equals its
# index blob, executable bits match modes, gitlinks recorded and submodule checkouts at them.
set -u
C=$1; H=$2; cd "$C" || exit 2
echo "HEAD $(git rev-parse HEAD) (expected $H) tree $(git rev-parse HEAD^{tree})"
[ "$(git rev-parse HEAD)" = "$H" ] || { echo "HEAD MISMATCH"; exit 1; }
a=$(git ls-files -s | sha256sum); b=$(git ls-tree -r --full-tree HEAD | awk '{print $1" "$3" 0\t"$4}' | sha256sum)
[ "$a" = "$b" ] && echo "index == HEAD tree (mode, id, stage, path)" || { echo "INDEX DIFFERS FROM HEAD"; exit 1; }
f=$(git ls-files -v | grep -vc '^H ' || true); echo "entries flagged other than H (assume-unchanged/skip-worktree/etc): $f"
bad=0; n=0
git ls-files -s | while read -r mode oid stage path; do
  case $mode in
    160000) continue;;
    120000) got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin);;
    *) got=$(git hash-object --no-filters -- "$path"); x=0; [ -x "$path" ] && x=1; w=0; [ "$mode" = 100755 ] && w=1; [ $x = $w ] || echo "MODE $path";;
  esac
  [ "$got" = "$oid" ] || echo "BLOB $path"
done > /tmp/vc.$$
echo "tracked files whose disk bytes or exec bit differ from the index: $(wc -l < /tmp/vc.$$)"; head -5 /tmp/vc.$$; rm -f /tmp/vc.$$
echo "untracked/modified per status: $(git status --porcelain --ignore-submodules=none | wc -l); ignored files present: $(git status --porcelain --ignored | grep -c '^!!')"
git ls-files -s | awk '$1==160000{print $2" "$4}' | while read -r oid path; do
  if [ -e "$path/.git" ]; then echo "gitlink $path $oid checkout $(git -C "$path" rev-parse HEAD) dirty=$(git -C "$path" status --porcelain | wc -l)"; else echo "gitlink $path $oid (not initialised)"; fi
done
