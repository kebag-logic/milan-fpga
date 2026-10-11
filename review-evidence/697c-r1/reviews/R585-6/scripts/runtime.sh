#!/bin/bash
# runtime.sh OUT : the size fixture's bare-metal runtime archives, with the same sources and flags as
# sw/firmware/ctrl/test/ctrl_image_runtime.py plus -fno-stack-protector (needed by --with-aecp's __umoddi3).
# Sources: picolibc 1.8.10 (newlib/), litex-hub pythondata-software-compiler_rt master, enjoy-digital litex master.
set -euo pipefail
P=$REVIEWS/697c-r585-6-packet; . $P/scripts/env.sh
OUT=$1; mkdir -p $OUT; D=$P/scratch/dl
PICO=$D/picolibc/picolibc-1.8.10/newlib
CRT=$D/crt/pythondata-software-compiler_rt-master/pythondata_software_compiler_rt/data/lib/builtins
LITE=$D/litex/litex-master/litex/soc/software
CC=$MILAN_RV32_CC; AR=${CC%gcc}ar
cp $LITE/libc/picolibc-minimal.h $OUT/picolibc.h
F="-march=rv32i -mabi=ilp32 -Os -ffreestanding -fno-pie -fno-common -ffunction-sections -fdata-sections -fno-builtin -nostdlib -fno-stack-protector -I$OUT -I$PICO/libc/include -include $OUT/picolibc.h"
objs=()
for n in memcpy memmove memset memcmp; do
  $CC $F -D_LIBC -I$PICO/libc/string -I$PICO/libc/locale -I$PICO/libc/ctype -I$PICO/libm/common -c $PICO/libc/string/$n.c -o $OUT/$n.o; objs+=($OUT/$n.o); done
rm -f $OUT/libc.a; $AR crs $OUT/libc.a "${objs[@]}"
objs=()
for n in umodsi3 udivsi3 divsi3 modsi3 lshrdi3 muldi3 divdi3 ashldi3 ashrdi3 udivmoddi4 clzsi2 ctzsi2 clzdi2 ctzdi2 udivdi3 umoddi3 moddi3 ucmpdi2; do
  $CC $F -D_YUGA_LITTLE_ENDIAN=1 -D_YUGA_BIG_ENDIAN=0 -c $CRT/$n.c -o $OUT/$n.o; objs+=($OUT/$n.o); done
$CC $F -D_YUGA_LITTLE_ENDIAN=1 -D_YUGA_BIG_ENDIAN=0 -c $LITE/libcompiler_rt/mulsi3.c -o $OUT/mulsi3.o; objs+=($OUT/mulsi3.o)
rm -f $OUT/libcompiler_rt.a; $AR crs $OUT/libcompiler_rt.a "${objs[@]}"
sha256sum $OUT/libc.a $OUT/libcompiler_rt.a
