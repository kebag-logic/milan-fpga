#!/bin/sh
# Record the review clone's exact-head integrity: HEAD, tree, index records
# (blob ids, modes, stages, gitlinks), worktree cleanliness, and submodule
# checkouts. Usage: 00_integrity.sh <clone> <label>  (prints to stdout)
set -eu
clone=$1
label=$2
cd "$clone"
echo "label: $label"
echo "HEAD: $(git rev-parse HEAD)"
echo "tree: $(git rev-parse 'HEAD^{tree}')"
echo "expected HEAD: 2accfadfd3d4d8a318e3e714ee0dc87fc84e4164"
echo "expected tree: 37b72c34062ccf6c9370311cd2e203a64c65fdd0"
echo "index records sha256: $(git ls-files -s | sha256sum | cut -d' ' -f1)"
echo "index records count: $(git ls-files -s | wc -l)"
echo "HEAD tree records sha256: $(git ls-tree -r --full-tree HEAD | sha256sum | cut -d' ' -f1)"
# the index must describe exactly HEAD's tree (same blob ids and modes)
if [ "$(git write-tree)" = "$(git rev-parse 'HEAD^{tree}')" ]; then
  echo "index tree == HEAD tree: yes"
else
  echo "index tree == HEAD tree: NO"
fi
echo "gitlinks (index):"
git ls-files -s | awk '$1=="160000"{print "  " $0}'
echo "submodule status:"
git submodule status | sed 's/^/  /'
echo "status --porcelain (tracked + untracked, ignored excluded):"
st=$(git status --porcelain=v1 --untracked-files=all)
if [ -z "$st" ]; then echo "  (clean)"; else echo "$st" | sed 's/^/  /'; fi
echo "worktree bytes vs index (diff --quiet): $(git diff --quiet && echo clean || echo DIRTY)"
echo "index vs HEAD (diff --cached --quiet): $(git diff --cached --quiet && echo clean || echo DIRTY)"
# hidden-edit guard: no index entry may carry assume-unchanged or skip-worktree
hidden=$(git ls-files -v | grep -E '^[a-zS]' || true)
if [ -z "$hidden" ]; then echo "assume-unchanged/skip-worktree entries: none"; else echo "HIDDEN ENTRIES:"; echo "$hidden"; fi
# re-hash every tracked regular file from the worktree and compare to its blob id
bad=0
git ls-files -s | awk '$1!="160000"{print $2 "\t" $4}' | while IFS="$(printf '\t')" read -r blob path; do
  if [ -L "$path" ]; then
    got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)
  else
    got=$(git hash-object --no-filters -- "$path")
  fi
  if [ "$got" != "$blob" ]; then echo "  BLOB MISMATCH: $path"; fi
done > /tmp/r263-2-blobcheck.$$ || true
if [ -s /tmp/r263-2-blobcheck.$$ ]; then cat /tmp/r263-2-blobcheck.$$; echo "worktree blob re-hash: MISMATCH"; else echo "worktree blob re-hash: all tracked files match their index blob ids"; fi
rm -f /tmp/r263-2-blobcheck.$$
