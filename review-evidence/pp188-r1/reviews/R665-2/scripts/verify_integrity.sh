#!/usr/bin/env bash
# Exact-head integrity and merge-composition record for PR #195, round 2.
# Usage: verify_integrity.sh CLONE_DIR
# Prints: head and tree ids, worktree/index cleanliness, a blob/mode check of
# every tracked path against HEAD, the gitlink count, the conflict-free
# re-merge of the two merge parents compared with the head tree, and any
# top-level port or parameter line changed since the round-1 head.
set -u
C=$1
HEAD_WANT=7f56fc4d7f5102cac6dacb9c00f372d20d3b379e
TREE_WANT=34af6de87215cc90a774757debc8af90073aaa87
cd "$C" || exit 2
echo "head  $(git rev-parse HEAD) (want $HEAD_WANT)"
echo "tree  $(git rev-parse 'HEAD^{tree}') (want $TREE_WANT)"
echo "status-lines $(git status --porcelain --ignored=no | wc -l)"
git diff --quiet HEAD -- && echo "worktree==HEAD yes" || echo "worktree==HEAD NO"
git diff --cached --quiet HEAD -- && echo "index==HEAD yes" || echo "index==HEAD NO"
# every tracked path: index mode+blob == HEAD tree mode+blob, and the file's
# bytes hash to that blob
bad=0; n=0
while IFS=$'\t' read -r meta path; do
  n=$((n+1))
  mode=${meta%% *}; rest=${meta#* }; blob=${rest%% *}
  [ "$mode" = 160000 ] && continue
  got=$(git hash-object -- "$path")
  [ "$got" = "$blob" ] || { bad=$((bad+1)); echo "BLOB MISMATCH $path"; }
  if [ "$mode" = 100755 ]; then [ -x "$path" ] || { bad=$((bad+1)); echo "MODE $path"; }
  else [ -x "$path" ] && { bad=$((bad+1)); echo "MODE $path"; }; fi
done < <(git ls-files -s)
echo "tracked $n mismatches $bad"
diff <(git ls-files -s | awk '{print $1, $2, $4}') \
     <(git ls-tree -r HEAD | awk '{print $1, $3, $4}') >/dev/null \
  && echo "index entries == HEAD tree yes" || echo "index entries == HEAD tree NO"
echo "gitlinks $(git ls-files -s | awk '$1==160000' | wc -l)"
P1=$(git rev-parse 'HEAD^1'); P2=$(git rev-parse 'HEAD^2')
echo "parents $P1 $P2"
echo "re-merge tree $(git merge-tree --write-tree "$P1" "$P2" | head -1)"
echo "top port/parameter lines changed since cb8bab04: $(git diff cb8bab04 HEAD -- hdl/top/protocol_processor_top.sv | grep -cE '^[-+][[:space:]]*(input|output|inout|parameter)\b')"
