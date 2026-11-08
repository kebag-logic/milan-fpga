# SPDX-License-Identifier: MIT
# Reviewer environment (sourced). Set TOOLS (holding gtest-1.14.0, clang-18 and clang-tidy-18),
# CLONE (a clone at the exact head) and PACKET (this packet) before sourcing.
: "${TOOLS:?set TOOLS}" "${CLONE:?set CLONE}" "${PACKET:?set PACKET}"
export PKG_CONFIG_PATH=$TOOLS/gtest-1.14.0/lib/pkgconfig
export CMAKE_PREFIX_PATH=$TOOLS/gtest-1.14.0
export LD_LIBRARY_PATH=$TOOLS/gtest-1.14.0/lib
export PATH=$TOOLS/clang-tidy-18/bin:$TOOLS/clang-18/bin:$PATH
export SCRATCH=$PACKET/scratch
export TMPDIR=$SCRATCH/tmp
mkdir -p "$TMPDIR"
