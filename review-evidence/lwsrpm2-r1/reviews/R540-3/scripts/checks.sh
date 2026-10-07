#!/bin/bash
# Published commands not covered by profiles.sh, sanitizer suites and documentation checks.
set -u
. "$(dirname "$0")/env.sh"
C=$PKT/receipts/checks; D=$PKT/receipts/doc; mkdir -p "$C" "$D"
cd "$SRC"
B=$PKT/scratch/build-default
( behave --dry-run > "$C/behave-dry.log" 2>&1; echo $? > "$C/behave-dry.rc" ) &
( cc -std=c11 -Isrc/include tests/unit/mrp_pdu_test.c src/core/mrp_pdu.c -xc - -lcgreen -o "$PKT/scratch/mrp_pdu_tests" > "$C/codec-cc.log" 2>&1 <<'C'
#include <cgreen/cgreen.h>
TestSuite *mrp_pdu_suite(void);
int main(void)
{
    return run_test_suite(mrp_pdu_suite(), create_text_reporter());
}
C
  echo $? > "$C/codec-cc.rc"; "$PKT/scratch/mrp_pdu_tests" > "$C/codec-run.log" 2>&1; echo $? > "$C/codec-run.rc" ) &
( python3 tests/check_freestanding.py > "$C/freestanding-default.log" 2>&1; echo $? > "$C/freestanding-default.rc" ) &
( CC="cc -DLWSRP_MILAN=1" python3 tests/check_freestanding.py > "$C/freestanding-milan.log" 2>&1; echo $? > "$C/freestanding-milan.rc" ) &
( rm -rf "$PKT/scratch/embedded"; python3 tests/check_embedded.py --work-dir "$PKT/scratch/embedded" > "$C/embedded.log" 2>&1; echo $? > "$C/embedded.rc" ) &
for m in OFF ON; do
  ( A=$PKT/scratch/asan-$m; rm -rf "$A"; F="-fsanitize=address,undefined -fno-omit-frame-pointer -g"
    cmake -S . -B "$A" -DCMAKE_BUILD_TYPE=Debug -DLWSRP_MILAN=$m "-DCMAKE_C_FLAGS=$F" "-DCMAKE_EXE_LINKER_FLAGS=$F" "-DCMAKE_SHARED_LINKER_FLAGS=$F" > "$C/asan-$m-build.log" 2>&1 &&
    cmake --build "$A" --parallel 4 >> "$C/asan-$m-build.log" 2>&1
    ASAN_OPTIONS=detect_leaks=1 UBSAN_OPTIONS=halt_on_error=1 "$A/unit_tests" > "$C/asan-$m-unit.log" 2>&1; echo $? > "$C/asan-$m-unit.rc" ) &
done
( python3 doc/tools/check_sentences.py > "$D/sentences.log" 2>&1; echo $? > "$D/sentences.rc" ) &
( python3 doc/tools/check_references.py > "$D/references.log" 2>&1; echo $? > "$D/references.rc" ) &
( python3 doc/tools/check_references.py --self-test > "$D/selftest.log" 2>&1; echo $? > "$D/selftest.rc" ) &
( python3 doc/tools/check_links.py --github-auth > "$D/links.log" 2>&1; echo $? > "$D/links.rc" ) &
( rm -rf "$PKT/scratch/graphs"; python3 doc/tools/render_mermaid.py --output "$PKT/scratch/graphs" > "$D/mermaid.log" 2>&1; echo $? > "$D/mermaid.rc" ) &
wait
for f in "$C"/*.rc "$D"/*.rc; do echo "$(basename "$f") $(cat "$f")"; done
