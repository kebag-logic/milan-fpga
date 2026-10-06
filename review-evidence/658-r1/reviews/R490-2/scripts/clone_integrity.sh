#!/bin/sh
# R490-2: prove the review clone holds the exact head bytes after the probes.
# usage: clone_integrity.sh <clone> <expected-head> <expected-tree>
set -u
cd "$1" || exit 2
echo "HEAD $(git rev-parse HEAD) expected $2"
echo "tree $(git rev-parse HEAD^{tree}) expected $3"
echo "porcelain lines: $(git status --porcelain --untracked-files=all | wc -l)"
echo "ignored lines: $(git status --porcelain --ignored --untracked-files=all | grep -c '^!!')"
git diff --quiet && git diff --cached --quiet && echo "worktree and index equal HEAD: yes" || echo "worktree and index equal HEAD: NO"
# every tracked regular file re-hashed against its index blob and mode
bad=0; n=0
git ls-files -s | while read -r mode blob stage path; do
  [ "$mode" = 160000 ] && continue
  h=$(git hash-object -- "$path")
  if [ -L "$path" ]; then fm=120000; elif [ -x "$path" ]; then fm=100755; else fm=100644; fi
  if [ "$h" != "$blob" ] || [ "$fm" != "$mode" ]; then echo "MISMATCH $mode $blob $path ($fm $h)"; fi
done > /tmp/r490_2_integrity_mismatch.$$
echo "tracked non-gitlink entries: $(git ls-files -s | grep -vc '^160000')"
echo "blob/mode mismatches: $(wc -l < /tmp/r490_2_integrity_mismatch.$$)"
cat /tmp/r490_2_integrity_mismatch.$$; rm -f /tmp/r490_2_integrity_mismatch.$$
echo "index vs HEAD tree: $(git ls-files -s | awk '{print $1, $2, $4}' | sort | sha256sum | cut -c1-16) vs $(git ls-tree -r HEAD | awk '{print $1, $3, $4}' | sort | sha256sum | cut -c1-16)"
echo "gitlinks recorded in HEAD:"; git ls-tree -r HEAD | awk '$1=="160000"{print "  " $3, $4}'
echo "submodule checkouts:"; git submodule status | sed 's/^/  /'
