#!/usr/bin/env bash
# p9 (R220-3): tracked/index/mode integrity of the review clone.
# Usage: p9_integrity.sh <clone> <expected-head>
set -uo pipefail
cd "$1" || exit 2
want=$2
echo "# integrity $(date -u +%FT%TZ)"
echo "HEAD $(git rev-parse HEAD) (expected $want)"
echo "tree $(git rev-parse HEAD^{tree})"
[ "$(git rev-parse HEAD)" = "$want" ] && echo "head-ok" || echo "HEAD-MISMATCH"
echo "status-porcelain-v2 (untracked, ignored):"
git status --porcelain=v2 --untracked-files=all --ignored
echo "end-status"
echo "ls-files -s sha256: $(git ls-files -s | sha256sum | cut -d' ' -f1)"
echo "index-vs-HEAD (diff-index --cached): $(git diff-index --cached HEAD | wc -l) entries"
echo "worktree-vs-index (diff-files): $(git diff-files | wc -l) entries"
echo "flags other than H: $(git ls-files -v | grep -vc '^H ')"
echo "core.filemode=$(git config --get core.filemode)"
bad=0; n=0
while IFS=$'\t' read -r meta path; do
  mode=${meta%% *}; rest=${meta#* }; blob=${rest%% *}
  [ "$mode" = 160000 ] && continue
  n=$((n+1))
  [ "$(git hash-object --no-filters -- "$path")" = "$blob" ] || { echo "CONTENT-MISMATCH $path"; bad=1; }
  if [ "$mode" = 100755 ]; then [ -x "$path" ] || { echo "MODE-MISMATCH $path"; bad=1; }
  elif [ "$mode" = 100644 ]; then [ -x "$path" ] && { echo "MODE-MISMATCH $path"; bad=1; }
  elif [ "$mode" = 120000 ]; then [ -L "$path" ] || { echo "LINK-MISMATCH $path"; bad=1; }
  fi
done < <(git ls-files -s)
echo "re-hashed non-gitlink files: $n; mismatches: $bad"
echo "__pycache__ dirs: $(find . -path ./.git -prune -o -name __pycache__ -print | wc -l)"
echo "submodule status:"; git submodule status
