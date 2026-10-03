#!/usr/bin/env bash
# Verify the review clone is byte-exact at the published head after every probe: HEAD, tree, index,
# tracked blob bytes and modes, nothing untracked or ignored, and the submodule gitlinks.
# Usage: verify_tree.sh <repo checkout> <expected head> <expected tree>
set -u
repo=$1 head=$2 tree=$3
cd "$repo" || exit 2
fail=0
[ "$(git rev-parse HEAD)" = "$head" ] && echo "HEAD $head OK" || { echo "HEAD MISMATCH"; fail=1; }
[ "$(git rev-parse HEAD^{tree})" = "$tree" ] && echo "tree $tree OK" || { echo "tree MISMATCH"; fail=1; }
[ "$(git write-tree)" = "$tree" ] && echo "index tree OK" || { echo "index tree MISMATCH"; fail=1; }
git update-index -q --really-refresh
if git diff --quiet && git diff --cached --quiet; then echo "worktree and index equal HEAD (bytes and modes)"; else echo "DIFF present"; git status --short; fail=1; fi
diff <(git ls-files -s | awk '{print $1, $2, $4}') <(git ls-tree -r HEAD | awk '{print $1, $3, $4}') > /dev/null \
  && echo "ls-files -s equals ls-tree -r HEAD (mode, blob, path)" || { echo "INDEX vs TREE MISMATCH"; fail=1; }
untracked=$(git status --porcelain --ignored --untracked-files=all | wc -l)
[ "$untracked" = 0 ] && echo "no untracked or ignored file" || { echo "untracked/ignored: $untracked"; git status --porcelain --ignored | head; fail=1; }
git ls-tree HEAD | awk '$2=="commit"{print $3, $4}' | while read -r sha path; do
  echo "gitlink $path $sha"
done
git submodule status 2>&1 | sed 's/^/submodule: /'
echo "verify_tree: $([ $fail = 0 ] && echo PASS || echo FAIL)"
exit $fail
