#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Identity of the reviewed clone and of the pinned simulator. Read-only.
set -u
. "$(dirname "$0")/env.sh"
cd "$CLONE" || exit 2
echo "== clone"
echo "HEAD $(git rev-parse HEAD)"
echo "tree $(git rev-parse 'HEAD^{tree}')"
echo "expect HEAD $HEAD_SHA tree $HEAD_TREE"
[ "$(git rev-parse HEAD)" = "$HEAD_SHA" ] && [ "$(git rev-parse 'HEAD^{tree}')" = "$HEAD_TREE" ] \
  && echo "identity: MATCH" || { echo "identity: MISMATCH"; exit 1; }
echo "status-porcelain-lines $(git status --porcelain --ignored=no | wc -l)"
echo "index-vs-HEAD diff lines $(git diff --cached --name-only | wc -l)"
echo "worktree-vs-index diff lines $(git diff --name-only | wc -l)"
echo "ls-files -s sha256 $(git ls-files -s | sha256sum | cut -d' ' -f1)"
echo "ls-tree -r HEAD sha256 $(git ls-tree -r HEAD | sha256sum | cut -d' ' -f1)"
echo "gitlinks (mode 160000): $(git ls-files -s | awk '$1==160000' | wc -l)"
echo "assume-unchanged/skip-worktree flags: $(git ls-files -v | grep -c '^[a-zS]' || true)"
# every tracked blob on disk hashes to the id HEAD records
bad=0
git ls-tree -r HEAD | while read -r mode type oid path; do
  [ "$type" = blob ] || continue
  got=$(git hash-object --no-filters -- "$path")
  [ "$got" = "$oid" ] || { echo "BLOB MISMATCH $path"; }
  m=$(stat -c %a -- "$path")
  case "$mode" in 100755) [ "$m" = 755 ] || echo "MODE MISMATCH $path $m";; 100644) [ "$m" = 644 ] || echo "MODE MISMATCH $path $m";; esac
done > "${TMPDIR:-/tmp}/r259-3-blobcheck.$$"
if [ -s "${TMPDIR:-/tmp}/r259-3-blobcheck.$$" ]; then cat "${TMPDIR:-/tmp}/r259-3-blobcheck.$$"; bad=1; fi
rm -f "${TMPDIR:-/tmp}/r259-3-blobcheck.$$"
echo "tracked blobs byte/mode check: $([ $bad = 0 ] && echo MATCH || echo MISMATCH)"
echo "commits base..head:"
git log --format='  %H %s' "$BASE_SHA..$HEAD_SHA"
echo "== pinned simulator"
echo "wrapper $PINNED_VERILATOR"
sha256sum "$PINNED_VERILATOR"
bin=$(sed -n 's/.* \(\/[^ ]*\/usr\/bin\/verilator\) .*/\1/p' "$PINNED_VERILATOR")
echo "script $bin"
sha256sum "$bin" "${bin}_bin"
"$PINNED_VERILATOR" --version
echo "system verilator (not used): $(verilator --version 2>/dev/null)"
echo "python3 $(python3 --version 2>&1)"
exit $bad
