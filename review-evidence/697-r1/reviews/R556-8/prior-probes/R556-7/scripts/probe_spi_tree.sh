#!/bin/sh
# Reviewer probe: an honest-contributor change that uses a public GoogleTest assertion from
# gtest/gtest-spi.h inside an existing traced test. The documented regeneration (traceability and
# test inventory --write) is applied, as CONTRIBUTING/VERIFICATION require after a test change.
# Then every source gate runs and the affected test is built and executed with GoogleTest 1.14.0.
# usage: probe_spi_tree.sh HEAD_CLONE HEAD_SHA WORK   (env.sh loaded)
set -u
src=$1; sha=$2; work=$3
rm -rf "$work"; mkdir -p "$work"; t=$work/tree
git clone -q --no-hardlinks "$src" "$t" && git -C "$t" checkout -q --detach "$sha" || exit 2
cd "$t"
python3 - tests/test_port.cpp <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
s = s.replace('#include <gtest/gtest.h>\n', '#include <gtest/gtest.h>\n#include <gtest/gtest-spi.h>\n', 1)
s = s.replace('    EXPECT_FALSE(example_adp_take_frame(&p, frame));\n}',
              '    EXPECT_FALSE(example_adp_take_frame(&p, frame));\n'
              '    EXPECT_NONFATAL_FAILURE(EXPECT_EQ(1, 2) << "planted inner failure", "planted inner failure");\n}', 1)
open(p, 'w').write(s)
PY
python3 scripts/traceability.py --write --build "$work/reg" --jobs 16 > "$work/regen-traceability.log" 2>&1; echo "regenerate traceability rc=$?"
python3 scripts/test_inventory.py --write --build "$work/reg" --jobs 16 > "$work/regen-inventory.log" 2>&1; echo "regenerate test inventory rc=$?"
git diff --stat
run() { name=$1; shift; "$@" > "$work/$name.log" 2>&1; echo "$name rc=$? ($(tail -1 "$work/$name.log" | cut -c1-110))"; }
run comments python3 scripts/check_comments.py
run needles python3 scripts/needle_audit.py
run test-inventory python3 scripts/test_inventory.py --build "$work/reg" --jobs 16
run traceability python3 scripts/traceability.py --build "$work/reg" --jobs 16
run conditionals python3 scripts/check_conditionals.py --work "$work/cond" --jobs 16
run boundary python3 scripts/check_boundary.py --work "$work/bnd" --jobs 16
run license python3 scripts/check_license.py
run port-contracts python3 scripts/check_port_contracts.py
run configure cmake -S . -B "$work/build" -DCMAKE_BUILD_TYPE=Debug
run build cmake --build "$work/build" -j16 --target port_tests
run port_tests "$work/build/port_tests"
