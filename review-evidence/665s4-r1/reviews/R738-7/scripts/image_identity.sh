#!/bin/bash
# image_identity.sh WORK: each booted image's map headers, stand-in constants in the flash port and loadable hash.
W=$1; OD=riscv32-linux-objdump; OC=riscv32-linux-objcopy
for v in control-8x8 nomap-1x1 stand-in-mem-8x8 stand-in-csr-8x8; do
  e=$W/$v-build/image/ctrl_app.elf; d=$W/$v/sw/firmware/ctrl_nvm/test/rv32/generated; m=$W/$v-build/split-soc/flash-map/generated
  h() { cmp -s "$m/$1" "$d/$1" && echo STAND-IN || echo generated; }
  link=$(grep -c -- '--flash-map' "$W/$v-build/image.log" 2>/dev/null)
  dis=$($OD -d "$e" | awk '/^[0-9a-f]+ <ls_/{f=1} /^[0-9a-f]+ <[^l]/{f=0} f')
  $OC -O binary "$e" "$W/$v.bin"
  echo "$v: map csr.h=$(h csr.h) mem.h=$(h mem.h); lui 0xf0004: $(grep -c 'lui.*0xf0004$' <<<"$dis"); lui 0xf0003: $(grep -c 'lui.*0xf0003$' <<<"$dis"); lui 0x20000: $(grep -c 'lui.*0x20000$' <<<"$dis"); loadable $(sha256sum "$W/$v.bin" | cut -c1-16)"
done
