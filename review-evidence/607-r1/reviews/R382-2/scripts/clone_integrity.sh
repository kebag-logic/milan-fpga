#!/usr/bin/env bash
# Verify the review clone is at the exact head with every tracked blob and mode intact,
# the index tree equal to the head tree, and the submodule gitlinks unchanged.
# Usage: clone_integrity.sh <clone> <expected-head> <expected-tree>
set -uo pipefail
C=$1; HEAD_EXP=$2; TREE_EXP=$3
export GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.commitGraph GIT_CONFIG_VALUE_0=false
cd "$C"
echo "HEAD $(git rev-parse HEAD) (expected $HEAD_EXP)"
echo "index tree $(git write-tree) (expected $TREE_EXP)"
echo "status entries (tracked+untracked, ignored excluded): $(git status --porcelain | wc -l)"
if git diff --quiet HEAD && git diff --cached --quiet; then echo "worktree+index == HEAD (content and mode): yes"; else echo "worktree+index == HEAD: NO"; fi
git ls-files -s | awk '$1=="160000"{print $2, $4}' | while read -r sha path; do
  if [ -e "$path/.git" ]; then co=$(git -C "$path" rev-parse HEAD 2>/dev/null); else co=not-initialised; fi
  echo "gitlink $path index=$sha checkout=$co"
done
mism=0; n=0
while IFS= read -r -d '' rec; do
  meta=${rec%%$'\t'*}; path=${rec#*$'\t'}; mode=${meta%% *}; rest=${meta#* }; sha=${rest%% *}
  [ "$mode" = 160000 ] && continue
  n=$((n+1))
  got=$(git hash-object --no-filters -- "$path" 2>/dev/null || echo missing)
  if [ -L "$path" ]; then fm=120000; elif [ -x "$path" ]; then fm=100755; else fm=100644; fi
  if [ "$got" != "$sha" ] || [ "$fm" != "$mode" ]; then mism=$((mism+1)); echo "MISMATCH $mode $path"; fi
done < <(git ls-files -s -z)
echo "tracked blobs rehashed=$n mismatched=$mism"
