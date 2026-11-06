#!/bin/bash
# map_probes.sh CLONE MUTANT_COPY OUT: what a directory at a header does at the head and under the exists() mutant, and
# what the stand-in directory does as a map. Objects are read, because empty archives stop every run at its link.
C=$1; M=$2; O=$3; rm -rf "$O"; mkdir -p "$O"
RV=sw/firmware/ctrl_nvm/test/rv32/generated
CFG=configs/endstation_ax7101_1x1_tdm8.yaml
: > "$O/libc.a"
HZ=$(cd "$C" && python3 -B sw/firmware/ctrl/test/ctrl_plat_image.py --config $CFG --csr-csv sw/firmware/ctrl/test/ctrl_plat_csr.csv \
     --flash-map "$(mkdir -p "$O/seed/generated"; : > "$O/seed/generated/csr.h"; : > "$O/seed/generated/mem.h"; echo '{"clock_hz":1}' > "$O/seed/flash_port.json"; echo "$O/seed")" \
     --output "$O/seed-out" --libc "$O/libc.a" --compiler-runtime "$O/libc.a" 2>&1 | sed -n 's/.*the shape at \([0-9]*\) Hz.*/\1/p')
echo "shape clock: $HZ Hz"
run() { # label tree mapdir
  ( cd "$2" && python3 -B sw/firmware/ctrl/test/ctrl_plat_image.py --config $CFG --csr-csv sw/firmware/ctrl/test/ctrl_plat_csr.csv \
    --flash-map "$3" --output "$O/$1" --libc "$O/libc.a" --compiler-runtime "$O/libc.a" ) > "$O/$1.log" 2>&1
  rc=$?; obj=$(ls "$O/$1"/*nvm_flash_litespi.o 2>/dev/null | head -1)
  printf '%s: rc=%s elf=%s files=%s\n' "$1" "$rc" "$([ -e "$O/$1/ctrl_app.elf" ] && echo yes || echo no)" "$(ls "$O/$1" 2>/dev/null | wc -l)"
  if [ -n "$obj" ]; then
    riscv32-linux-objdump -d "$obj" > "$obj.dis"
    echo "  flash port object compiled; lui 0xf0004: $(grep -c 'lui.*0xf0004' "$obj.dis"); lui 0x20000: $(grep -c 'lui.*0x20000' "$obj.dis")"
  fi
  grep -m1 -E 'REFUSED|error:' "$O/$1.log" | cut -c1-170 | sed 's/^/  /'
}
mk() { d="$O/maps/$1"; mkdir -p "$d/generated"; echo "{\"clock_hz\":$HZ}" > "$d/flash_port.json"; }
mk dir-both; mkdir "$d/generated/csr.h" "$d/generated/mem.h"
run head-dir-both "$C" "$d"
run mutant-dir-both "$M" "$d"
mk link-standin; ln -s "$C/$RV/csr.h" "$d/generated/csr.h"; ln -s "$C/$RV/mem.h" "$d/generated/mem.h"
run head-link-standin "$C" "$d"
mk copy-standin; cp "$C/$RV/csr.h" "$C/$RV/mem.h" "$d/generated/"
run head-copy-standin "$C" "$d"
run head-standin-dir-as-map "$C" "$C/sw/firmware/ctrl_nvm/test/rv32"
