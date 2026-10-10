#!/usr/bin/env bash
# Compare the base revision's core copies with the stack's files at a revision, token by token
# (comments stripped by the preprocessor in -fpreprocessed mode, whitespace collapsed).
# usage: core_tokens.sh <milan-fpga repo> <base rev> <stack repo> <stack rev>
set -u
repo=$1 base=$2 stack=$3 rev=$4
tmp=$(mktemp -d)
pairs="adp/adp.c:src/adp.c acmp/acmp.c:src/acmp.c maap/maap.c:src/maap.c adp/adp.h:include/adp.h acmp/acmp.h:include/acmp.h maap/maap.h:include/maap.h wire/wire.h:include/wire.h"
rc=0
for p in $pairs; do
  old=${p%%:*} new=${p##*:}
  git -C "$repo" show "$base:sw/firmware/ctrl/$old" > "$tmp/a" || { echo "MISSING base $old"; rc=1; continue; }
  git -C "$stack" show "$rev:$new" > "$tmp/b" || { echo "MISSING stack $new"; rc=1; continue; }
  for f in a b; do gcc -fpreprocessed -dD -E -P -x c "$tmp/$f" 2>/dev/null | tr -s ' \t\n' ' ' > "$tmp/$f.tok"; done
  if cmp -s "$tmp/a.tok" "$tmp/b.tok"; then echo "TOKEN-IDENTICAL $old == $new"; else echo "DIFFER $old != $new"; rc=1; fi
  echo "  raw-bytes-identical: $(cmp -s "$tmp/a" "$tmp/b" && echo yes || echo no)"
done
rm -rf "$tmp"; exit $rc
