#!/bin/sh
# Usage: merge_reconstruct.sh <repo> ; reproduces the PR #706 merge and classifies files.
set -eu
R=${1:?repo}
cd "$R"
B=c6bd08c6f52632c6d33d834ce842ac3cf63f29cc; L=26e2748f47b0d8fa533f53203264d9f31fc13c48; D=e81ce82f9aa3e4dcaffa5bcdf7e60f0c7cffd80c; M=313616d1a18549d41907db389d378f0beb9bc543
echo "git: $(git --version)"
echo "parents: $(git log -1 --format=%P $M)"
echo "merge-base(L,D): $(git merge-base $L $D)"
echo "recorded tree: $(git rev-parse $M^{tree})"
echo "merge-tree automatic result (first line tree, rest conflicts):"
git merge-tree --write-tree $L $D; echo "merge-tree rc=$?"
git diff --name-only $B $L | sort > /tmp/mr_L.$$; git diff --name-only $B $D | sort > /tmp/mr_D.$$
echo "files changed on lane side: $(wc -l < /tmp/mr_L.$$)"; echo "files changed on dev side: $(wc -l < /tmp/mr_D.$$)"
echo "files changed on both sides:"; comm -12 /tmp/mr_L.$$ /tmp/mr_D.$$
echo "files where merge differs from BOTH parents:"
for f in $(git diff --name-only $L $M); do git diff --quiet $D $M -- "$f" || echo "  $f"; done
echo "lane-side files: merge equals lane parent?"
for f in $(cat /tmp/mr_L.$$); do if git diff --quiet $L $M -- "$f"; then echo "  same  $f"; else echo "  DIFF  $f"; fi; done
echo "dev-side files: merge equals dev parent?"
for f in $(cat /tmp/mr_D.$$); do if git diff --quiet $D $M -- "$f"; then echo "  same  $f"; else echo "  DIFF  $f"; fi; done
echo "both-side files: lane hunk set (B..L) vs (D..M), and dev hunk set (B..D) vs (L..M), content lines only:"
for f in $(comm -12 /tmp/mr_L.$$ /tmp/mr_D.$$); do
  a=$(git diff -U0 $B $L -- "$f" | grep -E '^[+-][^+-]' | sha256sum | cut -c1-16)
  b=$(git diff -U0 $D $M -- "$f" | grep -E '^[+-][^+-]' | sha256sum | cut -c1-16)
  c=$(git diff -U0 $B $D -- "$f" | grep -E '^[+-][^+-]' | sha256sum | cut -c1-16)
  d=$(git diff -U0 $L $M -- "$f" | grep -E '^[+-][^+-]' | sha256sum | cut -c1-16)
  echo "  $f lane:$a merged-over-dev:$b dev:$c merged-over-lane:$d"
done
rm -f /tmp/mr_L.$$ /tmp/mr_D.$$
