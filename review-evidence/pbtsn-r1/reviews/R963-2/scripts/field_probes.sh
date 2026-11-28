#!/bin/sh
# Usage: field_probes.sh <clone> <work>. Copies the clone's tracked files to <work>/tree, builds the
# pbaem and entity tests once, then applies each probe below to src/pbaem.c alone, rebuilds, runs both
# test binaries and reports KILLED (a test fails) or SURVIVED. Restores the file after each probe.
set -u
CLONE=$1; WORK=$2
. "$(dirname "$0")/env.sh"
rm -rf "$WORK"; mkdir -p "$WORK/tree"
git -C "$CLONE" archive HEAD | tar -x -C "$WORK/tree"
cd "$WORK/tree" || exit 2
cmake -S . -B b -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=gcc -DCMAKE_CXX_COMPILER=g++ > "$WORK/configure.log" 2>&1 || { echo configure failed; exit 2; }
cmake --build b -j4 > "$WORK/build.log" 2>&1 || { echo baseline build failed; exit 2; }
run() { for t in pbaem_tests entity_tests; do f=$(find b -type f -name "$t" | head -1); [ -n "$f" ] || { echo "missing $t"; return 2; }; "$f" > "$WORK/$1.$t.log" 2>&1 || return 1; done; return 0; }
run baseline; echo "baseline (unmodified): rc $? (0 = all pass)"
cp src/pbaem.c "$WORK/pbaem.c.orig"
OLD='	return (format & ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT)) == AAF_BASE'
probe() { # name, replacement line
  python3 -I - "$OLD" "$2" src/pbaem.c <<'PY' || { echo "$1: anchor missing"; return; }
import sys
old, new, path = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(path).read()
assert s.count(old) == 1
open(path, 'w').write(s.replace(old, new))
PY
  if cmake --build b -j4 > "$WORK/$1.build.log" 2>&1; then run "$1"; rc=$?; [ $rc -eq 1 ] && echo "$1: KILLED" || echo "$1: SURVIVED (rc $rc)"; else echo "$1: BUILD FAILED"; fi
  cp "$WORK/pbaem.c.orig" src/pbaem.c
}
probe ignore-bit-depth '	return (format & ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT) & ~(UINT64_C(0xff) << 32)) == (AAF_BASE & ~(UINT64_C(0xff) << 32))'
probe ignore-ut-and-reserved-nibble '	return (format & ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT) & ~(UINT64_C(0xf) << 52)) == (AAF_BASE & ~(UINT64_C(0xf) << 52))'
probe ignore-ut-bit-only '	return (format & ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT) & ~(UINT64_C(1) << 52)) == (AAF_BASE & ~(UINT64_C(1) << 52))'
probe ignore-reserved-53-55 '	return (format & ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT) & ~(UINT64_C(0x7) << 53)) == (AAF_BASE & ~(UINT64_C(0x7) << 53))'
probe ignore-reserved-high-low-bits '	return (format & ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT) & ~UINT64_C(0xffe)) == (AAF_BASE & ~UINT64_C(0xffe))'
cmp -s src/pbaem.c "$CLONE/src/pbaem.c" && echo "probe tree restored to head bytes"
