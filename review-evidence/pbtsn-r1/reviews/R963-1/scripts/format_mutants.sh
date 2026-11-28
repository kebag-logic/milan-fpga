#!/bin/sh
# Reviewer mutation probe for pbaem_input_format_supported (AEM-01 "each 48 kHz PCM32 base format").
# Usage: format_mutants.sh CLONE WORKDIR  (needs the pinned GoogleTest on CMAKE_PREFIX_PATH)
set -u
CLONE=$1; WORK=$2
rm -rf "$WORK"; mkdir -p "$WORK/src"
git -C "$CLONE" archive HEAD | tar -x -C "$WORK/src"
cmake -S "$WORK/src" -B "$WORK/build" -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=gcc -DCMAKE_CXX_COMPILER=g++ >/dev/null || exit 2
ORIG='	return (format \& ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT)) == AAF_BASE \&\& count >= 1u \&\& count <= 8u;'
run() {
  name=$1; repl=$2
  cp "$WORK/src/src/pbaem.c" "$WORK/pbaem.c.orig"
  sed -i "s|$ORIG|$repl|" "$WORK/src/src/pbaem.c"
  if cmp -s "$WORK/src/src/pbaem.c" "$WORK/pbaem.c.orig"; then echo "$name: NOT APPLIED"; return; fi
  cmake --build "$WORK/build" -j4 --target pbaem_tests entity_tests >/dev/null 2>&1 || { echo "$name: BUILD FAILED"; cp "$WORK/pbaem.c.orig" "$WORK/src/src/pbaem.c"; return; }
  if "$WORK/build/pbaem_tests" >/dev/null 2>&1 && "$WORK/build/entity_tests" >/dev/null 2>&1; then echo "$name: SURVIVED (every pbaem and entity test passes)"; else echo "$name: KILLED"; fi
  cp "$WORK/pbaem.c.orig" "$WORK/src/src/pbaem.c"
}
cmake --build "$WORK/build" -j4 --target pbaem_tests entity_tests >/dev/null 2>&1 && "$WORK/build/pbaem_tests" >/dev/null && "$WORK/build/entity_tests" >/dev/null && echo "baseline: all pass"
# (a) ignore the AAF format byte (bits 47..40): accepts FLOAT_32BIT, INT_24BIT, INT_16BIT containers
run ignore-format-byte '	return (format \& ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT) \& ~(UINT64_C(0xff) << 40)) == (AAF_BASE \& ~(UINT64_C(0xff) << 40)) \&\& count >= 1u \&\& count <= 8u;'
# (b) ignore samples_per_frame (bits 21..12): accepts 12, 64 or 0 samples per frame
run ignore-samples-per-frame '	return (format \& ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT) \& ~(UINT64_C(0x3ff) << 12)) == (AAF_BASE \& ~(UINT64_C(0x3ff) << 12)) \&\& count >= 1u \&\& count <= 8u;'
# (c) ignore the subtype byte (bits 63..56)
run ignore-subtype '	return (format \& ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT) \& ~(UINT64_C(0xff) << 56)) == (AAF_BASE \& ~(UINT64_C(0xff) << 56)) \&\& count >= 1u \&\& count <= 8u;'
# (d) ignore the reserved low 12 bits
run ignore-reserved-low '	return (format \& ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT) \& ~UINT64_C(0xfff)) == (AAF_BASE \& ~UINT64_C(0xfff)) \&\& count >= 1u \&\& count <= 8u;'
# control: ignore the bit_depth byte (bits 39..32), expected KILLED by "24-bit depth is refused"
run control-ignore-bit-depth '	return (format \& ~(AAF_CHANNEL_MASK << AAF_CHANNEL_SHIFT) \& ~(UINT64_C(0xff) << 32)) == (AAF_BASE \& ~(UINT64_C(0xff) << 32)) \&\& count >= 1u \&\& count <= 8u;'
cmp -s "$WORK/src/src/pbaem.c" "$WORK/pbaem.c.orig" && echo "probe copy restored"
