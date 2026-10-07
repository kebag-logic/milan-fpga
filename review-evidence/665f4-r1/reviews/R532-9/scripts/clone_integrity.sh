#!/bin/bash
# usage: clone_integrity.sh CLONE -- prove the clone is the exact head: index tree,
# every tracked blob's bytes and mode, status, and the submodule gitlinks.
cd "$1" || exit 2
echo "HEAD $(git rev-parse HEAD)"
echo "HEAD tree $(git rev-parse 'HEAD^{tree}')"
echo "index tree $(git write-tree)"
bad=0; n=0
while IFS=$'\t' read -r meta path; do
  set -- $meta; mode=$1; type=$2; sha=$3
  [ "$type" = blob ] || continue
  n=$((n+1))
  if [ "$mode" = 120000 ]; then got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin); [ -L "$path" ] || got=x
  else got=$(git hash-object --no-filters "$path" 2>/dev/null)
       if [ "$mode" = 100755 ]; then [ -x "$path" ] || got=mode; else [ -x "$path" ] && got=mode; fi; fi
  [ "$got" = "$sha" ] || { bad=$((bad+1)); echo "MISMATCH $path"; }
done < <(git ls-tree -r HEAD)
echo "tracked blobs checked: $n, mismatches: $bad"
echo "status entries (incl. ignored): $(git status --porcelain --ignored | wc -l)"
git ls-tree HEAD external gptp-processor protocol-processor third_party/lwSRP third_party/verilog-axis
git submodule status
for s in gptp-processor protocol-processor third_party/verilog-axis; do echo "$s worktree entries: $(git -C $s status --porcelain --ignored | wc -l)"; done
