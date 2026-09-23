#!/usr/bin/env bash
# Integrity snapshot of a review clone: HEAD, tree, index hash, every tracked
# entry's mode/object ID re-hashed from the worktree bytes, and gitlinks.
# Usage: integrity.sh <clone> <out-file>
set -euo pipefail
clone=$1 out=$2
cd "$clone"
{
  echo "HEAD $(git rev-parse HEAD)"
  echo "TREE $(git rev-parse HEAD^{tree})"
  echo "INDEX_SHA256 $(sha256sum .git/index | cut -d' ' -f1)"
  echo "STATUS_PORCELAIN_LINES $(git status --porcelain=v1 --ignore-submodules=none | wc -l)"
  # every tracked entry: index mode/oid vs HEAD tree mode/oid vs worktree re-hash
  mismatch=0 total=0
  while IFS= read -r -d '' rec; do
    meta=${rec%%$'\t'*}; path=${rec#*$'\t'}
    mode=${meta%% *}; rest=${meta#* }; oid=${rest%% *}
    total=$((total+1))
    if [ "$mode" = 160000 ]; then
      if [ -e "$path/.git" ]; then sub=$(git -C "$path" rev-parse HEAD 2>/dev/null || echo unreadable); else sub=uninitialised; fi
      echo "GITLINK $path $oid checkout=$sub"
      continue
    fi
    if [ "$mode" = 120000 ]; then
      got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)
      [ -L "$path" ] || { echo "KIND_MISMATCH $path"; mismatch=$((mismatch+1)); }
    else
      got=$(git hash-object --no-filters -- "$path")
      want_x=$([ "$mode" = 100755 ] && echo x || echo -)
      have_x=$([ -x "$path" ] && echo x || echo -)
      [ "$want_x" = "$have_x" ] || { echo "MODE_MISMATCH $path $mode"; mismatch=$((mismatch+1)); }
    fi
    [ "$got" = "$oid" ] || { echo "BLOB_MISMATCH $path want=$oid got=$got"; mismatch=$((mismatch+1)); }
  done < <(git ls-files -s -z | sed -z 's/^\([0-9]*\) \([0-9a-f]*\) [0-9]*\t/\1 \2\t/')
  echo "TRACKED_ENTRIES $total"
  echo "MISMATCHES $mismatch"
  echo "INDEX_VS_HEAD_DIFF_LINES $(git diff-index --cached HEAD --ignore-submodules=none | wc -l)"
} > "$out"
cat "$out" | grep -v '^GITLINK' | head -20
grep '^GITLINK' "$out"
