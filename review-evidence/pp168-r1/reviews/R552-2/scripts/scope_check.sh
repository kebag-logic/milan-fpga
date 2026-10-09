#!/usr/bin/env bash
# Scope of the round-3 delta and integrity of the reviewed clone.
# usage: scope_check.sh REPO BASE_REV HEAD_REV EXPECTED_TREE
set -uo pipefail
repo=$1; base=$2; head=$3; tree=$4
cd "$repo"
echo "HEAD $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}')"
test "$(git rev-parse HEAD)" = "$(git rev-parse "$head")" && echo "PASS head is exact" || echo "FAIL head"
test "$(git rev-parse 'HEAD^{tree}')" = "$tree" && echo "PASS tree is exact" || echo "FAIL tree"
echo "parents of head: $(git rev-list --parents -n1 "$head")"
echo "--- files changed $base..$head"
git diff --name-status "$base" "$head"
n=$(git diff --name-only "$base" "$head" -- hdl tb scripts syn Makefile .github | wc -l)
test "$n" -eq 0 && echo "PASS no hdl/ tb/ scripts/ syn/ Makefile .github change ($n)" || echo "FAIL $n non-doc paths changed"
m=$(git diff --name-only "$base" "$head" | grep -v '^docs/' | wc -l)
test "$m" -eq 0 && echo "PASS only docs/ changed" || echo "FAIL $m paths outside docs/"
echo "--- worktree/index integrity"
git status --porcelain=v2 --untracked-files=all --ignored=no | sed 's/^/status: /'
test -z "$(git status --porcelain --untracked-files=all)" && echo "PASS worktree clean" || echo "FAIL worktree dirty"
git diff-index --quiet --cached HEAD && echo "PASS index equals HEAD" || echo "FAIL index differs"
git ls-files -s | awk '{print $1, $2, $4}' | sha256sum | sed 's/^/index modes+blobs+paths sha256: /'
git ls-tree -r "$head" | awk '{print $1, $3, $4}' | sha256sum | sed 's/^/head tree modes+blobs+paths sha256: /'
bad=$(git ls-files -s | while read -r mode blob _ path; do
  [ "$mode" = 160000 ] && continue
  [ -L "$path" ] && h=$(readlink "$path" | git hash-object --stdin) || h=$(git hash-object --no-filters "$path")
  [ "$h" = "$blob" ] || echo "$path"
  if [ "$mode" = 100755 ] && [ ! -x "$path" ]; then echo "mode:$path"; fi
  if [ "$mode" = 100644 ] && [ -x "$path" ]; then echo "mode:$path"; fi
done | wc -l)
test "$bad" -eq 0 && echo "PASS every tracked file's bytes and mode match its index blob" || echo "FAIL $bad tracked files differ"
g=$(git ls-files -s | awk '$1==160000' | wc -l)
echo "gitlinks (submodules) in index: $g; .gitmodules present: $(test -f .gitmodules && echo yes || echo no)"
