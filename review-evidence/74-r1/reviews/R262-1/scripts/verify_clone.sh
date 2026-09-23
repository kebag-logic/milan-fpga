#!/bin/sh
# Reviewer restore check (R262-1): proves the review clone is the exact head.
# usage: verify_clone.sh <clone> <head_sha> <tree_sha>
# 1. HEAD and HEAD^{tree} are the published ids;
# 2. the index equals the head tree (paths, modes, blob ids, stage 0 only);
# 3. every tracked non-gitlink path re-hashes on disk to its index blob id
#    and its on-disk type/mode matches (100644 / 100755 / 120000);
# 4. the three required gitlinks are checked out at their recorded commits;
# 5. no untracked or ignored residue remains.
set -u
C=$1; HEAD_WANT=$2; TREE_WANT=$3
cd "$C" || exit 2
fail=0
h=$(git rev-parse HEAD); t=$(git rev-parse 'HEAD^{tree}')
echo "HEAD=$h TREE=$t"
[ "$h" = "$HEAD_WANT" ] || { echo "FAIL head"; fail=1; }
[ "$t" = "$TREE_WANT" ] || { echo "FAIL tree"; fail=1; }
idx=$(git ls-files -s | awk '{print $1, $2, $4}' | sha256sum | cut -d' ' -f1)
tre=$(git ls-tree -r HEAD | awk '{print $1, $3, $4}' | sha256sum | cut -d' ' -f1)
stages=$(git ls-files -s | awk '$3 != 0' | wc -l)
echo "index-digest=$idx tree-digest=$tre nonzero-stages=$stages"
[ "$idx" = "$tre" ] && [ "$stages" -eq 0 ] || { echo "FAIL index != tree"; fail=1; }
n=0; bad=0
git ls-files -s | while read -r mode blob stage path; do
  [ "$mode" = 160000 ] && continue
  if [ "$mode" = 120000 ]; then
    [ -L "$path" ] || { echo "FAIL not a symlink: $path"; exit 1; }
    got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)
  else
    [ -f "$path" ] && [ ! -L "$path" ] || { echo "FAIL not a regular file: $path"; exit 1; }
    if [ -x "$path" ]; then m=100755; else m=100644; fi
    [ "$m" = "$mode" ] || { echo "FAIL mode $path: disk $m index $mode"; exit 1; }
    got=$(git hash-object --no-filters -- "$path")
  fi
  [ "$got" = "$blob" ] || { echo "FAIL bytes $path"; exit 1; }
done || fail=1
echo "tracked files re-hashed: $(git ls-files -s | awk '$1 != 160000' | wc -l)"
for s in protocol-processor gptp-processor third_party/verilog-axis; do
  want=$(git ls-files -s -- "$s" | awk '{print $2}')
  have=$(git -C "$s" rev-parse HEAD 2>/dev/null)
  dirty=$(git -C "$s" status --porcelain --ignored 2>/dev/null | wc -l)
  echo "gitlink $s index=$want checkout=$have residue=$dirty"
  [ -n "$want" ] && [ "$want" = "$have" ] && [ "$dirty" -eq 0 ] || { echo "FAIL gitlink $s"; fail=1; }
done
res=$(git status --porcelain --ignored --ignore-submodules=none | wc -l)
echo "status residue lines (incl. ignored): $res"
git status --porcelain --ignored --ignore-submodules=none | head -5
[ "$res" -eq 0 ] || fail=1
[ "$fail" -eq 0 ] && echo "RESTORE CHECK: PASS" || echo "RESTORE CHECK: FAIL"
exit "$fail"
