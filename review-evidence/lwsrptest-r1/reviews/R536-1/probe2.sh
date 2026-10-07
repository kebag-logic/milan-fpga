#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Reviewer probes, part 2: exported symbols, Zephyr source list, strict
# warnings, sanitizers, repeatability.
# Usage: probe2.sh <lwsrp-clone> <cgreen-prefix> <work-dir> <receipt-dir>
# Requires probe.sh to have built <work-dir>/p0_head and <work-dir>/p1_base.
set -u
SRC=$1; CG=$2; WORK=$3; OUT=$4
HEAD=e4f9995b791489c53b8ccb8a8dc09ec508e32e6b
BASE=19f5796b63652eb1151906de73cb827d4980a53f
mkdir -p "$WORK" "$OUT"
copy() { rm -rf "$WORK/$1"; mkdir -p "$WORK/$1"; git -C "$SRC" archive "$2" | tar -x -C "$WORK/$1"; }

# 1. Dynamic symbol export difference, base -> head.
nm -D --defined-only "$WORK/p1_base/build/libshlan.so" | awk '{print $3}' | sort > "$WORK/syms-base.txt"
nm -D --defined-only "$WORK/p0_head/build/libshlan.so" | awk '{print $3}' | sort > "$WORK/syms-head.txt"
diff "$WORK/syms-base.txt" "$WORK/syms-head.txt" > "$OUT/exported-symbols.diff"
echo "symbols_diff_rc=$?" > "$OUT/probe2-rc.txt"

# 2. Zephyr module source list (stubbed Zephyr CMake functions, no cgreen on path).
zep() { # name rev
    copy "$1" "$2"
    mkdir -p "$WORK/$1-zstub"
    cat > "$WORK/$1-zstub/CMakeLists.txt" <<EOF
cmake_minimum_required(VERSION 3.20)
project(zstub C)
function(zephyr_library_named n)
  set_property(GLOBAL APPEND PROPERTY ZLOG "library:\${n}")
endfunction()
function(zephyr_library_sources)
  foreach(s \${ARGN})
    set_property(GLOBAL APPEND PROPERTY ZLOG "source:\${s}")
  endforeach()
endfunction()
function(zephyr_include_directories)
endfunction()
function(zephyr_library_include_directories)
endfunction()
set(ZEPHYR_BASE /zephyr-stub)
set(CONFIG_LWSRP y)
add_subdirectory($WORK/$1 lwsrp)
get_property(z GLOBAL PROPERTY ZLOG)
foreach(l \${z})
  message(STATUS "ZLOG \${l}")
endforeach()
get_property(t DIRECTORY $WORK/$1 PROPERTY BUILDSYSTEM_TARGETS)
message(STATUS "ZLOG cmake-targets:\${t}")
EOF
    cmake -S "$WORK/$1-zstub" -B "$WORK/$1-zstub/build" > "$WORK/$1-zstub.log" 2>&1
    echo "$1_configure_rc=$?" >> "$OUT/probe2-rc.txt"
    grep 'ZLOG' "$WORK/$1-zstub.log" | sed 's/^-- ZLOG //' > "$OUT/$1-zephyr-sources.txt"
}
zep z_head "$HEAD"
zep z_base "$BASE"
diff "$OUT/z_base-zephyr-sources.txt" "$OUT/z_head-zephyr-sources.txt" > "$OUT/zephyr-sources.diff"
echo "zephyr_sources_diff_rc=$?" >> "$OUT/probe2-rc.txt"

# 3. Strict-warning builds of head and base with gcc and clang.
strict() { # name rev compiler
    copy "$1" "$2"
    ( cd "$WORK/$1" && cmake -B build -DCMAKE_C_COMPILER="$3" -DCMAKE_PREFIX_PATH="$CG" \
        "-DCMAKE_C_FLAGS=-Wmissing-prototypes -Wstrict-prototypes -Wshadow -Wconversion" ) > "$WORK/$1.configure.log" 2>&1
    cmake --build "$WORK/$1/build" -j4 > "$WORK/$1.build.log" 2>&1
    echo "$1_build_rc=$?" >> "$OUT/probe2-rc.txt"
    grep -E 'warning:' "$WORK/$1.build.log" | sed "s#$WORK/$1/##" | sort -u > "$OUT/$1-warnings.txt"
}
strict s_head_gcc "$HEAD" gcc &
strict s_head_clang "$HEAD" clang &
strict s_base_gcc "$BASE" gcc &
strict s_base_clang "$BASE" clang &
wait
for c in gcc clang; do
    grep -E 'tests/(features/switch_bindings|unit/main)\.c' "$OUT/s_head_$c-warnings.txt" > "$OUT/s_head_$c-new-file-warnings.txt"
    echo "s_head_${c}_new_file_warning_lines=$(wc -l < "$OUT/s_head_$c-new-file-warnings.txt")" >> "$OUT/probe2-rc.txt"
done

# 4. Sanitized head build: unit runner with leak detection, behave with ASan preloaded.
copy san_head "$HEAD"
( cd "$WORK/san_head" && cmake -B build -DCMAKE_BUILD_TYPE=Debug -DCMAKE_PREFIX_PATH="$CG" \
    "-DCMAKE_C_FLAGS=-fsanitize=address,undefined -fno-sanitize-recover=all -fno-omit-frame-pointer" \
    "-DCMAKE_SHARED_LINKER_FLAGS=-fsanitize=address,undefined" "-DCMAKE_EXE_LINKER_FLAGS=-fsanitize=address,undefined" ) > "$WORK/san_head.configure.log" 2>&1
cmake --build "$WORK/san_head/build" -j8 > "$WORK/san_head.build.log" 2>&1
echo "san_build_rc=$?" >> "$OUT/probe2-rc.txt"
( cd "$WORK/san_head" && LD_LIBRARY_PATH="$CG/lib" ASAN_OPTIONS=detect_leaks=1 ./build/unit_tests ) > "$OUT/san-unit.log" 2>&1
echo "san_unit_rc=$?" >> "$OUT/probe2-rc.txt"
ASAN_RT=$(gcc -print-file-name=libasan.so)
( cd "$WORK/san_head" && LD_PRELOAD="$ASAN_RT" ASAN_OPTIONS=detect_leaks=0 behave --no-color ) > "$OUT/san-behave.log" 2>&1
echo "san_behave_rc=$?" >> "$OUT/probe2-rc.txt"

# 5. Repeatability: three more ctest and behave runs on the reviewed head build.
for i in 1 2 3; do
    ( cd "$WORK/p0_head" && LD_LIBRARY_PATH="$CG/lib" ctest --test-dir build --output-on-failure ) > "$OUT/repeat-ctest-$i.log" 2>&1
    echo "repeat_ctest_${i}_rc=$?" >> "$OUT/probe2-rc.txt"
    ( cd "$WORK/p0_head" && behave --no-color ) > "$OUT/repeat-behave-$i.log" 2>&1
    echo "repeat_behave_${i}_rc=$?" >> "$OUT/probe2-rc.txt"
done
