#!/usr/bin/env bash
# clone_integrity.sh CLONE HEAD TREE: prove the review clone is byte-exact at HEAD after the probes.
# Checks HEAD and tree, index vs HEAD, worktree vs index, hidden index flags,
# untracked/ignored paths, every tracked regular file's blob id and mode
# (hashed from disk, so assume-unchanged/skip-worktree cannot hide an edit),
# symlinks, and each gitlink against its checked-out submodule HEAD.
set -uo pipefail
clone=$1 want_head=$2 want_tree=$3
cd "$clone" || exit 2
bad=0
head=$(git rev-parse HEAD); tree=$(git rev-parse 'HEAD^{tree}')
echo "HEAD $head $([ "$head" = "$want_head" ] && echo EXACT || { bad=1; echo MISMATCH; })"
echo "tree $tree $([ "$tree" = "$want_tree" ] && echo EXACT || { bad=1; echo MISMATCH; })"
if git diff --cached --quiet HEAD --; then echo "index vs HEAD: no difference"; else echo "index vs HEAD: DIFFERS"; bad=1; fi
flags=$(git ls-files -v | grep -c -v '^H ' || true)
echo "hidden index flags (non-H entries): $flags"; [ "$flags" = 0 ] || bad=1
status=$(git status --porcelain=v1 --ignored --untracked-files=all | wc -l)
echo "status entries incl. untracked and ignored: $status"; [ "$status" = 0 ] || bad=1
files=0 fmismatch=0 links=0
while IFS=$'\t' read -r meta path; do
  mode=${meta%% *}; rest=${meta#* }; type=${rest%% *}; oid=${rest#* }
  case "$mode" in
    100644|100755)
      files=$((files + 1))
      disk_mode=100644; [ -x "$path" ] && disk_mode=100755
      if [ -L "$path" ] || [ ! -f "$path" ] || [ "$(git hash-object --no-filters -- "$path")" != "$oid" ] || [ "$disk_mode" != "$mode" ]; then
        fmismatch=$((fmismatch + 1)); echo "MISMATCH $mode $path"; fi ;;
    120000)
      links=$((links + 1))
      if [ ! -L "$path" ] || [ "$(printf '%s' "$(readlink -- "$path")" | git hash-object --stdin)" != "$oid" ]; then
        fmismatch=$((fmismatch + 1)); echo "MISMATCH symlink $path"; fi ;;
    160000)
      if [ -e "$path/.git" ]; then
        sub=$(git -C "$path" rev-parse HEAD 2>/dev/null)
        dirty=$(git -C "$path" status --porcelain=v1 --untracked-files=all 2>/dev/null | wc -l)
        echo "gitlink $path pin $oid checkout $sub dirty-entries $dirty $([ "$sub" = "$oid" ] && [ "$dirty" = 0 ] && echo EXACT || echo MISMATCH)"
        { [ "$sub" = "$oid" ] && [ "$dirty" = 0 ]; } || bad=1
      else
        echo "gitlink $path pin $oid uninitialised"
      fi ;;
  esac
done < <(git ls-tree -r --full-tree HEAD)
echo "regular files checked: $files, symlinks: $links, mismatches: $fmismatch"
[ "$fmismatch" = 0 ] || bad=1
echo "RESULT $([ "$bad" = 0 ] && echo EXACT || echo NOT-EXACT)"
exit "$bad"
