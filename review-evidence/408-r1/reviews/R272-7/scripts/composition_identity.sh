#!/usr/bin/env bash
# Show that a merge-train candidate is exactly <dev> + <PR head>: the
# recomputed merge tree, the per-side patch-ids, the file overlap, and the
# live remote refs.  Usage: composition_identity.sh <clone> <candidate> <dev> <pr-head>
set -u
clone=$1 cand=$2 dev=$3 pr=$4
cd "$clone" || exit 2
mb=$(git merge-base "$dev" "$pr")
echo "candidate      $(git rev-parse "$cand") tree $(git rev-parse "$cand^{tree}")"
echo "parents        $(git rev-parse "$cand^1") $(git rev-parse "$cand^2")"
echo "merge-base     $mb"
echo "merge-tree     $(git merge-tree --write-tree "$dev" "$pr")   (clean recomputed merge of dev and PR head)"
echo "patch-id PR    mb..pr     $(git diff "$mb" "$pr" | git patch-id --stable | cut -d' ' -f1)"
echo "patch-id PR    dev..cand  $(git diff "$dev" "$cand" | git patch-id --stable | cut -d' ' -f1)"
echo "patch-id dev   mb..dev    $(git diff "$mb" "$dev" | git patch-id --stable | cut -d' ' -f1)"
echo "patch-id dev   pr..cand   $(git diff "$pr" "$cand" | git patch-id --stable | cut -d' ' -f1)"
echo "commits dev side: $(git rev-list --count "$mb..$dev")  PR side: $(git rev-list --count "$mb..$pr")"
echo "--- files changed by the PR (mb..pr)"
git diff --name-only "$mb" "$pr"
echo "--- of those, also changed on the dev side (mb..dev), with dev commits"
for f in $(git diff --name-only "$mb" "$pr"); do
    if git diff --quiet "$mb" "$dev" -- "$f"; then echo "  $f: dev side unchanged"
    else echo "  $f: ALSO CHANGED on dev by $(git log --format=%h "$mb..$dev" -- "$f" | paste -sd, -)"; fi
done
echo "--- hunks of the shared file on each side"
for f in $(git diff --name-only "$mb" "$pr"); do
    git diff --quiet "$mb" "$dev" -- "$f" && continue
    echo "  PR : $(git diff -U0 "$mb" "$pr" -- "$f" | grep '^@@' | paste -sd' ')"
    echo "  dev: $(git diff -U0 "$mb" "$dev" -- "$f" | grep '^@@' | paste -sd' ')"
done
echo "--- live remote refs"
git ls-remote https://github.com/kebag-logic/milan-fpga.git refs/heads/dev refs/pull/535/head
