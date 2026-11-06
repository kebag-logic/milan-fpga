#!/bin/sh
# Reproduce the round 12 merge and regeneration checks for PR #834.
# Usage: merge_regen_check.sh <clone containing 3e475161, 5843d1af, cc204c6f> <scratch dir>
set -u
C=$1; W=$2
HEAD=3e475161e528baa655a5ba84d6a38d78f8c64f3b; MERGE=3f4e39f35d19b416b7acb3a570273bfb1a327c0d
R11=5843d1af1d3a892fdc0fbb766ba2058ec44c26ea; DEV=cc204c6fd2349b543d73f15c97162a2c4434c86e; OLDBASE=1f29f189279f9fc0132f4918e47342b87d22f33a
cd "$C" || exit 2
echo "head tree: $(git rev-parse $HEAD^{tree})"
echo "merge-base --all head dev: $(git merge-base --all $HEAD $DEV | tr '\n' ' ')"
echo "auto-merge tree: $(git merge-tree --write-tree $R11 $DEV) rc=$?  committed merge tree: $(git rev-parse $MERGE^{tree})"
echo "combined-diff lines (0 = no hand-made hunk): $(git show --cc --format= $MERGE | wc -l)"
echo "patch-id r11: $(git diff $OLDBASE $R11 | git patch-id --stable | cut -d' ' -f1)"
echo "patch-id merged: $(git diff $DEV $MERGE | git patch-id --stable | cut -d' ' -f1)"
echo "regen commit files: $(git diff --name-only $MERGE $HEAD | tr '\n' ' ')"
rm -rf "$W/regen-probe"; git clone -q --no-checkout "$C" "$W/regen-probe" && cd "$W/regen-probe" && git checkout -q --detach $MERGE
python3 -I scripts/docs_inventory.py --check >/dev/null 2>&1; echo "check on merge commit rc=$? (1 expected: stale)"
python3 -I scripts/docs_inventory.py --write >/dev/null 2>&1; echo "write rc=$?"
echo "regenerated page blob $(git hash-object docs/DOCUMENTATION_AUDIT.md) vs head $(git rev-parse $HEAD:docs/DOCUMENTATION_AUDIT.md)"
echo "json blob $(git hash-object scripts/docs_inventory.json) vs head $(git rev-parse $HEAD:scripts/docs_inventory.json)"
echo "changed after write: $(git status --porcelain | tr '\n' ' ')"
