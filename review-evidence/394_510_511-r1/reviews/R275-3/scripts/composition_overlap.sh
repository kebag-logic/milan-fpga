#!/usr/bin/env bash
# Composition map for the merge-train candidate: which files this PR changes
# that a queued predecessor (or live dev since the PR's base) also changed,
# whether the merge is clean and conflict-free, and whether each PR hunk
# lands unchanged.
#   composition_overlap.sh <repo>
set -u
repo=$1
cd "$repo" || exit 2
H=8b7be584da62657f9767ad07e294d278144869c5   # candidate
B=70da0bcdf7896b26efb4cc3f854c17a02f2c4126   # candidate first parent
S=70f2c50d45550f65c9d71ed0f5b0d70dc48acdb6   # PR source head
MB=$(git merge-base "$B" "$S")
echo "candidate $H tree $(git rev-parse "$H^{tree}")"
echo "parents   $(git log -1 --format=%P "$H")"
echo "source    $S tree $(git rev-parse "$S^{tree}")"
echo "merge-base(parent, source) $MB"
echo "\$ git merge-tree --write-tree $B $S"; git merge-tree --write-tree "$B" "$S"; echo "exit=$?"
echo
echo "## first-parent history of the predecessor side, $MB..$B"
git log --first-parent --format='%h %s' "$MB..$B"
echo
echo "## files the PR changes ($MB..$S)"; git diff --name-only "$MB" "$S"
echo
echo "## files the predecessor side changes ($MB..$B)"; git diff --name-only "$MB" "$B"
echo
echo "## overlap"
comm -12 <(git diff --name-only "$MB" "$S" | sort) <(git diff --name-only "$MB" "$B" | sort)
echo
echo "## per-file patch identity: PR source diff vs candidate diff"
for f in $(git diff --name-only "$MB" "$S"); do
  a=$(git diff "$MB" "$S" -- "$f" | git patch-id --stable | cut -d' ' -f1)
  b=$(git diff "$B" "$H" -- "$f" | git patch-id --stable | cut -d' ' -f1)
  if [ "$a" = "$b" ]; then r=SAME; else r=DIFFER; fi
  echo "$r $f"
done
echo
echo "## the one DIFFER: patch text difference (context only)"
diff <(git diff "$MB" "$S" -- docs/reference/FR_NFR.md) <(git diff "$B" "$H" -- docs/reference/FR_NFR.md)
echo
echo "## predecessor edits on the overlap files"
git diff "$MB" "$B" -- $(comm -12 <(git diff --name-only "$MB" "$S" | sort) <(git diff --name-only "$MB" "$B" | sort))
echo
echo "## gitlinks: source, parent, candidate"
for r in "$S" "$B" "$H"; do echo "-- $r"; git ls-tree "$r" external gptp-processor protocol-processor third_party/verilog-axis; done
