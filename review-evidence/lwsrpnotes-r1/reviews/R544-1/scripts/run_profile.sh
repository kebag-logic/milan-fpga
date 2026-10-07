#!/usr/bin/env bash
# Build one profile out of tree and run ctest, the unit runner and behave.
# Usage: run_profile.sh <checkout> <OFF|ON> <build-dir> <receipt-dir> <cgreen-prefix>
set -u
SRC=$1; PROFILE=$2; BUILD=$3; OUT=$4; PREFIX=$5
mkdir -p "$OUT"
export CMAKE_PREFIX_PATH="$PREFIX" LD_LIBRARY_PATH="$PREFIX/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export PYTHONDONTWRITEBYTECODE=1
step() {
  local name=$1; shift
  ( cd "$SRC" && "$@" ) > "$OUT/$name.log" 2>&1
  local rc=$?
  echo "$name rc=$rc" | tee -a "$OUT/rc.txt"
  return $rc
}
: > "$OUT/rc.txt"
step configure cmake -S "$SRC" -B "$BUILD" -DCMAKE_BUILD_TYPE=Debug -DLWSRP_MILAN="$PROFILE"
step build cmake --build "$BUILD" --parallel 2
step ctest ctest --test-dir "$BUILD" --output-on-failure
step unit_tests "$BUILD/unit_tests"
step behave env SHLAN_LIBRARY="$BUILD/libshlan.so" behave
[ "$PROFILE" = OFF ] && step behave_dry_run behave --dry-run
exit 0
