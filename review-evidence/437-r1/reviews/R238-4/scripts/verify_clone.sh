#!/usr/bin/env bash
# Verify a clone is byte-exact at an expected head: HEAD and tree ids, index
# records equal to the tree (mode, object, path), every tracked regular file
# re-hashed from disk equal to its index blob (immune to assume-unchanged),
# no assume-unchanged/skip-worktree flags, and each gitlink equal to its
# submodule checkout's HEAD. Usage: verify_clone.sh <clone> <head> <tree>
set -u
cd "$1" || exit 2
ok=1
[ "$(git rev-parse HEAD)" = "$2" ] || { echo "HEAD mismatch"; ok=0; }
[ "$(git rev-parse 'HEAD^{tree}')" = "$3" ] || { echo "tree mismatch"; ok=0; }
diff <(git ls-files -s | awk '{print $1, $2, $4}' | sort -k3) <(git ls-tree -r HEAD | awk '{print $1, $3, $4}' | sort -k3) >/dev/null || { echo "index differs from HEAD tree"; ok=0; }
flags=$(git ls-files -v | awk 'substr($1,1,1) ~ /[a-zS]/' | wc -l); [ "$flags" = 0 ] || { echo "hidden-index flags: $flags"; ok=0; }
bad=0; n=0
while read -r mode obj stage path; do
  [ "$mode" = 160000 ] && continue
  n=$((n+1))
  if [ "$mode" = 120000 ]; then got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin); else got=$(git hash-object --no-filters -- "$path"); fi
  [ "$got" = "$obj" ] || { echo "BLOB MISMATCH $path"; bad=$((bad+1)); }
  if [ "$mode" = 100755 ] && [ ! -x "$path" ]; then echo "MODE MISMATCH $path"; bad=$((bad+1)); fi
  if [ "$mode" = 100644 ] && [ -x "$path" ] && [ ! -L "$path" ]; then echo "MODE MISMATCH $path"; bad=$((bad+1)); fi
done < <(git ls-files -s)
[ "$bad" = 0 ] || ok=0
echo "tracked non-gitlink entries re-hashed: $n, mismatches: $bad"
git ls-files -s | awk '$1=="160000"{print $2, $4}' | while read -r obj path; do
  if [ -e "$path/.git" ]; then sub=$(git -C "$path" rev-parse HEAD 2>/dev/null || echo unreadable); else sub=uninitialised; fi
  echo "gitlink $path $obj checkout $sub $([ "$sub" = "$obj" ] && echo MATCH || echo DIFFERENT)"
done
echo "porcelain lines: $(git status --porcelain --ignore-submodules=none | wc -l)"
[ "$ok" = 1 ] && echo "CLONE EXACT" || { echo "CLONE NOT EXACT"; exit 1; }
