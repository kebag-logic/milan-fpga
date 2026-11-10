#!/bin/sh
# Read-only integrity check of a checkout against its HEAD commit.
# Usage: verify_integrity.sh <checkout>...
# Prints HEAD and tree, whether the worktree and index equal HEAD, index flag
# anomalies (assume-unchanged / skip-worktree), an index-vs-tree comparison of
# mode, blob id and path for every non-gitlink entry, the reviewed files'
# on-disk blob ids, and the gitlinks recorded in the index and in the tree.
set -u
for d in "$@"; do
  echo "== $d"
  git -C "$d" rev-parse HEAD 'HEAD^{tree}'
  echo "status entries: $(git -C "$d" status --porcelain --ignore-submodules=none | wc -l)"
  if git -C "$d" diff --quiet HEAD; then echo "worktree==HEAD: yes"; else echo "worktree==HEAD: NO"; fi
  if git -C "$d" diff --cached --quiet; then echo "index==HEAD: yes"; else echo "index==HEAD: NO"; fi
  echo "ls-files -v entries not flagged H: $(git -C "$d" ls-files -v | grep -vc '^H ')"
  git -C "$d" ls-files -s | awk '$1!="160000"{print $1, $2, $4}' > /tmp/.r817-index.$$
  git -C "$d" ls-tree -r HEAD | awk '$2!="commit"{print $1, $3, $4}' > /tmp/.r817-tree.$$
  echo "index vs tree differing lines: $(diff /tmp/.r817-index.$$ /tmp/.r817-tree.$$ | wc -l)"
  rm -f /tmp/.r817-index.$$ /tmp/.r817-tree.$$
  for f in scripts/act_ci.py docs/testing/CI_WORKFLOWS.md; do
    echo "$f: HEAD blob $(git -C "$d" rev-parse "HEAD:$f") disk $(cd "$d" && git hash-object "$f") mode $(stat -c %a "$d/$f")"
  done
  echo "gitlinks (index):"; git -C "$d" ls-files -s | awk '$1=="160000"{print "  " $2, $4}'
  echo "gitlinks (tree):"; git -C "$d" ls-tree -r HEAD | awk '$2=="commit"{print "  " $3, $4}'
  echo "submodule status:"; git -C "$d" submodule status
done
