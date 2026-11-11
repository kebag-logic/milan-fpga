#!/bin/sh
# Usage: TSN_TOOLS=<tools> launch.sh NAME DIR CMD...
# Run CMD in DIR detached; its output goes to receipts/NAME.log and its exit status to receipts/NAME.rc.
# TSN_TOOLS holds the pinned GoogleTest 1.14.0 (gtest-1.14.0), Clang 18.1.3 (clang-18) and clang-tidy 18.1.3
# (clang-tidy-18); they go ahead of the host's. scratch/shim holds shim-clang.sh and shim-clangxx.sh as clang, clang++.
P=$(cd "$(dirname "$0")/.." && pwd)
: "${TSN_TOOLS:?set TSN_TOOLS to the pinned tool root}"
name=$1; dir=$2; shift 2
rm -f "$P/receipts/$name.rc"
export PATH="$P/scratch/shim:$TSN_TOOLS/clang-18/bin:$TSN_TOOLS/clang-tidy-18/bin:$PATH"
export PKG_CONFIG_PATH="$TSN_TOOLS/gtest-1.14.0/lib/pkgconfig"
export CMAKE_PREFIX_PATH="$TSN_TOOLS/gtest-1.14.0"
export LD_LIBRARY_PATH="$TSN_TOOLS/gtest-1.14.0/lib"
cd "$dir" || exit 2
setsid nohup sh -c '"$@" > "$0.log" 2>&1; echo $? > "$0.rc"' "$P/receipts/$name" "$@" < /dev/null > /dev/null 2>&1 &
echo "started $name pid $!"
