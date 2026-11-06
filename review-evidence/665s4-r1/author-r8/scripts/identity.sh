#!/bin/bash
# identity.sh <clone> <base>: the head's identity, on a clean clone of it: refs, merge base, what the delta touches,
# commit bodies, git diff --check and the privacy check. Exit 0 only when both checks are rc 0.
C=$1; B=$2; PREV=37e0393094e62d395edc2798a6a6da2f34badbec
L=$LANES/665-s4-f1-target
cd "$C" || exit 2
echo "head $(git rev-parse HEAD)"
echo "tree $(git rev-parse 'HEAD^{tree}')"
echo "lane branch $(git -C $L branch --show-current) at $(git -C $L rev-parse HEAD)"
echo "origin $(git remote get-url origin)"
git ls-remote https://github.com/kebag-logic/milan-fpga.git refs/heads/665-s4-f1-target refs/heads/dev-soft-core | sed 's/^\(.*\)\t\(.*\)$/live \2 \1/'
echo "merge-base against $B: $(git merge-base HEAD "$B")"
git merge-base --is-ancestor $PREV HEAD && echo "ancestor of head: ${PREV:0:8} yes"
git merge-base --is-ancestor f4c9ad4f HEAD && echo "ancestor of head: f4c9ad4f yes"
git diff --check "$B" HEAD; dc=$?; echo "git diff --check $B rc=$dc"
git diff --check $PREV HEAD; dp=$?; echo "git diff --check ${PREV:0:8} rc=$dp"
echo "status lines: $(git status --porcelain --untracked-files=all --ignore-submodules=none | wc -l)"
echo "hdl files changed since $B: $(git diff --name-only "$B" HEAD -- hdl | wc -l)"
echo "sv/v/c/h files changed since ${PREV:0:8}: $(git diff --name-only $PREV HEAD -- '*.sv' '*.v' '*.c' '*.h' | wc -l)"
echo "gitlinks changed since ${PREV:0:8}: $(git diff --raw $PREV HEAD | grep -c ' 160000 ')"
echo "files changed since ${PREV:0:8}:"; git diff --stat $PREV HEAD | sed 's/^/  /'
echo "commits on ${PREV:0:8}:"; git log --format='  %h %s' $PREV..HEAD
echo "commit bodies and trailers: $(git log --format='%b' $PREV..HEAD | grep -c .) lines"
python3 -I $MANAGEMENT/2026-09-23/push-privacy-check.py "$C" "$B"; pv=$?; echo "privacy rc=$pv"
[ "$dc" = 0 ] && [ "$dp" = 0 ] && [ "$pv" = 0 ]
