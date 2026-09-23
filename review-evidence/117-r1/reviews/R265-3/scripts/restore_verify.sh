#!/usr/bin/env bash
# Verify the review clone is byte-exact at the expected head: HEAD, tree, index
# vs tree, working-tree bytes vs index, no hidden-index flags, submodule gitlinks.
# Usage: restore_verify.sh <clone> <expected-head> <expected-tree>
set -u
clone=$1 head=$2 tree=$3
g() { git -C "$clone" "$@"; }
echo "HEAD $(g rev-parse HEAD) expected $head"
echo "tree $(g rev-parse 'HEAD^{tree}') expected $tree"
echo "index tree $(g write-tree 2>/dev/null) expected $tree"
echo "porcelain lines (incl. untracked): $(g status --porcelain --untracked-files=all | wc -l)"
echo "hidden-index flags (h/S/lowercase): $(g ls-files -v | grep -c -E '^[a-zS] ')"
# every tracked regular file / symlink: hash working-tree bytes and compare with the index
mism=0; n=0
while IFS= read -r -d '' rec; do
  meta=${rec%%$'\t'*}; path=${rec#*$'\t'}
  mode=${meta%% *}; rest=${meta#* }; sha=${rest%% *}
  [ "$mode" = 160000 ] && continue
  n=$((n+1))
  if [ "$mode" = 120000 ]; then
    got=$(printf '%s' "$(readlink "$clone/$path")" | git hash-object --stdin)
  else
    got=$(git hash-object --no-filters "$clone/$path" 2>/dev/null)
    if [ -x "$clone/$path" ]; then wm=100755; else wm=100644; fi
    [ "$wm" != "$mode" ] && { mism=$((mism+1)); echo "mode differs: $path"; }
  fi
  [ "$got" != "$sha" ] && { mism=$((mism+1)); echo "bytes differ: $path"; }
done < <(g ls-files -s -z)
echo "tracked files checked $n, mismatches $mism"
echo "submodule gitlinks at HEAD:"; g ls-tree HEAD external gptp-processor protocol-processor third_party/verilog-axis
echo "submodule status:"; g submodule status
