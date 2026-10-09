#!/usr/bin/env bash
# Prove the review clone still holds the exact head: HEAD, tree, index tree,
# every tracked blob's bytes and mode, empty status (untracked and ignored
# shown) and the required submodule gitlinks. Usage: restore_check.sh <repo> <head>
set -u
repo=$1; want=$2; cd "$repo" || exit 2; rc=0
h=$(git rev-parse HEAD); t=$(git rev-parse HEAD^{tree}); it=$(git write-tree)
echo "HEAD $h"; echo "tree $t"; echo "index-tree $it"
[ "$h" = "$want" ] || { echo "HEAD MISMATCH"; rc=1; }
[ "$t" = "$it" ] || { echo "INDEX TREE MISMATCH"; rc=1; }
git update-index -q --refresh
git diff-index --quiet HEAD -- || { echo "WORKTREE/INDEX DIFFERS"; rc=1; }
n=0; badb=0
while IFS=$'\t' read -r meta path; do
  mode=${meta%% *}; rest=${meta#* }; sha=${rest%% *}
  [ "$mode" = 160000 ] && continue
  n=$((n+1))
  if [ "$mode" = 120000 ]; then got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)
  else got=$(git hash-object --no-filters -- "$path"); fi
  fm=$(stat -c %a -- "$path" 2>/dev/null); case "$mode" in 100755) wm=755;; 100644) wm=644;; *) wm=$fm;; esac
  if [ "$got" != "$sha" ]; then echo "BLOB DIFF $path"; badb=$((badb+1)); fi
  if [ "$mode" = 100755 ] && [ ! -x "$path" ]; then echo "MODE DIFF $path"; badb=$((badb+1)); fi
done < <(git ls-files -s | sed -E 's/^([0-7]+) ([0-9a-f]+) [0-3]\t/\1 \2\t/')
echo "tracked blobs checked=$n differing=$badb"; [ $badb = 0 ] || rc=1
st=$(git status --porcelain=v1 --untracked-files=all --ignored); echo "status lines: $(printf '%s' "$st" | grep -c . )"
[ -z "$st" ] || { printf '%s\n' "$st" | head -20; rc=1; }
echo "gitlinks:"; git ls-files -s | awk '$1==160000{print "  "$4" "$2}'
echo "submodule status:"; git submodule status | sed 's/^/  /'
for s in protocol-processor gptp-processor third_party/verilog-axis; do
  want_s=$(git ls-files -s -- "$s" | awk '{print $2}'); got_s=$(git -C "$s" rev-parse HEAD 2>/dev/null)
  [ "$want_s" = "$got_s" ] && echo "  $s checkout matches gitlink" || { echo "  $s MISMATCH ($got_s vs $want_s)"; rc=1; }
done
echo "restore rc=$rc"; exit $rc
