#!/bin/sh
# Usage: validate.sh <clone> <work>. validate.py --jobs 16 with the pinned toolchain; writes <work>/validate.log and .rc
set -u
CLONE=$1; WORK=$2; TOOLS=${TOOLS:-$VALIDATION_TOOLS}
export PATH="$TOOLS/clang-tidy-18/bin:$TOOLS/clang-18/bin:$PATH"
export PKG_CONFIG_PATH="$TOOLS/gtest-1.14.0/lib/pkgconfig" CMAKE_PREFIX_PATH="$TOOLS/gtest-1.14.0" LD_LIBRARY_PATH="$TOOLS/gtest-1.14.0/lib"
mkdir -p "$WORK"; cd "$CLONE" || exit 2
python3 scripts/validate.py --work "$WORK/validate" --jobs 16 > "$WORK/validate.log" 2>&1; echo $? > "$WORK/validate.rc"
