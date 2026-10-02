#!/bin/sh
# usage: apply_check.sh TREE  - git apply --check -v of every *.patch in TREE, from TREE's root
cd "$1" || exit 2
n=0; bad=0
for p in $(find . -name '*.patch' | sort); do
  n=$((n+1))
  if out=$(git apply --check -v "$p" 2>&1); then
    off=$(printf '%s\n' "$out" | grep -o 'at [0-9]* (offset [-0-9]* lines\?)' | tr '\n' ';')
    echo "OK     $p ${off}"
  else
    bad=$((bad+1)); echo "REFUSE $p"; printf '%s\n' "$out" | sed 's/^/    /'
  fi
done
echo "patches=$n refused=$bad"
