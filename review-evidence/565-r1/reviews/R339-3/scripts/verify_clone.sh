#!/usr/bin/env bash
# Verify a review clone sits at the exact reviewed head with no residue:
# HEAD/tree, index == HEAD tree, every tracked blob's bytes and mode, no
# hidden index flags, no untracked or ignored files, submodule gitlinks.
# Usage: verify_clone.sh <repo> <head-sha> <tree-sha>
set -u
cd "$1" || exit 2
H=$2; T=$3; fail=0
chk() { if [ "$2" = "$3" ]; then echo "OK   $1"; else echo "FAIL $1: got '$2' want '$3'"; fail=1; fi; }
chk HEAD "$(git rev-parse HEAD)" "$H"
chk HEAD-tree "$(git rev-parse HEAD^{tree})" "$T"
chk index-tree "$(git write-tree)" "$T"
git update-index --really-refresh >/dev/null 2>&1
chk worktree-vs-index "$(git diff --name-only | wc -l)" 0
chk index-vs-HEAD "$(git diff --cached --name-only | wc -l)" 0
chk hidden-flags "$(git ls-files -v | grep -c -v '^H ')" 0
chk untracked+ignored "$(git status --porcelain --ignored --untracked-files=all | wc -l)" 0
# tracked blob bytes and modes, recomputed from the worktree
n=0; bad=0
while IFS=$'\t' read -r meta path; do
  set -- $meta; mode=$1; type=$2; oid=$3
  [ "$type" = blob ] || continue
  n=$((n+1))
  if [ "$mode" = 120000 ]; then got=$(printf %s "$(readlink "$path")" | git hash-object --stdin)
  else got=$(git hash-object --no-filters "$path"); fi
  [ "$got" = "$oid" ] || { echo "FAIL blob $path"; bad=$((bad+1)); }
  if [ "$mode" = 100755 ] && [ ! -x "$path" ]; then echo "FAIL mode $path"; bad=$((bad+1)); fi
  if [ "$mode" = 100644 ] && [ -x "$path" ]; then echo "FAIL mode $path"; bad=$((bad+1)); fi
done < <(git ls-tree -r "$H")
chk "tracked-blobs($n)-mismatches" "$bad" 0
echo "gitlinks at HEAD:"; git ls-tree -r "$H" | awk '$2=="commit"{print "  "$3, $4}'
git submodule status 2>/dev/null | sed 's/^/  submodule-status: /'
for p in $(git ls-tree -r "$H" | awk '$2=="commit"{print $4}'); do
  want=$(git ls-tree "$H" "$p" | awk '{print $3}')
  if [ -e "$p/.git" ]; then chk "gitlink $p" "$(git -C "$p" rev-parse HEAD)" "$want"
    chk "gitlink $p clean" "$(git -C "$p" status --porcelain | wc -l)" 0
  else echo "INFO gitlink $p not checked out (index gitlink $(git ls-files -s "$p" | awk '{print $2}'))"
    chk "gitlink $p index" "$(git ls-files -s "$p" | awk '{print $2}')" "$want"; fi
done
[ $fail -eq 0 ] && [ $bad -eq 0 ] && echo "RESULT: CLEAN" || { echo "RESULT: NOT CLEAN"; exit 1; }
