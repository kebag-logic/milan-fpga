#!/bin/sh
# Expose the pinned Clang 18.1.3 under the name the gates call. TSN_TOOLS is the pinned tool root.
: "${TSN_TOOLS:?set TSN_TOOLS to the pinned tool root}"
exec env LD_LIBRARY_PATH="$TSN_TOOLS/clang-18/root/usr/lib/x86_64-linux-gnu" "$TSN_TOOLS/clang-18/root/usr/lib/llvm-18/bin/clang" "$@"
