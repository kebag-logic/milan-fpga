#!/bin/sh
# usage: checkout_integrity.sh <clone> <expected-head> <expected-tree>
# Read-only: every tracked blob's bytes and mode against the index and HEAD, no untracked/ignored file, the
# submodule gitlinks recorded at HEAD.
set -u
C=$1; H=$2; T=$3
cd "$C" || exit 2
echo "head $(git rev-parse HEAD) expected $H"
echo "tree $(git rev-parse HEAD^{tree}) expected $T"
[ "$(git rev-parse HEAD)" = "$H" ] && [ "$(git rev-parse HEAD^{tree})" = "$T" ] || { echo "HEAD MISMATCH"; exit 1; }
git diff --quiet HEAD -- && git diff --cached --quiet && echo "index and worktree equal HEAD (stat + content)"
echo "status --ignored entries: $(git status --porcelain --ignored | wc -l)"
bad=0; n=0
git ls-files -s | awk '$1 != "160000"' > /tmp/.ci_$$
while read -r mode oid stage path; do
  n=$((n+1))
  got=$(git hash-object --no-filters -- "$path")
  [ "$got" = "$oid" ] || { echo "BLOB DIFF $path"; bad=$((bad+1)); }
  if [ "$mode" = 100755 ]; then [ -x "$path" ] || { echo "MODE DIFF $path"; bad=$((bad+1)); }
  elif [ "$mode" = 100644 ]; then [ ! -x "$path" ] || { echo "MODE DIFF $path"; bad=$((bad+1)); }; fi
done < /tmp/.ci_$$
rm -f /tmp/.ci_$$
echo "tracked blobs checked: $n, differing: $bad"
echo "gitlinks at HEAD:"; git ls-tree -r HEAD | awk '$1 == "160000"'
echo "submodule checkouts:"; git submodule status
[ "$bad" = 0 ] && echo "INTEGRITY OK" || { echo "INTEGRITY FAILED"; exit 1; }
