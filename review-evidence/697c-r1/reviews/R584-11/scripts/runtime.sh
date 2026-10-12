#!/usr/bin/env bash
# Differential stand-in runtime archives for ctrl_srp_image.py, from the repository's own image runtime.
# usage: runtime.sh <tree> <output directory>; MILAN_RV32_CC names the pinned SDK compiler.
set -euo pipefail
tree=$1 out=$2
: "${MILAN_RV32_CC:?}"
mkdir -p "$out"
img="$tree/sw/firmware/ctrl/test/rv32_image"
flags=(-march=rv32i -mabi=ilp32 -Os -ffreestanding -fno-pie -fno-common -ffunction-sections -fdata-sections
       -fno-builtin -fno-stack-protector -fno-tree-loop-distribute-patterns)
"$MILAN_RV32_CC" "${flags[@]}" -c "$img/image_rt.c" -o "$out/image_rt.o"
"$MILAN_RV32_CC" "${flags[@]}" -c "$img/image_arith.c" -o "$out/image_arith.o"
ar=${MILAN_RV32_CC%gcc}ar
rm -f "$out/libc.a" "$out/libcompiler_rt.a"
"$ar" crs "$out/libc.a" "$out/image_rt.o"
"$ar" crs "$out/libcompiler_rt.a" "$out/image_arith.o"
sha256sum "$out/libc.a" "$out/libcompiler_rt.a"
