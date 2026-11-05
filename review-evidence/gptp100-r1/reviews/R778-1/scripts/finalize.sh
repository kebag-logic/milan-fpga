#!/bin/bash
# usage: finalize.sh <packet dir> <review clone>
# 1. Replace host paths in publishable receipts with placeholders.
# 2. Verify the review clone is byte-exact at the reviewed head.
# 3. Write MANIFEST.sha256 over receipts/ and scripts/ (REPORT.md excluded).
set -u
P=$1; C=$2
find "$P/receipts" -type f -print0 | xargs -0 sed -i \
  -e "s#$P#<packet>#g" -e "s#$C#<review-clone>#g" \
  -e 's#/home/[a-z]*/\.local/share/containers/storage/overlay/[0-9a-f]*/diff#<toolchain>#g' \
  -e 's#$VALIDATION_TOOLS#<tools>#g' -e 's#/home/[a-z]*#<home>#g' -e 's#/tmp/#<tmp>/#g'
{
  cd "$C" || exit 1
  echo "HEAD $(git rev-parse HEAD)"
  echo "tree $(git rev-parse 'HEAD^{tree}')"
  echo "status-porcelain-lines $(git status --porcelain --untracked-files=all | wc -l)"
  echo "diff-index-vs-HEAD $(git diff-index --cached HEAD | wc -l)"
  echo "worktree-vs-index $(git diff-files | wc -l)"
  echo "index-entries-equal-HEAD-entries (mode blob path) $( [ "$(git ls-files -s | awk '{print $1, $2, $4}')" = "$(git ls-tree -r HEAD | awk '{print $1, $3, $4}')" ] && echo yes || echo NO)"
  echo "worktree-blobs-rehashed-equal $(git ls-files -z | xargs -0 git hash-object -- | paste -d" " - <(git ls-files -s | awk '{print $2}') | awk '$1!=$2' | wc -l) mismatches"
  echo "index-matches-HEAD-tree $( [ "$(git write-tree)" = "$(git rev-parse 'HEAD^{tree}')" ] && echo yes || echo NO)"
  echo "gitlinks-in-HEAD $(git ls-tree -r HEAD | awk '$1=="160000"' | wc -l)"
  echo "submodule-status-lines $(git submodule status 2>/dev/null | wc -l)"
} > "$P/receipts/exact-head-check.txt"
cd "$P" && find receipts scripts -type f | sort | xargs sha256sum > MANIFEST.sha256
