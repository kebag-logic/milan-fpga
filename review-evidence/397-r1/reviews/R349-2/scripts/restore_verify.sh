#!/bin/sh
# Verify the review clone is at the exact head with pristine tracked bytes, modes, index and gitlinks.
# Usage: restore_verify.sh <repo> <expected-head> <expected-tree>
R=$1; H=$2; T=$3; cd $R || exit 2
echo "HEAD=$(git rev-parse HEAD) expected=$H"
echo "HEAD^{tree}=$(git rev-parse 'HEAD^{tree}') expected=$T"
echo "index tree=$(git write-tree)"
echo "diff-index (index+worktree vs HEAD, content and mode):"; git diff-index --stat HEAD --; echo "(end)"
git update-index --really-refresh > /dev/null 2>&1; echo "update-index --really-refresh rc=$?"
echo "status --porcelain --ignored:"; git status --porcelain --ignored; echo "(end)"
echo "gitlinks at HEAD:"; git ls-tree HEAD | awk '$2=="commit"'
echo "submodule checkouts:"; git submodule status
for s in gptp-processor protocol-processor; do echo "$s porcelain+ignored:"; git -C $s status --porcelain --ignored; echo "(end)"; done
echo "protected paths vs round-1 head 7f997b60 and base ac18b509:"
git diff --stat 7f997b60d5a74d46beca5c263d27496ccce0ae4f HEAD -- sw/firmware/milan_baremetal tb/verilator/nvm_capture_cpu; echo "(end)"
git diff --stat ac18b50968b12efe4d15c0a06301264b35656b31 HEAD -- sw/firmware/milan_baremetal tb/verilator/nvm_capture_cpu external gptp-processor protocol-processor third_party; echo "(end)"
sha256sum sw/firmware/milan_baremetal/milan_baremetal.c
