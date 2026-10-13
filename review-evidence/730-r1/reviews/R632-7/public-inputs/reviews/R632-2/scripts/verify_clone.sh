#!/usr/bin/env bash
# Verify a review clone still holds the exact head: HEAD, tree, index == tree
# (modes and blob ids), every tracked regular file's bytes and exec bit,
# symlink targets, no untracked or modified files, and each initialized
# submodule's checkout at its gitlink. Usage: verify_clone.sh CLONE HEAD TREE
set -u
C=$1; HEAD=$2; TREE=$3; rc=0
cd "$C" || exit 2
[ "$(git rev-parse HEAD)" = "$HEAD" ] && echo "HEAD ok $HEAD" || { echo "HEAD MISMATCH"; rc=1; }
[ "$(git rev-parse HEAD^{tree})" = "$TREE" ] && echo "tree ok $TREE" || { echo "tree MISMATCH"; rc=1; }
idx=$(git ls-files -s | awk '{print $1, $2, $4}' | sha256sum | cut -d' ' -f1)
tre=$(git ls-tree -r --full-tree HEAD | awk '{print $1, $3, $4}' | sha256sum | cut -d' ' -f1)
[ "$idx" = "$tre" ] && echo "index == tree (mode, id, path) digest $idx" || { echo "index != tree"; rc=1; }
bad=0; n=0
while IFS=$'\t' read -r meta path; do
  set -- $meta; mode=$1; id=$2
  case $mode in
    160000) continue ;;
    120000) got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin) ;;
    *) got=$(git hash-object --no-filters -- "$path")
       if [ "$mode" = 100755 ] && [ ! -x "$path" ]; then echo "mode drift $path"; bad=$((bad+1)); fi
       if [ "$mode" = 100644 ] && [ -x "$path" ]; then echo "mode drift $path"; bad=$((bad+1)); fi ;;
  esac
  n=$((n+1))
  [ "$got" = "$id" ] || { echo "bytes drift $path"; bad=$((bad+1)); }
done < <(git ls-files -s | awk '{printf "%s %s\t", $1, $2; for (i=4;i<=NF;i++) printf "%s%s", $i, (i<NF?" ":""); print ""}')
[ $bad -eq 0 ] && echo "tracked bytes/modes ok ($n entries re-hashed)" || { echo "$bad drift(s)"; rc=1; }
st=$(git status --porcelain --untracked-files=all)
[ -z "$st" ] && echo "status clean (no modified or untracked files)" || { echo "status not clean:"; echo "$st"; rc=1; }
git ls-files -s | awk '$1=="160000"{print $2, $4}' | while read -r id path; do
  if [ -e "$path/.git" ]; then
    sub=$(git -C "$path" rev-parse HEAD)
    [ "$sub" = "$id" ] && echo "submodule $path at gitlink $id" || echo "SUBMODULE DRIFT $path $sub != $id"
  else
    echo "submodule $path uninitialized (gitlink $id)"
  fi
done
exit $rc
