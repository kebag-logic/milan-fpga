#!/usr/bin/env bash
# For every path changed on either side since the merge base, report whether the
# candidate blob equals the PR-head blob, the dev blob, or neither (a true merge).
# Usage: blob_identity.sh <repo> <base> <dev> <pr> <candidate>
set -u; cd "$1" || exit 2; b=$2 d=$3 p=$4 c=$5
blob() { git rev-parse -q --verify "$1:$2" 2>/dev/null || echo absent; }
{ git diff --no-renames --name-only "$b" "$d"; git diff --no-renames --name-only "$b" "$p"; } | sort -u | while read -r f; do
  cb=$(blob "$c" "$f"); pb=$(blob "$p" "$f"); db=$(blob "$d" "$f")
  if [ "$cb" = "$pb" ] && [ "$cb" = "$db" ]; then s=both
  elif [ "$cb" = "$pb" ]; then s=PR-head
  elif [ "$cb" = "$db" ]; then s=dev
  else s=MERGED; fi
  printf '%-8s %s %s\n' "$s" "$cb" "$f"
done
echo "-- outside both change sets, candidate vs dev differences:"
git diff --no-renames --name-only "$d" "$c" | grep -vxF -f <(git diff --no-renames --name-only "$b" "$p") || echo none
