# Reviewer environment (sourced). REPO = exact-head clone, PKT = packet directory.
: "${REPO:?set REPO to the exact-head clone}"
: "${PKT:?set PKT to the packet directory}"
: "${TOOLS:?set TOOLS to the pinned tool root (gtest-1.14.0, clang-18, clang-tidy-18)}"
GT=${GT:-$TOOLS/gtest-1.14.0}
export PKG_CONFIG_PATH=$GT/lib/pkgconfig CMAKE_PREFIX_PATH=$GT LD_LIBRARY_PATH=$GT/lib
export SCR=$PKT/scratch RCP=$PKT/receipts
export TMPDIR=$SCR/tmp
# Pinned Clang 18.1.3 and clang-tidy 18.1.3.
export PATH=$TOOLS/clang-18/bin:$TOOLS/clang-tidy-18/bin:$PATH
mkdir -p "$TMPDIR" "$RCP"
# tree COMMIT DEST: export a tracked tree into a fresh directory
tree() { rm -rf "$2"; mkdir -p "$2"; git -C "$REPO" archive "$1" | tar -x -C "$2"; }
