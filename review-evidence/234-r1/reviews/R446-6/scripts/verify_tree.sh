#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Verify a review checkout is the exact head after probes: HEAD and tree, no status or ignored file, index equal to
# HEAD, every tracked blob's bytes and mode equal to HEAD's, the gitlinks against a base commit, and each
# initialised submodule clean at its gitlink. Exit 0 only when all hold.
# Usage: verify_tree.sh <checkout> <head> <base>
set -u
cd "$1" || exit 2
HEAD=$2; BASE=$3; bad=0
echo "date $(date -u +%FT%TZ)"
echo "HEAD $(git rev-parse HEAD) tree $(git rev-parse HEAD^{tree})"
[ "$(git rev-parse HEAD)" = "$HEAD" ] || { echo "HEAD is not $HEAD"; bad=1; }
s=$(git status --porcelain=v1 --untracked-files=all); echo "status-porcelain:"; [ -n "$s" ] && { echo "$s"; bad=1; }
i=$(git status --porcelain=v1 --ignored=matching | grep '^!!'); echo "ignored:"; [ -n "$i" ] && { echo "$i"; bad=1; }
git diff-index --cached --quiet HEAD; r=$?; echo "diff-index-cached rc: $r"; [ $r = 0 ] || bad=1
git diff-files --quiet; r=$?; echo "diff-files rc: $r"; [ $r = 0 ] || bad=1
echo "tracked blobs of worktree vs HEAD (bytes and mode):"
mism=0; n=0
while IFS= read -r -d '' rec; do
  meta=${rec%%	*}; path=${rec#*	}; set -- $meta; mode=$1; type=$2; obj=$3
  [ "$type" = blob ] || continue
  n=$((n + 1))
  if [ "$mode" = 120000 ]; then
    [ -L "$path" ] && [ "$(printf %s "$(readlink "$path")" | git hash-object --stdin)" = "$obj" ] || { echo "MISMATCH $path"; mism=$((mism + 1)); }
    continue
  fi
  [ -f "$path" ] && [ ! -L "$path" ] && [ "$(git hash-object --no-filters "$path")" = "$obj" ] || { echo "MISMATCH $path"; mism=$((mism + 1)); continue; }
  want=$([ "$mode" = 100755 ] && echo x || echo -); have=$([ -x "$path" ] && echo x || echo -)
  [ "$want" = "$have" ] || { echo "MODE $path"; mism=$((mism + 1)); }
done < <(git ls-tree -r -z HEAD)
echo "checked $n tracked files, $mism mismatches"; [ $mism = 0 ] || bad=1
echo "gitlinks (HEAD; base $BASE):"
git ls-tree -r HEAD | awk '$1 == "160000"'
[ "$(git ls-tree -r HEAD | awk '$1 == "160000"')" = "$(git ls-tree -r "$BASE" | awk '$1 == "160000"')" ] && echo "gitlinks equal to base" || { echo "gitlinks DIFFER from base"; bad=1; }
git submodule status
git submodule status | while read -r line; do
  case $line in -*) continue ;; esac
  set -- $line; sha=${1#[+U ]}; path=$2
  d=$(git -C "$path" status --porcelain=v1 --untracked-files=all | wc -l); ig=$(git -C "$path" status --porcelain=v1 --ignored=matching | grep -c '^!!')
  echo "$path: $(git -C "$path" rev-parse HEAD) dirty=$d ignored=$ig"
done
git submodule status | grep -q '^[+U]' && bad=1
for path in $(git submodule status | awk '$1 !~ /^-/ {print $2}'); do
  [ "$(git -C "$path" status --porcelain=v1 --untracked-files=all --ignored=matching | wc -l)" = 0 ] || bad=1
done
echo "verify_tree: $([ $bad = 0 ] && echo PASS || echo FAIL)"
exit $bad
