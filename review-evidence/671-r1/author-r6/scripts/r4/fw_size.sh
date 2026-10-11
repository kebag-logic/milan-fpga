#!/usr/bin/env bash
# Compile milan_baremetal.c by LiteX's own $(compile) rule from
# sw/firmware/milan_baremetal/Makefile against a product build tree's
# generated headers, once per source and per compiler triple, and print size.
# Usage: fw_size.sh <repo> <build-tree> <out> <triple> <src.c>...
set -u
repo=$1; tree=$2; out=$3; triple=$4; shift 4
for src in "$@"; do
  tag=$(basename "$(dirname "$src")")
  d="$out/$triple/$tag/software/libmilan_baremetal"
  mkdir -p "$d"
  cp "$repo/sw/firmware/milan_baremetal/Makefile" "$d/Makefile"
  make -C "$d" -I "$tree/software/libmilan_baremetal" TRIPLE="$triple" \
    LIBMILAN_BAREMETAL_DIRECTORY="$(dirname "$src")" milan_baremetal.o > "$d/build.log" 2>&1 || { cat "$d/build.log"; exit 1; }
  sha256sum "$src"
  readelf -p .comment "$d/milan_baremetal.o" | grep -m1 GCC
  size "$d/milan_baremetal.o"
done
