#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Run the repository's documented checks at the reviewed head, concurrently.
# Usage: run_checks.sh <checkout> <scratch> <receipts> <cgreen-prefix>
# Each check writes <name>.log and <name>.rc under <receipts>/head.
set -u
SRC=$(cd "$1" && pwd); SCR=$2; OUT=$3/head; CG=$4
mkdir -p "$OUT" "$SCR"
export CMAKE_PREFIX_PATH="$CG" LD_LIBRARY_PATH="$CG/lib" CPATH="$CG/include" LIBRARY_PATH="$CG/lib"
export PYTHONDONTWRITEBYTECODE=1
run() { local n=$1; shift; ( cd "$SRC" && "$@" ) > "$OUT/$n.log" 2>&1; echo $? > "$OUT/$n.rc"; }
profile() { # $1 = OFF|ON
  local p=$1 b="$SCR/build-$1" n="profile-$1"
  { rm -rf "$b"
    echo "== configure"; cmake -S . -B "$b" -DCMAKE_BUILD_TYPE=Debug -DLWSRP_MILAN=$p; echo "configure rc=$?"
    echo "== build"; cmake --build "$b" --parallel 4; echo "build rc=$?"
    echo "== ctest"; ctest --test-dir "$b" --output-on-failure; echo "ctest rc=$?"
    echo "== unit_tests"; "$b/unit_tests"; echo "unit_tests rc=$?"
    echo "== behave"; SHLAN_LIBRARY="$b/libshlan.so" behave; echo "behave rc=$?"
    echo "== behave --dry-run"; behave --dry-run; echo "behave-dry rc=$?"
  } 2>&1
}
codec() {
  mkdir -p "$SCR/codec"
  cc -std=c11 -Isrc/include tests/unit/mrp_pdu_test.c src/core/mrp_pdu.c -xc - -lcgreen -o "$SCR/codec/mrp_pdu_tests" <<'C'
#include <cgreen/cgreen.h>
TestSuite *mrp_pdu_suite(void);
int main(void)
{
    return run_test_suite(mrp_pdu_suite(), create_text_reporter());
}
C
  local rc=$?; echo "compile rc=$rc"; [ $rc -eq 0 ] || return $rc
  "$SCR/codec/mrp_pdu_tests"
}
export -f profile codec; export SCR
run check-sentences python3 doc/tools/check_sentences.py &
run check-references python3 doc/tools/check_references.py &
run check-references-selftest python3 doc/tools/check_references.py --self-test &
run check-links-anon python3 doc/tools/check_links.py &
run render-mermaid python3 doc/tools/render_mermaid.py --output "$SCR/graphs" &
run profile-OFF bash -c 'profile OFF; exit 0' &
run profile-ON bash -c 'profile ON; exit 0' &
run codec-isolated bash -c codec &
run check-freestanding python3 tests/check_freestanding.py &
run check-freestanding-milan env CC="cc -DLWSRP_MILAN=1" python3 tests/check_freestanding.py &
run check-embedded python3 tests/check_embedded.py --work-dir "$SCR/embedded" &
run check-reversals-OFF python3 tests/check_reversals.py --work-dir "$SCR/rev-off" --prefix "$CG" &
run check-reversals-ON python3 tests/check_reversals.py --work-dir "$SCR/rev-on" --prefix "$CG" --milan ON &
wait
# Profile sub-step return codes are recorded inside the profile logs.
for f in "$OUT"/*.rc; do printf '%s %s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done
grep -h ' rc=' "$OUT"/profile-*.log
