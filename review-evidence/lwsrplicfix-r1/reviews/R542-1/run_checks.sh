#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
# Start the documented lwSRP doc/tools checks and test commands concurrently.
# Usage: run_checks.sh <repo> <out-dir> <scratch-dir> <cgreen-prefix>
# Each job writes <out-dir>/<name>.log and, when finished, <out-dir>/<name>.rc.
# Wait with wait_checks.sh <out-dir> <name>...
set -eu
repo=$(cd "$1" && pwd -P)
out=$2
scratch=$3
cg=$4
mkdir -p "$out" "$scratch"
out=$(cd "$out" && pwd -P)
scratch=$(cd "$scratch" && pwd -P)

job() {
    name=$1; shift
    rm -f "$out/$name.rc" "$out/$name.log"
    setsid nohup sh -c '
        name=$1; out=$2; shift 2
        { echo "+ $*"; date -u +%FT%TZ; } > "$out/$name.log"
        rc=0; "$@" >> "$out/$name.log" 2>&1 || rc=$?
        date -u +%FT%TZ >> "$out/$name.log"
        echo "$rc" > "$out/$name.rc"
    ' sh "$name" "$out" "$@" < /dev/null > /dev/null 2>&1 &
}

profile() {
    # profile <OFF|ON> <build-dir>
    m=$1; b=$2
    rm -rf "$b"
    cd "$repo"
    export CMAKE_PREFIX_PATH="$cg" LD_LIBRARY_PATH="$cg/lib"
    echo "== configure"; cmake -S . -B "$b" -DCMAKE_BUILD_TYPE=Debug -DLWSRP_MILAN="$m" || return 10
    echo "== build"; cmake --build "$b" --parallel 4 || return 11
    echo "== ctest"; ctest --test-dir "$b" --output-on-failure || return 12
    echo "== unit_tests"; "$b/unit_tests" || return 13
    echo "== behave"; SHLAN_LIBRARY="$b/libshlan.so" behave || return 14
    echo "== behave --dry-run"; behave --dry-run || return 15
    echo "== profile $m rc=0"
}

if [ "${RUN_CHECKS_PROFILE:-}" ]; then
    profile "$RUN_CHECKS_PROFILE" "$RUN_CHECKS_BUILD"
    exit $?
fi

self=$(cd "$(dirname "$0")" && pwd -P)/$(basename "$0")
export PYTHONDONTWRITEBYTECODE=1
job profile-off env RUN_CHECKS_PROFILE=OFF RUN_CHECKS_BUILD="$scratch/build-off" sh "$self" "$repo" "$out" "$scratch" "$cg"
job profile-on env RUN_CHECKS_PROFILE=ON RUN_CHECKS_BUILD="$scratch/build-on" sh "$self" "$repo" "$out" "$scratch" "$cg"
job check-sentences sh -c "cd '$repo' && python3 doc/tools/check_sentences.py"
job check-references sh -c "cd '$repo' && python3 doc/tools/check_references.py"
job check-references-selftest sh -c "cd '$repo' && python3 doc/tools/check_references.py --self-test"
job check-links-anon sh -c "cd '$repo' && python3 doc/tools/check_links.py"
job check-links-auth sh -c "cd '$repo' && python3 doc/tools/check_links.py --github-auth"
job render-mermaid sh -c "cd '$repo' && python3 doc/tools/render_mermaid.py --output '$scratch/graphs'"
job check-embedded sh -c "cd '$repo' && rm -rf '$scratch/embedded' && python3 tests/check_embedded.py --work-dir '$scratch/embedded'"
job check-freestanding sh -c "cd '$repo' && python3 tests/check_freestanding.py"
job check-freestanding-milan sh -c "cd '$repo' && CC='cc -DLWSRP_MILAN=1' python3 tests/check_freestanding.py"
echo "started"
