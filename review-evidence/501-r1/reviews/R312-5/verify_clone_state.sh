#!/usr/bin/env bash
# Verify a review clone is byte-exact at the expected head: HEAD, tree,
# worktree and index versus HEAD (bytes and modes), untracked files, and
# the required submodule checkouts against their gitlinks.
# Usage: verify_clone_state.sh <clone> <expected-head-sha> <expected-tree>
set -u
cd "$1" || exit 2
head=$2; tree=$3; bad=0
[ "$(git rev-parse HEAD)" = "$head" ] && echo "HEAD $head OK" || { echo "HEAD MISMATCH"; bad=1; }
[ "$(git rev-parse HEAD^{tree})" = "$tree" ] && echo "tree $tree OK" || { echo "TREE MISMATCH"; bad=1; }
git update-index -q --really-refresh >/dev/null 2>&1
git diff --quiet HEAD -- && echo "worktree == HEAD (tracked bytes and modes)" || { echo "WORKTREE DIFFERS"; git diff --stat HEAD | tail -5; bad=1; }
git diff --cached --quiet HEAD -- && echo "index == HEAD" || { echo "INDEX DIFFERS"; bad=1; }
a=$(git ls-files -s | awk '{print $1, $2, $4}' | sha256sum | cut -d' ' -f1)
b=$(git ls-tree -r --full-tree HEAD | awk '{print $1, $3, $4}' | sha256sum | cut -d' ' -f1)
[ "$a" = "$b" ] && echo "index entries (mode, oid, path) == HEAD tree listing: $a" || { echo "INDEX LISTING DIFFERS"; bad=1; }
u=$(git ls-files --others --exclude-standard | wc -l)
[ "$u" = 0 ] && echo "no untracked files" || { echo "UNTRACKED: $u"; bad=1; }
for s in protocol-processor gptp-processor third_party/verilog-axis; do
  pin=$(git rev-parse "HEAD:$s"); got=$(git -C "$s" rev-parse HEAD)
  if [ "$pin" = "$got" ] && git -C "$s" diff --quiet HEAD -- && [ -z "$(git -C "$s" ls-files --others --exclude-standard)" ]; then
    echo "submodule $s at gitlink $pin, clean"
  else echo "SUBMODULE $s: pin $pin checkout $got (or dirty)"; bad=1; fi
done
exit $bad
