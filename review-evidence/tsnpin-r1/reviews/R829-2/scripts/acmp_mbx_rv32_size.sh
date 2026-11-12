#!/usr/bin/env bash
# acmp_mbx_rv32_size.sh <checkout> <sdk> <work> <rev>...: compile sw/firmware/ctrl/acmp/acmp_mbx.c at each rev
# with the pinned RV32 SDK and the image's flags, and print each function's size and sizeof(struct acmp_mbx).
set -eu
CO=$1; SDK=$2; W=$3; shift 3
for rev in "$@"; do
  d=$W/$rev; rm -rf "$d"; mkdir -p "$d/tree"
  git -C "$CO" archive "$rev" sw/firmware | tar -x -C "$d/tree"
  git -C "$CO" archive "$(git -C "$CO" rev-parse "$rev:third_party/tsn-c-stack" >/dev/null 2>&1 && echo "$rev")" >/dev/null 2>&1 || true
  stack=$CO/third_party/tsn-c-stack   # 715589c at both revs (the pin moved before round 1's head)
  test "$(git -C "$CO" rev-parse "$rev:third_party/tsn-c-stack")" = "$(git -C "$stack" rev-parse HEAD)"
  c=$d/tree/sw/firmware/ctrl
  inc=(); for x in mbx host port loop adp maap acmp app test; do inc+=("-I$c/$x"); done
  inc+=("-I$(dirname "$0")/shim" "-I$stack/include" "-I$d/tree/sw/firmware/ctrl_nvm" "-I$d/tree/sw/firmware/gtest")
  printf '#include "acmp_mbx.h"\n_Static_assert(1, "");\nunsigned sz_acmp_mbx = sizeof(struct acmp_mbx);\nunsigned pass_max = ACMP_MBX_PASS_MAX;\n' > "$d/sz.c"
  "$SDK/bin/riscv32-linux-gcc" -march=rv32i -mabi=ilp32 -ffreestanding -fno-stack-protector -Os -DNDEBUG -std=c11 \
    -DCTRL_MBX_BASE=0x80000000u -DNDEBUG -ffunction-sections -fdata-sections -fno-pic -fno-pie "${inc[@]}" \
    -c "$c/acmp/acmp_mbx.c" -o "$d/acmp_mbx.o"
  "$SDK/bin/riscv32-linux-gcc" -march=rv32i -mabi=ilp32 -ffreestanding -Os -std=c11 -DCTRL_MBX_BASE=0x80000000u \
    "${inc[@]}" -c "$d/sz.c" -o "$d/sz.o"
  echo "== $rev"
  "$SDK/bin/riscv32-linux-nm" -S --size-sort "$d/acmp_mbx.o" | awk '$3 ~ /[tT]/ {printf "  %s %d\n", $4, strtonum("0x"$2)}'
  "$SDK/bin/riscv32-linux-size" "$d/acmp_mbx.o" | tail -1 | awk '{print "  text", $1}'
  "$SDK/bin/riscv32-linux-objdump" -s -j .data.sz_acmp_mbx -j .data.pass_max -j .sdata.sz_acmp_mbx -j .sdata.pass_max -j .data -j .sdata "$d/sz.o" | grep -E "^ [0-9a-f]{4} " | head -2
done
