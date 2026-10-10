#!/usr/bin/env bash
# Reviewer gate bank for lwSRP PR #18 at one exact head.
# Usage: run_gates.sh <lwSRP checkout> <unit framework prefix> <scratch dir> <receipt dir>
# Independent gates run concurrently; each has its own log and rc file.
set -u
SRC=$(readlink -f "$1"); PREFIX=$(readlink -f "$2"); SCR=$(readlink -m "$3"); OUT=$(readlink -m "$4")
mkdir -p "$SCR" "$OUT"
export CMAKE_PREFIX_PATH="$PREFIX" LD_LIBRARY_PATH="$PREFIX/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export CPATH="$PREFIX/include" LIBRARY_PATH="$PREFIX/lib"
git -C "$SRC" rev-parse HEAD > "$OUT/head.txt"

gate() { # name, command...
  local name=$1; shift
  ( cd "$SRC" && "$@" ) > "$OUT/$name.log" 2>&1
  echo $? > "$OUT/$name.rc"
}

profile() { # OFF|ON
  local p=$1 b="$SCR/build-$1"
  gate "configure-$p" cmake -S "$SRC" -B "$b" -DCMAKE_BUILD_TYPE=Debug -DLWSRP_MILAN=$p || return
  gate "build-$p" cmake --build "$b" --parallel 4
  gate "ctest-$p" ctest --test-dir "$b" --output-on-failure
  gate "unit-$p" "$b/unit_tests"
  gate "behave-$p" env SHLAN_LIBRARY="$b/libshlan.so" behave
}

profile OFF &
profile ON &
gate behave-dryrun behave --dry-run &
gate equivalence-OFF python3 tests/check_equivalence.py --work-dir "$SCR/eq-OFF" --prefix "$PREFIX" --milan OFF &
gate equivalence-ON python3 tests/check_equivalence.py --work-dir "$SCR/eq-ON" --prefix "$PREFIX" --milan ON &
gate reversals-OFF python3 tests/check_reversals.py --work-dir "$SCR/rev-OFF" --prefix "$PREFIX" --milan OFF &
gate reversals-ON python3 tests/check_reversals.py --work-dir "$SCR/rev-ON" --prefix "$PREFIX" --milan ON &
gate freestanding-OFF python3 tests/check_freestanding.py &
gate freestanding-ON env CC="cc -DLWSRP_MILAN=1" python3 tests/check_freestanding.py &
gate embedded python3 tests/check_embedded.py --work-dir "$SCR/embedded" &
gate doc-sentences python3 doc/tools/check_sentences.py &
gate doc-references python3 doc/tools/check_references.py &
gate doc-references-selftest python3 doc/tools/check_references.py --self-test &
gate doc-links-local python3 doc/tools/check_links.py --local-only &
gate strict-gcc gcc -O2 -std=c11 -Wall -Wextra -Wpedantic -Werror -Isrc/include -Isrc -c src/core/mrp_mad.c -o "$SCR/strict-gcc.o" &
gate strict-clang clang -O2 -std=c11 -Wall -Wextra -Wpedantic -Werror -Isrc/include -Isrc -c src/core/mrp_mad.c -o "$SCR/strict-clang.o" &
wait
for f in "$OUT"/*.rc; do printf '%s %s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done | tee "$OUT/SUMMARY.txt"
