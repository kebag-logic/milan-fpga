#!/bin/sh
# Show that the delta changes no non-comment SystemVerilog token.
# usage: sv_nocomment_delta.sh <repo> <base> <head> <file>...
set -eu
REPO=$1; B=$2; H=$3; shift 3
strip() { sed -e 's#//.*$##' -e 's/[[:space:]]\+/ /g' -e 's/^ //;s/ $//' | grep -v '^$' || true; }
for f in "$@"; do
  a=$(git -C "$REPO" show "$B:$f" | strip | sha256sum | cut -c1-16)
  b=$(git -C "$REPO" show "$H:$f" | strip | sha256sum | cut -c1-16)
  [ "$a" = "$b" ] && echo "SAME-CODE $f $a" || echo "CODE-DIFFERS $f $a $b"
done
