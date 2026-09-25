#!/bin/sh
# Verify the reviewed clone is byte-identical to the exact head: HEAD, tree,
# index records vs HEAD tree (paths, modes, blob ids), worktree bytes re-hashed
# for every tracked regular file, no hidden index flags, submodule gitlinks.
set -u
cd "$1" || exit 2
exp_head=7463ab0889da9a95fce7c921e386d6035d69778e
exp_tree=7741fe585b8de933e461cad62cf763976c30833a
rc=0
h=$(git rev-parse HEAD); t=$(git rev-parse 'HEAD^{tree}')
echo "HEAD $h"; echo "tree $t"
[ "$h" = "$exp_head" ] || { echo "HEAD mismatch"; rc=1; }
[ "$t" = "$exp_tree" ] || { echo "tree mismatch"; rc=1; }
idx=$(git ls-files -s | awk '{print $1" "$2" "$4}' | sort | sha256sum)
tre=$(git ls-tree -r HEAD | awk '{print $1" "$3" "$4}' | sort | sha256sum)
echo "index-vs-tree records: $( [ "$idx" = "$tre" ] && echo equal || echo DIFFER)"
[ "$idx" = "$tre" ] || rc=1
flags=$(git ls-files -v | grep -v '^H ' | wc -l)
echo "non-H index flags (assume-unchanged/skip-worktree/etc): $flags"
[ "$flags" = 0 ] || rc=1
bad=0; n=0
git ls-files -s | awk '$1!="160000"{print $2"\t"$4}' > /tmp/r249-2-files.$$
while IFS="$(printf '\t')" read -r blob path; do
  n=$((n+1))
  [ -L "$path" ] && got=$(readlink "$path" | tr -d '\n' | git hash-object --stdin) || got=$(git hash-object --no-filters -- "$path" 2>/dev/null)
  [ "$got" = "$blob" ] || { echo "BYTES DIFFER: $path"; bad=$((bad+1)); }
done < /tmp/r249-2-files.$$
rm -f /tmp/r249-2-files.$$
echo "tracked files re-hashed: $n, differing: $bad"
[ "$bad" = 0 ] || rc=1
echo "untracked (not ignored):"; git ls-files --others --exclude-standard | head
echo "gitlinks:"; git ls-tree HEAD protocol-processor gptp-processor third_party/verilog-axis external
git submodule status
for s in protocol-processor gptp-processor third_party/verilog-axis; do
  want=$(git ls-tree HEAD "$s" | awk '{print $3}'); got=$(git -C "$s" rev-parse HEAD)
  dirty=$(git -C "$s" status --porcelain | wc -l)
  echo "$s want=$want got=$got dirty=$dirty"
  [ "$want" = "$got" ] && [ "$dirty" = 0 ] || rc=1
done
echo "verify exit $rc"; exit $rc
