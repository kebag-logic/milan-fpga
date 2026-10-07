#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
# Link the switch probe against the sources named in the embedded module branch
# of the root build definition. Usage: module_link.sh <source-tree> <probe.c> <output>
set -u
SRC=$1; PROBE=$2; OUT=$3
LIST=$(sed -n '/zephyr_library_sources(/,/)/p' "$SRC/CMakeLists.txt" | grep -E '^\s*src/' | sed "s|^\s*|$SRC/|")
echo "module sources:"; echo "$LIST"
cc -std=c11 -I"$SRC/src/include" -I"$SRC/src" $LIST "$PROBE" -o "$OUT"
rc=$?; echo "link rc=$rc"; exit $rc
