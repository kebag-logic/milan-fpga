#!/usr/bin/env bash
# Execute every published shell command from README.md and doc/tester.md in an
# exported snapshot of HEAD. Usage: run-suites.sh CHECKOUT SNAPDIR OUTDIR DEPS_PREFIX
set -u
repo=$1; snap=$2; out=$3; deps=$4; mkdir -p "$out"
rm -rf "$snap"; mkdir -p "$snap"
git -C "$repo" archive HEAD | tar -x -C "$snap"
export CPATH="$deps/include" LIBRARY_PATH="$deps/lib" LD_LIBRARY_PATH="$deps/lib" CMAKE_PREFIX_PATH="$deps"
cd "$snap" || exit 2
n=0
run() { n=$((n+1)); name=$(printf '%02d-%s' $n "$1"); shift; echo "\$ $*" >"$out/$name.log"; bash -c "$*" >>"$out/$name.log" 2>&1; echo $? >"$out/$name.rc"; echo "$name rc=$(cat "$out/$name.rc")"; }
# README.md quick start
run readme-configure 'cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug'
run readme-build 'cmake --build build --parallel 2'
run readme-ctest 'ctest --test-dir build --output-on-failure'
run readme-behave 'behave'
# doc/tester.md run the suites (fresh build dir)
rm -rf build
run tester-configure 'cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug'
run tester-build 'cmake --build build --parallel 2'
run tester-ctest 'ctest --test-dir build --output-on-failure'
run tester-unit './build/unit_tests'
run tester-behave 'behave'
run tester-behave-dry 'behave --dry-run'
# doc/tester.md isolated codec run (verbatim heredoc)
run tester-isolated-compile "cc -std=c11 -Isrc/include tests/unit/mrp_pdu_test.c src/core/mrp_pdu.c -xc - -lcgreen -o build/mrp_pdu_tests <<'C'
#include <cgreen/cgreen.h>
TestSuite *mrp_pdu_suite(void);
int main(void)
{
    return run_test_suite(mrp_pdu_suite(), create_text_reporter());
}
C"
run tester-isolated-run './build/mrp_pdu_tests'
