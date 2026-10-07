#!/bin/bash
# Run every command published on the lwSRP pages at an exact head, one log and rc per command.
# Usage: run_page_commands.sh <clone> <export-dir> <cgreen-prefix> <log-dir> <graph-out>
# Build/test commands run in a fresh git-archive export of HEAD; doc checks run in the clone
# (the link checker needs the origin remote). cgreen is made discoverable through env only,
# as doc/tester.md instructs ("Make the unit framework's headers and library discoverable").
set -u
CLONE=$1; EXPORT=$2; DEPS=$3; LOGS=$4; GRAPHS=$5
mkdir -p "$LOGS"
rm -rf "$EXPORT"; mkdir -p "$EXPORT"
git -C "$CLONE" archive HEAD | tar -x -C "$EXPORT"
export CMAKE_PREFIX_PATH=$DEPS CPATH=$DEPS/include LIBRARY_PATH=$DEPS/lib LD_LIBRARY_PATH=$DEPS/lib
run() { # id dir cmd...
  local id=$1 dir=$2; shift 2
  ( cd "$dir" && "$@" ) > "$LOGS/$id.log" 2>&1; local rc=$?
  echo "$rc" > "$LOGS/$id.rc"; printf '%s rc=%s :: %s\n' "$id" "$rc" "$*"
}
# README.md quick start (lines 35-38)
run readme-1 "$EXPORT" cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
run readme-2 "$EXPORT" cmake --build build --parallel 2
run readme-3 "$EXPORT" ctest --test-dir build --output-on-failure
run readme-4 "$EXPORT" behave
# doc/tester.md run the suites (lines 15-20), on a second fresh export
rm -rf "$EXPORT-t"; mkdir -p "$EXPORT-t"; git -C "$CLONE" archive HEAD | tar -x -C "$EXPORT-t"
run tester-1 "$EXPORT-t" cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
run tester-2 "$EXPORT-t" cmake --build build --parallel 2
run tester-3 "$EXPORT-t" ctest --test-dir build --output-on-failure
run tester-4 "$EXPORT-t" ./build/unit_tests
run tester-5 "$EXPORT-t" behave
run tester-6 "$EXPORT-t" behave --dry-run
# doc/tester.md isolated codec run (lines 45-53), verbatim heredoc
( cd "$EXPORT-t" && cc -std=c11 -Isrc/include tests/unit/mrp_pdu_test.c src/core/mrp_pdu.c -xc - -lcgreen -o build/mrp_pdu_tests <<'C'
#include <cgreen/cgreen.h>
TestSuite *mrp_pdu_suite(void);
int main(void)
{
    return run_test_suite(mrp_pdu_suite(), create_text_reporter());
}
C
) > "$LOGS/tester-7.log" 2>&1; echo $? > "$LOGS/tester-7.rc"; echo "tester-7 rc=$(cat "$LOGS/tester-7.rc") :: cc ... heredoc"
run tester-8 "$EXPORT-t" ./build/mrp_pdu_tests
# doc/tools/README.md (lines 14-17)
export DOC_SCRATCH=$GRAPHS
run tools-1 "$CLONE" python3 doc/tools/check_sentences.py
run tools-2 "$CLONE" python3 doc/tools/check_references.py
run tools-3 "$CLONE" python3 doc/tools/check_links.py --github-auth
run tools-4 "$CLONE" python3 doc/tools/render_mermaid.py --output "$DOC_SCRATCH/graphs"
