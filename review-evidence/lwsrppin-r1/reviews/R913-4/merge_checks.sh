#!/bin/sh
# Reproduce and check a two-parent sync merge from a clone that holds both parents and the merge base.
# Usage: sh merge_checks.sh <clone> [merge-commit]   (default HEAD). Prints a receipt; exit 1 on any failed check.
set -u
C=$1; M=${2:-HEAD}
cd "$C" || exit 2
P1=$(git rev-parse "$M^1"); P2=$(git rev-parse "$M^2"); B=$(git merge-base "$P1" "$P2")
echo "merge $(git rev-parse "$M") tree $(git rev-parse "$M^{tree}")"
echo "first parent $P1; second parent $P2; merge base $B"
echo "message: $(git log -1 --format=%B "$M" | sed '/^$/d' | wc -l) non-empty line(s): $(git log -1 --format=%s "$M")"
t=$(mktemp -d); bad=0
git diff --name-only "$B" "$P1" | sort > "$t/p1"; git diff --name-only "$B" "$P2" | sort > "$t/p2"
git diff --name-only "$B" "$M" | sort > "$t/m"; sort -u "$t/p1" "$t/p2" > "$t/u"
echo "paths: first $(wc -l < "$t/p1"), second $(wc -l < "$t/p2"), both $(comm -12 "$t/p1" "$t/p2" | wc -l)"
for f in $(comm -23 "$t/p1" "$t/p2"); do
  [ "$(git rev-parse "$M:$f" 2>/dev/null)" = "$(git rev-parse "$P1:$f" 2>/dev/null)" ] || { echo "FIRST-ONLY PATH DIFFERS $f"; bad=1; }
done
for f in $(comm -13 "$t/p1" "$t/p2"); do
  [ "$(git rev-parse "$M:$f" 2>/dev/null)" = "$(git rev-parse "$P2:$f" 2>/dev/null)" ] || { echo "SECOND-ONLY PATH DIFFERS $f"; bad=1; }
done
echo "one-sided paths equal to their own side: $([ $bad = 0 ] && echo yes || echo NO)"
x=$(comm -23 "$t/m" "$t/u"); echo "paths changed by the merge that neither side changed: ${x:-none}"; [ -z "$x" ] || bad=1
mt=$(git merge-tree --write-tree --name-only "$P1" "$P2" | head -1)
echo "git merge-tree (git $(git --version | cut -d' ' -f3)) tree with conflict markers: $mt"
for f in $(comm -12 "$t/p1" "$t/p2"); do
  if [ "$(git rev-parse "$mt:$f")" = "$(git rev-parse "$M:$f")" ]; then echo "both-changed $f: identical to git's automatic merge"
  else echo "both-changed $f: HAND-RESOLVED (diff from the conflicted merge below)"; fi
done
echo "--- resolution of every conflicted path (merge-tree's conflicted text -> merge)"
git diff "$mt" "$M"
echo "--- gitlinks: merge vs first parent, then merge vs second parent"
git ls-tree -r "$M" | awk '$1=="160000"' > "$t/gm"
git ls-tree -r "$P1" | awk '$1=="160000"' | diff - "$t/gm" && echo "gitlinks == first parent"
git ls-tree -r "$P2" | awk '$1=="160000"' | diff - "$t/gm"
rm -rf "$t"
echo "RESULT: $([ $bad = 0 ] && echo PASS || echo FAIL)"
exit $bad
