#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# R304-3: prove the reviewed clone still holds exact head bytes, modes and index.
# usage: clone_integrity.sh CLONE EXPECTED_HEAD EXPECTED_TREE
set -u
C=$1 H=$2 T=$3
G="/usr/bin/git -C $C"
echo "head=$($G rev-parse HEAD) expect=$H"
echo "tree=$($G rev-parse HEAD^{tree}) expect=$T"
echo "detached=$($G symbolic-ref -q HEAD >/dev/null && echo no || echo yes)"
echo "status_porcelain_lines=$($G status --porcelain --ignored=no | wc -l)"
echo "untracked_or_ignored_lines=$($G status --porcelain --ignored | wc -l)"
$G diff-index --quiet --cached HEAD; echo "index_vs_head_rc=$?"
$G diff-files --quiet; echo "worktree_vs_index_rc=$?"
# every index entry (mode, blob) equals the head tree entry
a=$($G ls-files -s | awk '{print $1, $2, $4}' | sha256sum | cut -d' ' -f1)
b=$($G ls-tree -r HEAD | awk '{split($0,x,"\t"); split(x[1],y," "); print y[1], y[3], x[2]}' | sha256sum | cut -d' ' -f1)
echo "index_entries_sha=$a head_tree_entries_sha=$b match=$([ "$a" = "$b" ] && echo yes || echo no)"
# re-hash every tracked working file against the head blob and mode
bad=0 n=0
$G ls-tree -r HEAD | while IFS="$(printf '\t')" read -r meta path; do
  mode=$(echo "$meta" | cut -d' ' -f1) blob=$(echo "$meta" | cut -d' ' -f3)
  [ "$mode" = 160000 ] && { echo "gitlink $path $blob"; continue; }
  got=$($G hash-object "$C/$path")
  x=$([ -x "$C/$path" ] && echo 100755 || echo 100644)
  [ -L "$C/$path" ] && x=120000
  if [ "$got" != "$blob" ] || [ "$x" != "$mode" ]; then echo "MISMATCH $path"; fi
done > /tmp/r304-3-integrity.$$ 2>&1
echo "tracked_files=$($G ls-tree -r HEAD | wc -l) blob_or_mode_mismatches=$(grep -c MISMATCH /tmp/r304-3-integrity.$$)"
echo "gitlinks_at_head=$($G ls-tree -r HEAD | awk '$1=="160000"' | wc -l) .gitmodules_present=$($G cat-file -e HEAD:.gitmodules 2>/dev/null && echo yes || echo no)"
cat /tmp/r304-3-integrity.$$; rm -f /tmp/r304-3-integrity.$$
$G fsck --no-dangling --connectivity-only 2>&1 | tail -2; echo "fsck_rc=$?"
