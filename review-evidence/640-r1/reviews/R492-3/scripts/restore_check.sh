#!/bin/sh
# Verify a clone equals an exact head: HEAD, tree, index tree, every tracked
# blob's bytes and mode, an empty status including ignored files, and each
# initialised submodule checkout equal to its gitlink.
# Usage: restore_check.sh <repo> <head-sha> <tree-sha>
set -u
repo=$1 head=$2 tree=$3 bad=0
cd "$repo" || exit 2
h=$(git rev-parse HEAD); t=$(git rev-parse 'HEAD^{tree}'); i=$(git write-tree)
echo "HEAD=$h tree=$t index_tree=$i"
[ "$h" = "$head" ] && [ "$t" = "$tree" ] && [ "$i" = "$tree" ] || bad=1
n=0 mism=0
git ls-files -s | while read -r mode sha stage path; do
  [ "$mode" = 160000 ] && continue
  if [ -L "$path" ]; then got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin); fm=120000
  else got=$(git hash-object --no-filters "$path"); [ -x "$path" ] && fm=100755 || fm=100644; fi
  [ "$got" = "$sha" ] && [ "$fm" = "$mode" ] || echo "MISMATCH $mode $path"
done > /tmp/.rc_$$ 
mism=$(grep -c MISMATCH /tmp/.rc_$$); n=$(git ls-files -s | grep -vc '^160000'); rm -f /tmp/.rc_$$
echo "tracked_blobs=$n mismatches=$mism"; [ "$mism" = 0 ] || bad=1
st=$(git status --porcelain --ignored | wc -l); echo "status_lines_including_ignored=$st"; [ "$st" = 0 ] || bad=1
git ls-files -s | awk '$1=="160000"{print $2, $4}' | while read -r sha path; do
  if [ -e "$path/.git" ]; then sub=$(git -C "$path" rev-parse HEAD); [ "$sub" = "$sha" ] && r=match || r=MISMATCH
  else r=not-initialised; fi; echo "submodule $path gitlink=$sha $r"
done
echo "restore_ok=$([ $bad = 0 ] && echo yes || echo no)"
exit $bad
