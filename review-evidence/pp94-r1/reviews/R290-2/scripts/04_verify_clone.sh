#!/usr/bin/env bash
# Verify the review clone still holds exact head bytes, modes and index; list gitlinks.
# Usage: CLONE=<clone> bash 04_verify_clone.sh
set -u
C=${CLONE:?}
echo "HEAD $(git -C "$C" rev-parse HEAD)"
echo "tree $(git -C "$C" rev-parse 'HEAD^{tree}')"
echo "index-tree $(git -C "$C" write-tree)"
echo "status-porcelain-lines $(git -C "$C" status --porcelain --ignored | wc -l)"
git -C "$C" status --porcelain --ignored | head
git -C "$C" diff --quiet HEAD && echo "worktree==HEAD: yes" || echo "worktree==HEAD: NO"
echo "gitlinks (mode 160000): $(git -C "$C" ls-files -s | awk '$1=="160000"' | wc -l)"
test -e "$C/.gitmodules" && echo ".gitmodules present" || echo ".gitmodules absent"
# re-hash every tracked file from disk and compare with the index blob id and mode
bad=0
while read -r mode blob stage path; do
  [ "$mode" = 160000 ] && continue
  h=$(git -C "$C" hash-object -- "$path")
  m=$([ -x "$C/$path" ] && echo 100755 || echo 100644)
  [ -L "$C/$path" ] && m=120000
  if [ "$h" != "$blob" ] || [ "$m" != "$mode" ]; then echo "MISMATCH $path"; bad=1; fi
done < <(git -C "$C" ls-files -s)
echo "tracked blob/mode mismatches: $bad"
