#!/bin/bash
# Verify the reviewer clone equals the exact head: index tree, worktree blob bytes and modes, gitlinks, cleanliness.
cd "$1" || exit 2
echo "HEAD $(git rev-parse HEAD 2>/dev/null)"
echo "index tree $(git write-tree 2>/dev/null)  head tree $(git rev-parse HEAD^{tree} 2>/dev/null)"
git diff --quiet 2>/dev/null && echo "worktree vs index: clean" || echo "worktree vs index: DIRTY"
git diff --cached --quiet 2>/dev/null && echo "index vs HEAD: clean" || echo "index vs HEAD: DIRTY"
n=0; bad=0; badmode=0
while read -r mode sha stage path; do
  [ "$mode" = 160000 ] && continue
  n=$((n+1))
  if [ "$mode" = 120000 ]; then h=$(readlink -n "$path" | git hash-object --stdin); else h=$(git hash-object "$path"); fi
  [ "$h" = "$sha" ] || { bad=$((bad+1)); echo "BLOB MISMATCH $path"; }
  if [ "$mode" = 100755 ]; then [ -x "$path" ] || { badmode=$((badmode+1)); echo "MODE $path"; }
  elif [ "$mode" = 100644 ]; then [ -x "$path" ] && { badmode=$((badmode+1)); echo "MODE $path"; }; fi
done < <(git ls-files -s 2>/dev/null)
echo "tracked non-gitlink blobs: $n  byte mismatches: $bad  mode mismatches: $badmode"
git ls-files -s 2>/dev/null | awk '$1==160000{print "gitlink", $4, $2}'
git submodule status 2>/dev/null
for s in protocol-processor gptp-processor third_party/verilog-axis; do echo "submodule $s porcelain lines: $(git -C $s status --porcelain 2>/dev/null | wc -l)"; done
echo "untracked+ignored entries: $(git status --porcelain --ignored 2>/dev/null | wc -l)"
git status --porcelain --ignored 2>/dev/null | head
