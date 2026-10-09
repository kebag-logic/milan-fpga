# Reviewer environment: pinned GoogleTest 1.14.0 (built from f8d7d77c) and Ubuntu 24.04 clang 18.1.3 lexer.
# Usage: PACKET=/path/to/packet . env.sh
: "${PACKET:?set PACKET}"
export PATH="$PACKET/scratch/bin:$PATH"
export PKG_CONFIG_PATH="$PACKET/scratch/gtest-install/lib/pkgconfig"
export CMAKE_PREFIX_PATH="$PACKET/scratch/gtest-install"
export PYTHONDONTWRITEBYTECODE=1
# Bank variant: identical 1.14.0 install, but package Cflags use -isystem (as a /usr install behaves).
# Select with: TSN_REVIEW_PC=isystem
if [ "${TSN_REVIEW_PC:-}" = isystem ]; then export PKG_CONFIG_PATH="$PACKET/scratch/pc-isystem"; fi
