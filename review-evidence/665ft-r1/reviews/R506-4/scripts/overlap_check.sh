#!/usr/bin/env bash
# Composition checks for the merge-train candidate: the merge reproduces the
# candidate tree, the shared files equal a three-way merge of both sides, and
# each side's added text survives once. Run from a clone holding all revisions.
# Usage: overlap_check.sh <base> <predecessor> <pr-head> <candidate>
set -u
base=$1; pre=$2; pr=$3; cand=$4
echo "merge-tree: $(git merge-tree --write-tree "$pre" "$pr")  candidate tree: $(git rev-parse "$cand^{tree}")"
shared=$(comm -12 <(git diff --name-only "$base" "$pr" | sort) <(git diff --name-only "$base" "$pre" | sort))
echo "shared files:"; echo "$shared"
for f in $shared; do
  d=$(mktemp -d)
  git show "$base:$f" > "$d/b"; git show "$pre:$f" > "$d/o"; git show "$pr:$f" > "$d/t"
  git show "$cand:$f" > "$d/c"
  git merge-file -p "$d/o" "$d/b" "$d/t" > "$d/m"; rc=$?
  cmp -s "$d/m" "$d/c" && echo "merge-file rc=$rc IDENTICAL $f" || echo "merge-file rc=$rc DIFFERS $f"
  # every line either side added must appear in the candidate at least as often
  python3 - "$d" "$f" <<'PY'
import collections, difflib, sys
d, f = sys.argv[1], sys.argv[2]
read = lambda n: open(f"{d}/{n}", encoding="utf-8").read().splitlines()
base, cand = read("b"), collections.Counter(read("c"))
for side in ("o", "t"):
    added = collections.Counter(l[2:] for l in difflib.ndiff(base, read(side)) if l.startswith("+ "))
    for line, n in added.items():
        if cand[line] < n:
            print(f"MISSING ({side}) {f}: {line!r}")
    print(f"added-line survival ({side}) {f}: {sum(added.values())} line(s) checked")
PY
  rm -r "$d"
done
echo "non-shared PR files differing between PR head and candidate: $(comm -23 <(git diff --name-only "$base" "$pr" | sort) <(echo "$shared" | sort) | while read -r f; do git diff --quiet "$pr" "$cand" -- "$f" || echo "$f"; done | wc -l)"
