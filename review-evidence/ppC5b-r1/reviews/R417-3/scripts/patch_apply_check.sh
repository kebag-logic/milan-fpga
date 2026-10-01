#!/usr/bin/env bash
# Every campaign patch under tb/ must pass `git apply --check` against an exported tree.
# usage: patch_apply_check.sh <exported-tree>
cd "$1" || exit 2; n=0; bad=0
while read -r p; do n=$((n+1)); git apply --check "$p" 2>/tmp/pac.$$ || { bad=$((bad+1)); echo "REFUSED $p"; cat /tmp/pac.$$; }; done < <(find tb -name '*.patch' | sort)
echo "patches: $n, refused: $bad"; rm -f /tmp/pac.$$; [ $bad -eq 0 ]
