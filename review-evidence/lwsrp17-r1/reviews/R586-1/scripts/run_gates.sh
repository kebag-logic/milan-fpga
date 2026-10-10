#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Reviewer gate bank for lwSRP PR #18 at one exact head.
# Usage: run_gates.sh <lwsrp-checkout> <cgreen-prefix> <scratch-dir> <receipt-dir>
# Runs independent gates concurrently; each writes <name>.log and <name>.rc.
set -u
SRC=$(cd "$1" && pwd); PREFIX=$(cd "$2" && pwd); SCR=$3; OUT=$4
mkdir -p "$SCR" "$OUT"
export LD_LIBRARY_PATH="$PREFIX/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export CMAKE_PREFIX_PATH="$PREFIX"

gate() { # name, command...
    local name=$1; shift
    ( cd "$SRC" && "$@" ) > "$OUT/$name.log" 2>&1
    echo $? > "$OUT/$name.rc"
}

profile() { # OFF|ON
    local m=$1 b="$SCR/build-$1"
    rm -rf "$b"
    gate "configure-$m" cmake -S "$SRC" -B "$b" -DCMAKE_BUILD_TYPE=Debug -DLWSRP_MILAN="$m" || return
    gate "build-$m" cmake --build "$b" --parallel 4
    grep -ci "warning" "$OUT/build-$m.log" > "$OUT/build-$m.warnings" || true
    gate "ctest-$m" ctest --test-dir "$b" --output-on-failure
    gate "unit-$m" "$b/unit_tests"
    gate "behave-$m" env SHLAN_LIBRARY="$b/libshlan.so" behave
}

profile OFF &
profile ON &
gate equivalence-OFF python3 tests/check_equivalence.py --work-dir "$SCR/eq-OFF" --prefix "$PREFIX" &
gate equivalence-ON python3 tests/check_equivalence.py --work-dir "$SCR/eq-ON" --prefix "$PREFIX" --milan ON &
gate reversals-OFF python3 tests/check_reversals.py --work-dir "$SCR/rev-OFF" --prefix "$PREFIX" &
gate reversals-ON python3 tests/check_reversals.py --work-dir "$SCR/rev-ON" --prefix "$PREFIX" --milan ON &
gate embedded python3 tests/check_embedded.py --work-dir "$SCR/embedded" &
gate freestanding-OFF python3 tests/check_freestanding.py &
gate freestanding-ON env CC="cc -DLWSRP_MILAN=1" python3 tests/check_freestanding.py &
gate behave-dry-run behave --dry-run &
gate doc-sentences python3 doc/tools/check_sentences.py &
gate doc-references python3 doc/tools/check_references.py &
gate doc-references-selftest python3 doc/tools/check_references.py --self-test &
gate doc-links-local python3 doc/tools/check_links.py --local-only &
gate strict-gcc gcc -O2 -std=c11 -Wall -Wextra -Wpedantic -Werror -Isrc/include -Isrc -c src/core/mrp_mad.c -o "$SCR/mad-gcc.o" &
gate strict-clang clang -O2 -std=c11 -Wall -Wextra -Wpedantic -Werror -Isrc/include -Isrc -c src/core/mrp_mad.c -o "$SCR/mad-clang.o" &
wait
for f in "$OUT"/*.rc; do printf '%s %s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done
