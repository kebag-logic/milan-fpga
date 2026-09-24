#!/usr/bin/env bash
# Verify the review clone is at the exact head with untouched tracked bytes, modes, index and gitlinks.
set -u
cd "$1"
echo "HEAD $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}') write-tree $(git write-tree)"
echo "index sha256 $(git ls-files -s | sha256sum | cut -d' ' -f1)"
echo "porcelain (incl. ignored) lines: $(git status --porcelain --ignored | wc -l)"
git diff --quiet && git diff --cached --quiet && echo "worktree and index match HEAD"
echo "index entries not plain-tracked (assume-unchanged/skip-worktree): $(git ls-files -v | grep -vc '^H')"
git ls-files -s | awk '$1!="160000"{print $1" "$2" "$4}' > /tmp/vcs_ls.$$
awk '{print $3}' /tmp/vcs_ls.$$ | git hash-object --stdin-paths > /tmp/vcs_disk.$$
paste -d' ' /tmp/vcs_ls.$$ /tmp/vcs_disk.$$ | awk '$2!=$4{b++} END{print "tracked files", NR, "blob mismatches", b+0}'
while read -r m _ p; do
  case "$m" in 100755) [ -x "$p" ] || echo "MODE $p";; 100644) [ -x "$p" ] && echo "MODE-X $p";; esac
done < /tmp/vcs_ls.$$
echo "mode check done"
rm -f /tmp/vcs_ls.$$ /tmp/vcs_disk.$$
git ls-tree HEAD external gptp-processor protocol-processor third_party/verilog-axis
git submodule status
for s in gptp-processor protocol-processor; do echo "$s dirty lines: $(git -C "$s" status --porcelain | wc -l)"; done
