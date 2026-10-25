#!/usr/bin/env bash
# Verify a clone's tracked bytes, modes, index and submodule gitlinks against HEAD without the stat cache.
set -u
cd "${1:?repo}" || exit 2
rc=0
echo "HEAD $(git rev-parse HEAD) tree $(git rev-parse HEAD^{tree})"
[ "$(git write-tree)" = "$(git rev-parse HEAD^{tree})" ] && echo "index tree == HEAD tree" || { echo "INDEX MISMATCH"; rc=1; }
git -c core.checkStat=minimal update-index -q --really-refresh >/dev/null 2>&1
git diff --quiet HEAD -- && echo "worktree tracked diff: none" || { echo "WORKTREE DIFF"; rc=1; }
# raw bytes of every regular file / symlink against its blob
n=0; bad=0
while IFS=$'\t' read -r meta path; do
  set -- $meta; mode=$1; oid=$3
  case "$mode" in
    160000) continue ;;
    120000) got=$(readlink -- "$path" | tr -d '\n' | git hash-object --stdin) ;;
    *) got=$(git hash-object --no-filters -- "$path");
       if [ "$mode" = 100755 ] && [ ! -x "$path" ]; then echo "MODE $path"; bad=$((bad+1)); fi
       if [ "$mode" = 100644 ] && [ -x "$path" ]; then echo "MODE $path"; bad=$((bad+1)); fi ;;
  esac
  n=$((n+1)); [ "$got" = "$oid" ] || { echo "BYTES $path"; bad=$((bad+1)); }
done < <(git ls-tree -r HEAD)
echo "checked $n blobs, mismatches $bad"; [ "$bad" = 0 ] || rc=1
git ls-tree -r HEAD | awk '$1=="160000"{print $3, $4}' | while read -r oid path; do
  if [ -e "$path/.git" ]; then got=$(git -C "$path" rev-parse HEAD); st="init"; else got="(uninitialized)"; st="uninit"; fi
  echo "gitlink $path $oid $st $([ "$got" = "$oid" ] && echo match || echo "$got")"
done
echo "untracked (non-ignored): $(git status --porcelain --untracked-files=all | grep -c '^??')"
exit $rc
