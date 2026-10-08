#!/bin/sh
# Reproduce the manager candidate tree from public commits (no commits pushed).
# Usage: candidate_tree_check.sh <git-dir-with-objects>
set -e
cd "$1"
D=99e4eb6c14462aafa84bb1ac597fd241abc1a240      # live dev tip
H654=853a7357ba86d758a0e38f65db89a6187fb547bc   # PR #694 (#654) head
P=9c601b5983acfd60fb269b9a88c27b48cab7cf65      # PR #695 head under review
T1=$(git merge-tree --write-tree $D $H654 | head -1)
C1=$(GIT_AUTHOR_NAME=x GIT_AUTHOR_EMAIL=x@invalid GIT_COMMITTER_NAME=x GIT_COMMITTER_EMAIL=x@invalid \
     GIT_AUTHOR_DATE="1970-01-01T00:00:00Z" GIT_COMMITTER_DATE="1970-01-01T00:00:00Z" git commit-tree $T1 -p $D -p $H654 -m synth)
T2=$(git merge-tree --write-tree $C1 $P | head -1)
echo "dev+654 tree $T1"
echo "candidate tree $T2"
echo "claimed tree 140c3b838ef3a1f72e2669744871a48b83911311"
[ "$T2" = 140c3b838ef3a1f72e2669744871a48b83911311 ] && echo MATCH || { echo MISMATCH; exit 1; }
