#!/bin/sh
# Run a command with the scratch GoogleTest 1.14.0 prefix and no ambient include or library paths.
# usage: isolated.sh PACKET NAME CWD CMD...  -> PACKET/receipts/run/NAME.log and NAME.rc
P="$1"; N="$2"; D="$3"; shift 3
mkdir -p "$P/receipts/run"
unset CPATH C_INCLUDE_PATH CPLUS_INCLUDE_PATH LIBRARY_PATH PKG_CONFIG_ALLOW_SYSTEM_CFLAGS PKG_CONFIG_ALLOW_SYSTEM_LIBS
export PKG_CONFIG_PATH="$P/scratch/sdk/gtest/lib/pkgconfig" CMAKE_PREFIX_PATH="$P/scratch/sdk/gtest" TSN_CLANG="$P/scratch/bin/clang-18" PYTHONDONTWRITEBYTECODE=1
cd "$D" || exit 2
start=$(date +%s)
"$@" > "$P/receipts/run/$N.log" 2>&1
rc=$?
echo "$rc" > "$P/receipts/run/$N.rc"
echo "elapsed_s $(( $(date +%s) - start ))" >> "$P/receipts/run/$N.log"
exit $rc
