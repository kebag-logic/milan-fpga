#!/usr/bin/env bash
# Closing integrity check of the reviewer clone: exact head and tree, clean worktree,
# index entries (mode, blob, path) equal to HEAD's tree, every tracked file's bytes and
# mode equal to its blob, and the submodule gitlinks (none expected in this repository).
# Usage: final_state.sh CLONE HEAD TREE
set -u
c=$1; head=$2; tree=$3
cd "$c" || exit 2
rc=0
h=$(git rev-parse HEAD); t=$(git rev-parse HEAD^{tree})
echo "HEAD $h"; echo "tree $t"
[ "$h" = "$head" ] && [ "$t" = "$tree" ] || { echo "HEAD/tree MISMATCH"; rc=1; }
st=$(git status --porcelain --ignored=no --untracked-files=all)
[ -z "$st" ] && echo "worktree clean (no modified, staged or untracked files)" || { echo "worktree NOT clean:"; echo "$st"; rc=1; }
if diff <(git ls-files -s | awk '{print $1, $2, $4}') <(git ls-tree -r HEAD | awk '{print $1, $3, $4}') >/dev/null; then
  echo "index == HEAD tree ($(git ls-files | wc -l) entries, modes and blobs)"
else
  echo "index DIFFERS from HEAD tree"; rc=1
fi
bad=0
while IFS= read -r line; do
  mode=${line%% *}; rest=${line#* }; blob=${rest%% *}; path=${line#*	}
  [ "$mode" = 160000 ] && continue
  if [ "$mode" = 120000 ]; then got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)
  else got=$(git hash-object --no-filters "$path"); fi
  fm=100644; [ -x "$path" ] && fm=100755; [ -L "$path" ] && fm=120000
  [ "$got" = "$blob" ] && [ "$fm" = "$mode" ] || { echo "BYTES/MODE differ: $path"; bad=$((bad+1)); }
done < <(git ls-files -s)
[ $bad -eq 0 ] && echo "every tracked file's bytes and mode equal its blob" || rc=1
gl=$(git ls-files -s | awk '$1==160000' | wc -l)
echo "gitlinks in tree: $gl; .gitmodules: $([ -f .gitmodules ] && echo present || echo absent)"
git submodule status 2>&1 | sed 's/^/submodule: /'
exit $rc
