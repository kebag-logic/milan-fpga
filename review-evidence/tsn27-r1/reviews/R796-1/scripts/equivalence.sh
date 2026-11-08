#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Bit-exactness of the reviewed wire_put_be under several compilers and options.
set -u
. "$(dirname "$0")/env.sh"
out=$SCRATCH/equivalence; mkdir -p "$out"
rc=0
for cc in gcc clang clang-18; do
  for opt in -O0 -O2 -Os -O3; do
    exe=$out/eq-$cc$opt
    san="-fsanitize=undefined -fno-sanitize-recover=all"; [ "$cc" = clang-18 ] && san=""  # pinned clang-18 tree ships no sanitizer runtime
    if $cc -std=c11 $opt -Wall -Wextra -Werror $san \
        -I"$CLONE/include" "$PACKET/scripts/equivalence.c" -o "$exe" 2>"$exe.log"; then
      r=$("$exe"); echo "$cc $opt: $r"; "$exe" >/dev/null || rc=1
    else echo "$cc $opt: BUILD FAILED"; cat "$exe.log"; rc=1; fi
  done
done
echo "equivalence rc=$rc"
exit $rc
