#!/usr/bin/env bash
# Reproduce the composition facts for the #582 merge-train candidate.
# Usage: composition_overlap.sh <clone>
set -u
cd "$1" || exit 2
src_base=9e9954e96bf55181edb9949ae94c9abd4ab6aaf5   # PR #596 source base
pr_head=aafcae59732c0a12333b73d82d5cdcbcbf90c47f    # PR #596 reviewed source head
parent=b468a56d9e3ed9c10e4e41503c446dd6b242b9f8     # train parent (C_600)
cand=1304205cfc9fa4c9e69a32130fb366895c5f883b       # candidate
echo "candidate parents: $(git log -1 --format=%P $cand)"
echo "merge-base(parent, pr_head): $(git merge-base $parent $pr_head)"
echo "recomputed merge tree: $(git merge-tree --write-tree $parent $pr_head)"
echo "candidate tree:        $(git rev-parse "$cand^{tree}")"
echo "patch-id source (base..pr_head): $(git diff $src_base $pr_head | git patch-id --stable | cut -d' ' -f1)"
echo "patch-id composed (parent..cand): $(git diff $parent $cand | git patch-id --stable | cut -d' ' -f1)"
git diff --name-only $src_base $pr_head | sort > /tmp/r355-3-pr-files.$$
git diff --name-only $src_base $parent | sort > /tmp/r355-3-train-files.$$
echo "PR files: $(wc -l < /tmp/r355-3-pr-files.$$); train files: $(wc -l < /tmp/r355-3-train-files.$$)"
echo "files changed by both the PR and a train predecessor:"
comm -12 /tmp/r355-3-pr-files.$$ /tmp/r355-3-train-files.$$ | while read -r f; do
    echo "  $f"
    git log --format='    train commit %h %s' $src_base..$parent -- "$f" | grep -v '^    train commit .* Validate issue'
    a=$(git diff $src_base $pr_head -- "$f" | grep '^[+-][^+-]' | sha256sum | cut -c1-16)
    b=$(git diff $parent $cand -- "$f" | grep '^[+-][^+-]' | sha256sum | cut -c1-16)
    echo "    PR changed lines $a; composed changed lines $b"
done
rm -f /tmp/r355-3-pr-files.$$ /tmp/r355-3-train-files.$$
echo "PR-file blob identity, candidate vs source head:"
git diff --name-only $src_base $pr_head | while read -r f; do
    [ "$(git rev-parse $pr_head:$f)" = "$(git rev-parse $cand:$f)" ] && s=SAME || s=DIFFERS
    echo "  $s $f"
done
echo "submodule gitlinks:"
for c in $src_base $pr_head $parent $cand; do
    echo "  ${c:0:10} $(git ls-tree $c gptp-processor protocol-processor third_party/verilog-axis | awk '{printf "%s=%s ", $4, substr($3,1,10)}')"
done
