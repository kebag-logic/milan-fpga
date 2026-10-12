#!/usr/bin/env bash
# Compile dev's three cores and the pinned stack's with the RV32 image flags, release and debug,
# each from a directory holding only that core and its headers under the same names, and compare objects.
# usage: objects.sh <dev clone> <stack dir> <work dir>; needs MILAN_RV32_CC.
set -euo pipefail
dev=$1 stack=$2 work=$3
: "${MILAN_RV32_CC:?}"
rm -rf "$work"; mkdir -p "$work"
flags=(-march=rv32i -mabi=ilp32 -ffreestanding -fno-stack-protector -Os -std=c11 -Wall -Wextra -Werror -pedantic
       -DCTRL_MBX_BASE=0x80000000u -ffile-prefix-map="$work"=. -nostdinc -isystem "$("$MILAN_RV32_CC" -print-file-name=include)" -I "$dev/sw/firmware/gtest/rv32_include" )
for core in adp acmp maap; do
  for side in dev stack; do
    d="$work/$side/$core"; mkdir -p "$d"
    if [ $side = dev ]; then
      cp "$dev/sw/firmware/ctrl/$core/$core.c" "$dev/sw/firmware/ctrl/$core/$core.h" "$dev/sw/firmware/ctrl/wire/wire.h" "$d/"
    else
      cp "$stack/src/$core.c" "$stack/include/$core.h" "$stack/include/wire.h" "$d/"
    fi
  done
  for mode in -DNDEBUG -UNDEBUG; do
    for side in dev stack; do
      (cd "$work/$side/$core" && "$MILAN_RV32_CC" "${flags[@]}" "$mode" -I. -c "$core.c" -o "$core$mode.o")
    done
    if cmp -s "$work/dev/$core/$core$mode.o" "$work/stack/$core/$core$mode.o"; then v=EQUAL; else v=DIFFER; fi
    echo "$core $mode $v $(sha256sum < "$work/stack/$core/$core$mode.o" | cut -c1-16)"
  done
done
