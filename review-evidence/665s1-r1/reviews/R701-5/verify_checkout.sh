#!/bin/bash
# Verify a detached review clone is at the exact head with every tracked blob,
# mode and index entry intact, and each initialized submodule at its gitlink.
#   $1 the clone   $2 the expected head
set -u
cd "$1" || exit 2
fail=0
head=$(git rev-parse HEAD); echo "HEAD $head tree $(git rev-parse HEAD^{tree})"
[ "$head" = "$2" ] || { echo "HEAD mismatch"; fail=1; }
git diff --quiet && echo "worktree vs index: clean" || { echo "worktree differs"; fail=1; }
git diff --cached --quiet && echo "index vs HEAD: clean" || { echo "index differs"; fail=1; }
idx=$(git ls-files -s | awk '$1!="160000"{print $1, $2, $4}' | sha256sum | cut -c1-64)
tree=$(git ls-tree -r HEAD | awk '$2=="blob"{print $1, $3, $4}' | sha256sum | cut -c1-64)
[ "$idx" = "$tree" ] && echo "index modes/blobs equal HEAD tree: $idx" || { echo "index/tree differ"; fail=1; }
n=0; bad=0
while IFS=$'\t' read -r meta path; do
    set -- $meta; mode=$1 blob=$2
    [ "$mode" = 160000 ] && continue
    n=$((n+1))
    if [ "$mode" = 120000 ]; then got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)
    else got=$(git hash-object --no-filters -- "$path")
         if [ "$mode" = 100755 ] && [ ! -x "$path" ]; then echo "mode lost: $path"; bad=$((bad+1)); fi
         if [ "$mode" = 100644 ] && [ -x "$path" ]; then echo "mode gained: $path"; bad=$((bad+1)); fi
    fi
    [ "$got" = "$blob" ] || { echo "blob differs: $path"; bad=$((bad+1)); }
done < <(git ls-files -s | awk '{print $1" "$2"\t"$4}')
echo "tracked files hashed: $n, differences: $bad"; [ $bad = 0 ] || fail=1
git ls-tree -r HEAD | awk '$2=="commit"{print $3, $4}' | while read -r want path; do
    if [ -e "$path/.git" ]; then got=$(git -C "$path" rev-parse HEAD); dirty=$(git -C "$path" status --porcelain | wc -l)
        echo "submodule $path gitlink $want checkout $got dirty=$dirty $([ "$got" = "$want" ] && [ "$dirty" = 0 ] && echo OK || echo MISMATCH)"
    else echo "submodule $path gitlink $want not initialized"; fi
done
untracked=$(git status --porcelain --ignored --untracked-files=all | grep -v '^!! external/' | wc -l)
echo "untracked or ignored entries: $untracked"; git status --porcelain --ignored --untracked-files=all | head -5
exit $fail
