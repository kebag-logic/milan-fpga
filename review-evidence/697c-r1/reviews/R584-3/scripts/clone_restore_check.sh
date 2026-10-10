#!/usr/bin/env bash
# R584-3: the review clone is at the exact head: HEAD, tree, index == HEAD tree, every tracked blob re-hashed
# from the working tree with its mode, no assume-unchanged/skip-worktree flag, gitlinks at their pins, clean.
set -u; cd "$1"
echo "HEAD $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}') write-tree $(git write-tree)"
diff <(git ls-files -s | awk '{print $1, $2, $4}') <(git ls-tree -r HEAD | awk '{print $1, $3, $4}') >/dev/null && echo "index == HEAD tree" || echo "INDEX DIFFERS"
echo "flags (h/S lines): $(git ls-files -v | grep -c '^[a-zS]')"
bad=0; n=0
while IFS= read -r -d '' line; do
  meta=${line%%$'\t'*}; path=${line#*$'\t'}; mode=${meta%% *}; rest=${meta#* }; sha=${rest%% *}
  [ "$mode" = 160000 ] && continue
  n=$((n+1))
  if [ "$mode" = 120000 ]; then got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)
  else got=$(git hash-object "$path"); fi
  want_x=no; [ "$mode" = 100755 ] && want_x=yes; is_x=no; [ -x "$path" ] && [ ! -L "$path" ] && is_x=yes
  [ "$mode" = 120000 ] && is_x=$want_x
  if [ "$got" != "$sha" ] || [ "$want_x" != "$is_x" ]; then bad=$((bad+1)); echo "MISMATCH $mode $path"; fi
done < <(git ls-files -s -z)
echo "tracked blobs re-hashed with modes: $n, mismatches: $bad"
git ls-tree -r HEAD | awk '$1=="160000"{print $3, $4}' | while read sha p; do
  if [ -e "$p/.git" ]; then echo "gitlink $p $sha checkout $(git -C "$p" rev-parse HEAD) dirty=$(git -C "$p" status --porcelain --ignored | wc -l)"
  else echo "gitlink $p $sha (not initialised)"; fi
done
echo "status lines (incl. ignored): $(git status --porcelain --ignored | wc -l)"
