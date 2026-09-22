#!/usr/bin/env bash
# R235: prove a scratch extract still holds exactly the commit's blobs
# (every regular file hashed with `git hash-object`, compared with ls-tree).
# Usage: verify_extract.sh <review-checkout> <extract-dir> <rev>
set -euo pipefail
repo=${1:?}; dir=${2:?}; rev=${3:?}
bad=0; n=0
while read -r mode type blob path; do
  [ "$type" = blob ] || continue
  n=$((n+1))
  if [ "$mode" = 120000 ]; then
    [ "$(printf '%s' "$(readlink "$dir/$path")" | git -C "$repo" hash-object --stdin)" = "$blob" ] || { echo "SYMLINK MISMATCH $path"; bad=$((bad+1)); }
  else
    [ "$(git -C "$repo" hash-object --no-filters "$dir/$path")" = "$blob" ] || { echo "MISMATCH $path"; bad=$((bad+1)); }
  fi
done < <(git -C "$repo" ls-tree -r --full-tree "$rev" | tr '\t' ' ')
extra=$(cd "$dir" && find . -type f -not -path '*/__pycache__/*' | sed 's#^\./##' | sort | comm -23 - <(git -C "$repo" ls-tree -r --name-only --full-tree "$rev" | sort) | wc -l)
echo "$dir @ $rev: $n blobs checked, $bad mismatches, $extra extra non-bytecode files"
