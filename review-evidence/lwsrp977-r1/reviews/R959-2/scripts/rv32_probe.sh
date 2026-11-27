#!/bin/bash
# rv32_probe.sh <repo> <base-rev> <head-rev> <work>
# Compile-only RV32I probe (no link, no libc): the freestanding sources of both
# revisions with clang's riscv32 target and a stub <string.h>. Default objects
# are compared byte for byte; the head is also compiled, warnings as errors,
# with the scale options, the end-station switches, and both together.
set -u
repo=$1; base=$2; head=$3; work=$4
rm -rf "$work"; mkdir -p "$work/stub"
cat > "$work/stub/string.h" <<'EOF'
#ifndef RV32_PROBE_STRING_H
#define RV32_PROBE_STRING_H
#include <stddef.h>
void *memcpy(void *restrict, const void *restrict, size_t);
void *memmove(void *, const void *, size_t);
void *memset(void *, int, size_t);
int memcmp(const void *, const void *, size_t);
size_t strlen(const char *);
#endif
EOF
for rev in base head; do
  sha=$([ $rev = base ] && echo "$base" || echo "$head")
  mkdir -p "$work/$rev"; git -C "$repo" archive "$sha" src | tar -x -C "$work/$rev"
done
SOURCES="src/core/mrp_mad.c src/core/mrp_pdu.c src/core/switch.c src/ports/timer.c src/modules/mmrp.c src/modules/mvrp.c src/modules/msrp.c"
CC="clang --target=riscv32-unknown-elf -march=rv32i -mabi=ilp32 -ffreestanding -nostdlibinc -isystem $work/stub"
W="-std=c11 -Wall -Wextra -Wpedantic -Werror -Isrc/include -Isrc"
same=0; total=0; fail=0
for opt in -O0 -O2 -Os "-Os -DLWSRP_MILAN=1"; do
  for s in $SOURCES; do
    for rev in base head; do
      o="$work/obj/${opt// /_}/$rev/${s//\//_}.o"; mkdir -p "$(dirname "$o")"
      (cd "$work/$rev" && $CC $W $opt -c "$s" -o "$o") || { echo "BUILD-FAIL $rev $opt $s"; fail=$((fail+1)); }
    done
    a="$work/obj/${opt// /_}/base/${s//\//_}.o"; b="$work/obj/${opt// /_}/head/${s//\//_}.o"
    total=$((total+1)); if cmp -s "$a" "$b"; then same=$((same+1)); r=SAME; else r=DIFF; fi
    echo "$r rv32i [$opt] $s"
  done
done
echo "rv32i default objects byte-identical: $same of $total"
SCALE="-DLWSRP_TIMER_SLOTS=64u -DLWSRP_ATTR_BUCKETS=16u -DLWSRP_TX_MERGE=1"
ES="-DLWSRP_ONE_PORT_MAP=1 -DLWSRP_LEAN_VALIDATE=1 -DLWSRP_RAPID_REPLACE=1 -DLWSRP_LEAN_COPY=1 -DLWSRP_LEAN_TX=1"
for set in "scale|$SCALE" "end-station|$ES" "scale+end-station|$SCALE $ES" "scale+end-station+milan|$SCALE $ES -DLWSRP_MILAN=1"; do
  label=${set%%|*}; flags=${set#*|}; n=0
  for s in $SOURCES; do
    (cd "$work/head" && $CC $W -Os $flags -c "$s" -o "$work/opt.o") && n=$((n+1)) || { echo "BUILD-FAIL head $label $s"; fail=$((fail+1)); }
  done
  echo "rv32i head $label: $n of 7 sources compiled, -Werror"
done
echo "build failures: $fail"
[ "$same" -eq "$total" ] && [ "$fail" -eq 0 ]
