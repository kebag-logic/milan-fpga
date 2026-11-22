#!/bin/sh
# Verify a review clone is byte-exact at its head: HEAD/tree, index == HEAD tree (blob ids and modes),
# worktree == index (after a full refresh), no untracked files, and the submodule gitlinks.
# Usage: verify_clone.sh <clone> <expected-head> <expected-tree>
set -u
C=$1; H=$2; T=$3
cd "$C" || exit 2
echo "head  $(git rev-parse HEAD) (expected $H)"
echo "tree  $(git rev-parse HEAD^{tree}) (expected $T)"
[ "$(git rev-parse HEAD)" = "$H" ] && [ "$(git rev-parse HEAD^{tree})" = "$T" ] || { echo "FAIL head/tree"; exit 1; }
git ls-tree -r --full-tree HEAD | awk '{print $1, $3, $4}' | sort > /tmp/vc_tree.$$
git ls-files -s | awk '{print $1, $2, $4}' | sort > /tmp/vc_index.$$
if cmp -s /tmp/vc_tree.$$ /tmp/vc_index.$$; then echo "index == HEAD tree: $(wc -l < /tmp/vc_index.$$) entries (mode, blob, path)"; else echo "FAIL index differs from HEAD tree"; exit 1; fi
rm -f /tmp/vc_tree.$$ /tmp/vc_index.$$
git update-index -q --really-refresh >/dev/null 2>&1
if git diff-files --quiet --ignore-submodules=all; then echo "worktree == index (every tracked file's bytes and mode)"; else echo "FAIL worktree differs"; git diff-files --name-only | head; exit 1; fi
U=$(git ls-files --others --exclude-standard | wc -l); echo "untracked (not ignored): $U"
git ls-tree HEAD protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis external
git submodule status
