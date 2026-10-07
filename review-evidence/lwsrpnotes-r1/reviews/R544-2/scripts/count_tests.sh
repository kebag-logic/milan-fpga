#!/usr/bin/env bash
# Count executed unit tests per profile: export the exact head into scratch,
# wrap the text reporter's start_test, and run both profiles in parallel.
# Usage: count_tests.sh CHECKOUT CGREEN_PREFIX OUT [REV]
set -u
SRC=$(cd "$1" && pwd); PREFIX=$(cd "$2" && pwd); OUT=$3
rm -rf "$OUT"; mkdir -p "$OUT/src"
git -C "$SRC" archive "${4:-HEAD}" | tar -x -C "$OUT/src"
python3 - "$OUT/src/tests/unit/main.c" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
s = s.replace("int main(void)\n{", "#include <stdio.h>\nstatic unsigned tests;\nstatic void (*inner)(TestReporter *, const char *);\n"
              "static void counted(TestReporter *r, const char *n) { ++tests; inner(r, n); }\nint main(void)\n{", 1)
s = s.replace("    int result = run_test_suite(suite, reporter);",
              "    inner = reporter->start_test; reporter->start_test = counted;\n"
              "    int result = run_test_suite(suite, reporter);\n    printf(\"COUNTED TESTS: %u\\n\", tests);", 1)
open(p, "w").write(s)
PY
export LD_LIBRARY_PATH="$PREFIX/lib"
for m in OFF ON; do
  ( cmake -S "$OUT/src" -B "$OUT/b-$m" -DCMAKE_BUILD_TYPE=Debug -DCMAKE_PREFIX_PATH="$PREFIX" -DLWSRP_MILAN=$m &&
    cmake --build "$OUT/b-$m" --parallel 4 && "$OUT/b-$m/unit_tests" ) > "$OUT/count-$m.log" 2>&1; echo $? > "$OUT/count-$m.rc" &
done
wait
for m in OFF ON; do echo "$m rc=$(cat "$OUT/count-$m.rc") $(grep -E 'COUNTED|Completed' "$OUT/count-$m.log" | tr '\n' ' ')"; done
