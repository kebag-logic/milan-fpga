#!/usr/bin/env bash
# R524-3: C11 7.2 conformance probe of sw/firmware/gtest/rv32_include/assert.h.
# Usage: c11_assert_probe.sh <assert.h> <work> <rv32-gcc>
# Host gcc runs the semantics (the header alone on the -I path, own handler);
# the pinned RV32 compiler builds the same unit -std=c11 -pedantic -Werror.
set -u
HDR=$1 WORK=$2 RVCC=$3
rm -rf "$WORK"; mkdir -p "$WORK/inc"; cp "$HDR" "$WORK/inc/assert.h"
cat > "$WORK/unit.c" <<'EOF'
#include <assert.h>
static int calls;
static int bump(void) { return ++calls; }
static void active_once(void) { assert(bump() == 1); }
static_assert(sizeof(int) >= 2, "C11 7.2p3 static_assert");
#define NDEBUG
#include <assert.h>
static void disabled(void) { assert(bump() == 99); (void)(assert(0), 0); }
#undef NDEBUG
#include <assert.h>
static void reenabled(int x) { (void)(assert(x == 2), 0); }
int run(int x) { active_once(); disabled(); reenabled(x); return calls; }
EOF
cat > "$WORK/host_main.c" <<'EOF'
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int run(int x);
_Noreturn void __assert_fail(const char *expr, const char *file, unsigned int line, const char *func) {
    printf("HANDLER expr=[%s] file=[%s] line=%u func=[%s]\n", expr, strrchr(file, '/') ? strrchr(file, '/') + 1 : file, line, func);
    fflush(stdout); _Exit(3);
}
int main(int argc, char **argv) {
    (void)argv;
    int calls = run(argc == 1 ? 2 : 5);
    printf("RETURNED calls=%d\n", calls);
    return calls == 1 ? 0 : 1;
}
EOF
W="-std=c11 -pedantic -Wall -Wextra -Werror"
rc=0
gcc $W -I"$WORK/inc" -c "$WORK/unit.c" -o "$WORK/unit.o" || { echo "FAIL host compile"; exit 1; }
gcc -std=c11 -c "$WORK/host_main.c" -o "$WORK/host_main.o" && gcc "$WORK/unit.o" "$WORK/host_main.o" -o "$WORK/probe" || exit 1
out=$("$WORK/probe"); r=$?
echo "pass-path: rc=$r $out"
[ $r -eq 0 ] && [ "$out" = "RETURNED calls=1" ] && echo "PASS: active assert evaluates once; NDEBUG re-inclusion disables it (no evaluation); undef NDEBUG re-enables" || { echo "FAIL pass-path"; rc=1; }
out=$("$WORK/probe" fail); r=$?
echo "fail-path: rc=$r $out"
[ $r -eq 3 ] && [ "$out" = "HANDLER expr=[x == 2] file=[unit.c] line=11 func=[reenabled]" ] && echo "PASS: failing assert reports text, __FILE__, __LINE__, __func__ to __assert_fail" || { echo "FAIL fail-path"; rc=1; }
gcc -E -P -I"$WORK/inc" "$WORK/unit.c" | grep -n "bump() == 99\|__assert_fail\|_Static_assert" | head
inc=$("$RVCC" -print-file-name=include)
"$RVCC" -march=rv32i -mabi=ilp32 -ffreestanding -fno-stack-protector -Os $W -nostdinc -isystem "$inc" -I"$WORK/inc" -c "$WORK/unit.c" -o "$WORK/unit_rv32.o" && echo "PASS: RV32 pedantic -Werror build of the unit" || { echo "FAIL rv32 compile"; rc=1; }
"${RVCC%gcc}nm" -u "$WORK/unit_rv32.o"
printf '#include <assert.h>\nint f(int x) { assert(x > 0); return x; }\n' > "$WORK/nd.c"
"$RVCC" -march=rv32i -mabi=ilp32 -ffreestanding -fno-stack-protector -Os $W -nostdinc -isystem "$inc" -I"$WORK/inc" -DNDEBUG -c "$WORK/nd.c" -o "$WORK/nd.o" || rc=1
u=$("${RVCC%gcc}nm" -u "$WORK/nd.o"); echo "NDEBUG undefined: [${u}]"
[ -z "$u" ] && echo "PASS: -DNDEBUG object references no handler" || { echo "FAIL ndebug"; rc=1; }
echo "== c11 assert probe rc=$rc =="
exit $rc
