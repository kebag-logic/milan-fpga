#!/usr/bin/env bash
# Identity observation only (NOT candidate validation, which is manager-owned):
# live dev fetched into the base scratch clone at review time; does the
# manager's recorded current-dev candidate tree equal git merge-tree of the
# reviewed head with that dev tip, and are #513's paths disjoint from the
# issue delta? No gate is run here.
set -euo pipefail
SC=${SCRATCH:-/tmp/r222-478-r2-scratch}
G="$SC/base-sub"
HEAD_C=1496558d82cf35fc98dda0e781b2a1be643c301a
BASE_NOW=88e9276b2a220c716f64a843f7e1eb8f9265e896
# The reviewed head's objects come from the review clone's object store.
git -C "$G" fetch -q $VALIDATION_STORAGE/reviews/r222-478-r2 "$HEAD_C" 2>/dev/null || true
DEV=$(git -C "$G" rev-parse refs/remotes/live/dev)
echo "live dev (fetched $(date -Is)): $DEV"
echo "dev descends from the head's base $BASE_NOW: $(git -C "$G" merge-base --is-ancestor $BASE_NOW "$DEV" && echo yes || echo NO)"
echo "head already contains dev: $(git -C "$G" merge-base --is-ancestor "$DEV" $HEAD_C && echo yes || echo no)"
echo "paths changed on dev since the head's base ($BASE_NOW..$DEV):"
git -C "$G" diff --name-only $BASE_NOW "$DEV" | sed 's/^/  /'
echo "issue-delta paths ($BASE_NOW..$HEAD_C):"
git -C "$G" diff --name-only $BASE_NOW $HEAD_C | sed 's/^/  /'
common=$(comm -12 <(git -C "$G" diff --name-only $BASE_NOW "$DEV" | sort) <(git -C "$G" diff --name-only $BASE_NOW $HEAD_C | sort))
echo "overlapping paths: ${common:-none}"
mt=$(git -C "$G" merge-tree --write-tree $HEAD_C "$DEV")
echo "git merge-tree($HEAD_C, $DEV) = $mt"
echo "manager-recorded candidate tree 93be2b5788c4b79e88bfe22fbaf985686bbdc8f2 equal: $([ "$mt" = 93be2b5788c4b79e88bfe22fbaf985686bbdc8f2 ] && echo yes || echo NO)"
p() { git -C "$G" diff --full-index --no-renames "$1" "$2" -- docs/ENDSTATION_BUILDER.md sw/builder/endstation_builder.py sw/builder/test_builder.py | sha256sum | cut -d' ' -f1; }
echo "issue patch sha256 head vs base: $(p $BASE_NOW $HEAD_C); merge-tree vs dev: $(p "$DEV" "$mt")"
echo "gitlinks equal between dev and merge-tree: $([ "$(git -C "$G" ls-tree -r "$DEV" | awk '$1=="160000"')" = "$(git -C "$G" ls-tree -r "$mt" | awk '$1=="160000"')" ] && echo yes || echo NO)"
