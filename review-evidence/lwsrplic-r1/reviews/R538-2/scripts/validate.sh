#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
# Build and test one exported tree of lwSRP, recording every exit code.
# Usage: CGREEN_PREFIX=<cgreen install prefix> validate.sh <repo> <rev> <workdir> <logdir>
# The tree is exported with git archive, so the source checkout is not touched.
set -u
repo=$1 rev=$2 work=$3 logs=$4
rm -rf "$work"; mkdir -p "$work" "$logs"
git -C "$repo" archive "$rev" | tar -x -C "$work"
cd "$work" || exit 2
export LD_LIBRARY_PATH="$CGREEN_PREFIX/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export PYTHONDONTWRITEBYTECODE=1
step() { name=$1; shift; "$@" > "$logs/$name.log" 2>&1; rc=$?; echo "$name rc=$rc" | tee -a "$logs/rc.txt"; }
: > "$logs/rc.txt"
echo "rev=$(git -C "$repo" rev-parse "$rev") tree=$(git -C "$repo" rev-parse "$rev^{tree}")" > "$logs/rev.txt"
step cfg cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug -DCMAKE_PREFIX_PATH="$CGREEN_PREFIX"
step build cmake --build build --parallel 16
step ctest ctest --test-dir build --output-on-failure
step unit_direct ./build/unit_tests
step behave behave
step behave_dry behave --dry-run
# Object-code comparison input: optimised, no debug info, path-neutral.
mkdir -p objs
for c in src/ports/alloc.c src/ports/timer.c src/core/mrp_mad.c src/core/mrp_pdu.c \
         src/core/switch_ctrl.c src/modules/sim_adapter.c src/modules/mvrp.c \
         src/modules/mmrp.c src/modules/msrp.c tests/features/switch_bindings.c; do
    gcc -std=c11 -O2 -g0 -fPIC -Wall -Wextra -Wpedantic -ffile-prefix-map="$work"=. \
        -Isrc/include -Isrc/modules -Isrc -c "$c" -o "objs/$(basename "$c" .c).o" \
        >> "$logs/objs.log" 2>&1 || echo "objfail $c" >> "$logs/objs.log"
done
(cd objs && sha256sum *.o) > "$logs/objs.sha256"
echo "objs rc=0" >> "$logs/rc.txt"
