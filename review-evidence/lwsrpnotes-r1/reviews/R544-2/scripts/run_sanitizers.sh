#!/usr/bin/env bash
# Build the exact head with ASan/UBSan in both profiles and run the unit runner.
# Usage: run_sanitizers.sh CHECKOUT CGREEN_PREFIX OUT
set -u
SRC=$(cd "$1" && pwd); PREFIX=$(cd "$2" && pwd); OUT=$3
rm -rf "$OUT"; mkdir -p "$OUT/src"
git -C "$SRC" archive HEAD | tar -x -C "$OUT/src"
export LD_LIBRARY_PATH="$PREFIX/lib" ASAN_OPTIONS=detect_leaks=1 UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1
F="-fsanitize=address,undefined -fno-omit-frame-pointer -fno-sanitize-recover=all"
for m in OFF ON; do
  ( cmake -S "$OUT/src" -B "$OUT/b-$m" -DCMAKE_BUILD_TYPE=Debug -DCMAKE_PREFIX_PATH="$PREFIX" -DLWSRP_MILAN=$m \
      -DCMAKE_C_FLAGS="$F" -DCMAKE_EXE_LINKER_FLAGS="$F" -DCMAKE_SHARED_LINKER_FLAGS="$F" &&
    cmake --build "$OUT/b-$m" --parallel 4 && "$OUT/b-$m/unit_tests" ) > "$OUT/san-$m.log" 2>&1; echo $? > "$OUT/san-$m.rc" &
done
wait
for m in OFF ON; do echo "$m rc=$(cat "$OUT/san-$m.rc") $(grep -E 'Completed|ERROR: |runtime error' "$OUT/san-$m.log" | head -3 | tr '\n' ' ')"; done
