#!/usr/bin/env bash
# R226-2 integrity snapshot of the isolated review clone (read-only; no index refresh).
set -euo pipefail
repo=${1:?repo}
export GIT_OPTIONAL_LOCKS=0 GIT_NO_REPLACE_OBJECTS=1
cd "$repo"
echo "date: $(date -Is)"
echo "repo: $repo"
echo "HEAD: $(git rev-parse HEAD)"
echo "HEAD^{tree}: $(git rev-parse 'HEAD^{tree}')"
echo "symbolic-ref: $(git symbolic-ref -q HEAD || echo '(detached)')"
echo "index-file-sha256: $(sha256sum .git/index | cut -d' ' -f1)"
echo "ls-files-s-sha256: $(git ls-files -s | sha256sum | cut -d' ' -f1)"
echo "ls-files-s-count: $(git ls-files -s | wc -l)"
echo "ls-tree-HEAD-sha256: $(git ls-tree -r --full-tree HEAD | sha256sum | cut -d' ' -f1)"
# index entries must equal HEAD tree entries (mode, blob, path)
diff <(git ls-files -s | awk '{print $1, $2, $4}') \
     <(git ls-tree -r --full-tree HEAD | awk '{print $1, $3, $4}') >/dev/null \
  && echo "index-equals-HEAD-tree: yes" || echo "index-equals-HEAD-tree: NO"
# worktree bytes of every tracked regular file hashed as git blobs
tracked_worktree=$(git ls-files -s | awk '$1!="160000"{print $4}' | git hash-object --stdin-paths | sha256sum | cut -d' ' -f1)
tracked_index=$(git ls-files -s | awk '$1!="160000"{print $2}' | sha256sum | cut -d' ' -f1)
echo "worktree-blob-list-sha256: $tracked_worktree"
echo "index-blob-list-sha256:    $tracked_index"
[ "$tracked_worktree" = "$tracked_index" ] && echo "worktree-bytes-equal-index: yes" || echo "worktree-bytes-equal-index: NO"
echo "modes-on-disk-vs-index:"
git ls-files -s | awk '$1=="100755"{print $4}' | while read -r p; do [ -x "$p" ] || echo "  not-exec: $p"; done
git ls-files -s | awk '$1=="100644"{print $4}' | while read -r p; do [ -x "$p" ] && echo "  exec: $p"; done || true
git ls-files -s | awk '$1=="120000"{print $4}' | while read -r p; do [ -L "$p" ] || echo "  not-link: $p"; done
echo "  (end)"
echo "status --porcelain=v2 --ignored --untracked-files=all:"
git status --porcelain=v2 --branch --ignored --untracked-files=all | sed 's/^/  /'
echo "diff-quiet: $(git diff --quiet && echo clean || echo DIRTY)"
echo "diff-cached-quiet: $(git diff --cached --quiet && echo clean || echo DIRTY)"
echo "stash: $(git stash list | wc -l)"
echo "refs:"
git for-each-ref --format='  %(objectname) %(refname)'
echo "submodule status:"
git submodule status 2>&1 | sed 's/^/  /'
echo "ls-files -v flags (non-H):"
git ls-files -v | awk '$1!="H"' | sed 's/^/  /' | head -20
echo "  (end)"
echo "alternates: $(cat .git/objects/info/alternates 2>/dev/null || echo none)"
