#!/usr/bin/env bash
# Verify the review clone is exactly the head under review: HEAD, tree, index
# and working-tree bytes/modes, no untracked or ignored leftovers, gitlinks.
# Usage: verify-clone.sh <clone-dir> <expected-head> <expected-tree>
set -u
cd "$1"
echo "HEAD $(git rev-parse HEAD) expected $2"; echo "tree $(git rev-parse 'HEAD^{tree}') expected $3"
git update-index -q --really-refresh
echo "index vs HEAD (expect empty):"; git diff-index --cached --name-status HEAD --; echo "(end)"
echo "worktree vs index (expect empty):"; git diff-files --name-status; echo "(end)"
echo "untracked+ignored (expect empty):"; git status --porcelain --ignored --untracked-files=all; echo "(end)"
echo "index entries $(git ls-files -s | wc -l); HEAD tree entries $(git ls-tree -r HEAD | wc -l)"
echo "index stage/mode/blob == HEAD tree mode/blob: $([ "$(git ls-files -s | awk '{print $1, $2, $4}' | sort)" = "$(git ls-tree -r HEAD | awk '{print $1, $3, $4}' | sort)" ] && echo yes || echo NO)"
# re-hash every tracked file's bytes and compare to the recorded blob ids
bad=0; while IFS= read -r -d '' f; do
  exp=$(git rev-parse "HEAD:$f"); got=$(git hash-object --no-filters -- "$f"); [ "$exp" = "$got" ] || { echo "BYTES DIFFER: $f"; bad=1; }
done < <(git ls-files -z); echo "rehash of working-tree bytes: $([ $bad = 0 ] && echo all match || echo MISMATCH)"
echo "gitlinks (mode 160000) in HEAD: $(git ls-tree -r HEAD | awk '$1=="160000"' | wc -l); .gitmodules: $([ -f .gitmodules ] && echo present || echo absent)"
