#!/bin/sh
# Template of the scratch/bin/{clang,clang++,clang-18,clang++-18} wrappers used for this review (see TOOLCHAIN.md).
# Pinned Clang 18.1.3, with a scratch resource dir that adds compiler-rt 18.1.3 and the Ubuntu 24.04 GCC 13
# libstdc++ headers (the CI image's), because the host's GCC 16 libstdc++ is not parseable by Clang 18.
# Replace clang by clang++ in B for the C++ wrappers.
L=$TOOLS/clang-18/root/usr/lib/x86_64-linux-gnu
B=$TOOLS/clang-18/root/usr/lib/llvm-18/bin/clang
if [ "$1" = "-cc1" ]; then exec env LD_LIBRARY_PATH=$L "$B" "$@"; fi
exec env LD_LIBRARY_PATH=$L "$B" -resource-dir $PACKET/scratch/res18 --gcc-toolchain=$PACKET/scratch/gcc13/x/usr "$@"
