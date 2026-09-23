#!/bin/sh
# Record the review clone's exact state: HEAD, tree, tracked bytes/modes vs
# the index and HEAD, untracked files, and the required submodule gitlinks.
# Usage: verify_clone.sh <clone-dir>
set -eu
C=${1:?clone dir}
cd "$C"
echo "HEAD $(git rev-parse HEAD)"
echo "TREE $(git rev-parse 'HEAD^{tree}')"
echo "index-vs-HEAD diff (cached, names):"; git diff --cached --name-status | sed 's/^/  /'
echo "worktree-vs-index diff (names):"; git diff --name-status | sed 's/^/  /'
echo "untracked (excluding ignored):"; git ls-files --others --exclude-standard | sed 's/^/  /'
echo "ignored untracked entries (e.g. caches a gate could leave):"; git ls-files --others --ignored --exclude-standard --directory | sed 's/^/  /'
echo "assume-unchanged/skip-worktree flags (h/S/s):"; git ls-files -v | grep -E '^[hSs] ' | sed 's/^/  /' || true
# every tracked non-gitlink entry: hash the worktree bytes and compare with HEAD
bad=0
git ls-tree -r HEAD | while read -r mode type obj path; do
  [ "$type" = blob ] || continue
  if [ "$mode" = 120000 ]; then
    got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)
  else
    got=$(git hash-object --no-filters -- "$path")
  fi
  [ "$got" = "$obj" ] || { echo "  BYTES DIFFER: $path"; }
  if [ "$mode" = 100755 ] && [ ! -x "$path" ]; then echo "  MODE DIFFERS (want +x): $path"; fi
  if [ "$mode" = 100644 ] && [ -x "$path" ] && [ ! -L "$path" ]; then echo "  MODE DIFFERS (want -x): $path"; fi
done > /tmp/verify_clone_$$.txt
echo "tracked blob byte/mode mismatches: $(wc -l < /tmp/verify_clone_$$.txt)"; cat /tmp/verify_clone_$$.txt; rm -f /tmp/verify_clone_$$.txt
echo "gitlinks (HEAD tree) vs submodule checkouts:"
git ls-tree -r HEAD | awk '$2=="commit"{print $3, $4}' | while read -r obj path; do
  if [ -e "$path/.git" ]; then co=$(git -C "$path" rev-parse HEAD 2>/dev/null || echo none); st=$(git -C "$path" status --porcelain | wc -l)
  else co=uninitialised; st=-; fi
  echo "  $path gitlink=$obj checkout=$co dirty_entries=$st"
done
