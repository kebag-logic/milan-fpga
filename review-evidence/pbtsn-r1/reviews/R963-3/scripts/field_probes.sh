#!/bin/sh
# Usage: field_probes.sh <clone> <work>. Copies the clone's HEAD files to <work>/tree, builds the pbaem and
# entity tests, then applies each probe below to the AAF comparison in src/pbaem.c alone, rebuilds, runs both
# test binaries and reports KILLED (a test fails, with the failing assertion messages) or SURVIVED.
# Restores the file after each probe. TOOLS: pinned GoogleTest prefix directory (default $VALIDATION_TOOLS).
set -u
CLONE=$1; WORK=$2; TOOLS=${TOOLS:-$VALIDATION_TOOLS}
export PKG_CONFIG_PATH="$TOOLS/gtest-1.14.0/lib/pkgconfig" CMAKE_PREFIX_PATH="$TOOLS/gtest-1.14.0" LD_LIBRARY_PATH="$TOOLS/gtest-1.14.0/lib"
rm -rf "$WORK"; mkdir -p "$WORK/tree"
git -C "$CLONE" archive HEAD | tar -x -C "$WORK/tree"
cd "$WORK/tree" || exit 2
echo "head $(git -C "$CLONE" rev-parse HEAD)"
cmake -S . -B b -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=gcc -DCMAKE_CXX_COMPILER=g++ > "$WORK/configure.log" 2>&1 || { echo configure failed; exit 2; }
cmake --build b -j8 > "$WORK/build.log" 2>&1 || { echo baseline build failed; exit 2; }
run() { r=0; for t in pbaem_tests entity_tests; do f=$(find b -type f -name "$t" | head -1); [ -n "$f" ] || { echo "missing $t"; return 2; }; "$f" > "$WORK/$1.$t.log" 2>&1 || r=1; done; return $r; }
run baseline; echo "baseline (unmodified): rc $? (0 = all pass)"
cp src/pbaem.c "$WORK/pbaem.c.orig"
OLD='	return (format & ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT)) == AAF_BASE'
probe() { # name, mask dropped from both sides
  NEW="	return (format & ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT) & ~($2)) == (AAF_BASE & ~($2))"
  python3 -I - "$OLD" "$NEW" src/pbaem.c <<'PY' || { echo "$1: anchor missing"; return; }
import sys
old, new, path = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(path).read()
assert s.count(old) == 1
open(path, 'w').write(s.replace(old, new))
PY
  if cmake --build b -j8 > "$WORK/$1.build.log" 2>&1; then
    run "$1"; rc=$?
    if [ $rc -eq 1 ]; then
      msgs=$(cat "$WORK/$1".*.log | grep -E '^(an?|the|reserved|twelve|nine|zero|44|24-bit) ' | sed 's/, bit [0-9]*$/, bit N/' | sort | uniq -c | sed 's/^ *//' | tr '\n' ';')
      echo "$1 (drops $2): KILLED by: $msgs"
    else echo "$1 (drops $2): SURVIVED (rc $rc)"; fi
  else echo "$1: BUILD FAILED"; fi
  cp "$WORK/pbaem.c.orig" src/pbaem.c
}
probe ignore-reserved-53-55-together 'UINT64_C(0x7) << 53'
probe ignore-ut-and-reserved-nibble 'UINT64_C(0xf) << 52'
probe ignore-low-reserved-bits-1-11 'UINT64_C(0xffe)'
probe ignore-low-reserved-bits-1-10 'UINT64_C(0x7fe)'
probe ignore-low-reserved-bit-0 'UINT64_C(0x1)'
probe ignore-low-reserved-bit-5 'UINT64_C(0x20)'
probe ignore-bit-depth-low-bit 'UINT64_C(1) << 32'
probe ignore-format-code-high-bit 'UINT64_C(1) << 47'
probe ignore-subtype-bit-57 'UINT64_C(1) << 57'
cmp -s src/pbaem.c "$CLONE/src/pbaem.c" && echo "probe tree restored to head bytes"
