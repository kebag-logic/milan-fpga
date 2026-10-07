#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Verify the reviewer clone is exactly the reviewed head with clean tracked bytes and index.
# Usage: verify_clone.sh <checkout>
set -u
cd "$1" || exit 2
HEAD=f800a2bb920c543934d6286a47fe20dde3efa2c5; TREE=f950b4f333aeb8b2cb267c7c2040645ff6f8050c
rc=0
h=$(git rev-parse HEAD); t=$(git rev-parse 'HEAD^{tree}'); w=$(git write-tree)
echo "HEAD $h"; echo "HEAD tree $t"; echo "index tree $w"
[ "$h" = "$HEAD" ] && [ "$t" = "$TREE" ] && [ "$w" = "$TREE" ] || rc=1
git update-index -q --really-refresh >/dev/null
if git diff --quiet HEAD -- && git diff --cached --quiet; then echo "tracked bytes/modes: clean"; else echo "tracked bytes/modes: DIRTY"; rc=1; fi
echo "untracked: $(git ls-files --others --exclude-standard | wc -l); ignored: $(git ls-files --others --ignored --exclude-standard | wc -l)"
echo "gitlinks (mode 160000): $(git ls-files -s | awk '$1==160000' | wc -l)"
echo "LICENSE blob $(git hash-object LICENSE) $(sha256sum LICENSE | cut -d' ' -f1)"
echo "result rc=$rc"
exit $rc
