#!/usr/bin/env bash
# integrity.sh: the review clone against its exact head: HEAD and tree, the index unchanged since the round began
# (scratch/index_before.txt), every tracked file's bytes and mode equal to its blob (git diff and a re-hash of each
# worktree file), no untracked or ignored file, and each initialised submodule at its gitlink and clean.
set -u
L=${CLONE:?export CLONE, the review clone at the exact head}
P=${PACKET:?export PACKET, this packet directory}
cd "$L" || exit 3
bad=0
say() { echo "$1"; [ "$2" = ok ] || bad=1; }
[ "$(git rev-parse HEAD)" = afa3ea19d6a1075382c63e4fc1e188a9aadf33bb ] && say "HEAD afa3ea19d6a1075382c63e4fc1e188a9aadf33bb" ok || say "HEAD moved" bad
[ "$(git rev-parse HEAD^{tree})" = 406dc4ba57ae0b7e1f06f5e400356872cabc32af ] && say "tree 406dc4ba57ae0b7e1f06f5e400356872cabc32af" ok || say "tree differs" bad
git ls-files -s > "$P/scratch/index_after.txt"
cmp -s "$P/scratch/index_before.txt" "$P/scratch/index_after.txt" && say "index: identical to the round's start ($(wc -l < "$P/scratch/index_after.txt") entries)" ok || say "index changed" bad
git diff --quiet && git diff --cached --quiet && say "git diff (worktree and index): empty" ok || say "git diff not empty" bad
# re-hash every regular tracked file and compare with its blob and mode
mism=0
while IFS=$'\t' read -r meta path; do
  mode=${meta%% *}; rest=${meta#* }; blob=${rest%% *}
  [ "$mode" = 160000 ] && continue
  if [ "$mode" = 120000 ]; then
    [ -L "$path" ] && [ "$(printf %s "$(readlink "$path")" | git hash-object --stdin)" = "$blob" ] || { echo "symlink mismatch $path"; mism=$((mism+1)); }
    continue
  fi
  [ -f "$path" ] || { echo "missing $path"; mism=$((mism+1)); continue; }
  [ "$(git hash-object --no-filters "$path")" = "$blob" ] || { echo "bytes mismatch $path"; mism=$((mism+1)); }
  x=$([ -x "$path" ] && echo 100755 || echo 100644)
  [ "$x" = "$mode" ] || { echo "mode mismatch $path"; mism=$((mism+1)); }
done < <(git ls-files -s | awk '{print $1" "$2"\t"$4}')
[ "$mism" = 0 ] && say "tracked files: every blob's bytes and mode match" ok || say "tracked files: $mism mismatch(es)" bad
extra=$(git status --porcelain --ignored --untracked-files=all | wc -l)
[ "$extra" = 0 ] && say "untracked or ignored files: none" ok || { git status --porcelain --ignored --untracked-files=all | head; say "untracked or ignored files: $extra" bad; }
while read -r line; do
  sha=$(echo "$line" | awk '{print $1}' | sed 's/^[-+U ]//'); path=$(echo "$line" | awk '{print $2}')
  want=$(git ls-tree HEAD "$path" | awk '{print $3}')
  case "$line" in
    -*) say "submodule $path: not initialised, gitlink $want" ok ;;
    *) dirty=$(git -C "$path" status --porcelain --ignored --untracked-files=all | wc -l)
       [ "$sha" = "$want" ] && [ "$dirty" = 0 ] && say "submodule $path: at gitlink $want, clean" ok || say "submodule $path: $sha vs $want, $dirty change(s)" bad ;;
  esac
done < <(git submodule status)
echo "integrity: $([ $bad = 0 ] && echo PASS || echo FAIL)"
exit $bad
