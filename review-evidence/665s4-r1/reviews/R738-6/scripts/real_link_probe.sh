#!/bin/bash
# real_link_probe.sh CLONE FLATTENED_MAP RUNTIME OUT: true archives. A complete generated map as the control, then a map
# whose headers are links to, or copies of, the port's stand-ins, and a partial map, each scanned as the author scans.
C=$1; F=$2; RT=$3; O=$4; rm -rf "$O"; mkdir -p "$O/maps"
RV=$C/sw/firmware/ctrl_nvm/test/rv32/generated
cd "$C" || exit 2
scan() { riscv32-linux-objdump -d "$1" | awk '/^[0-9a-f]+ <ls_/{f=1} /^$/{f=0} f' > "$1.ls.dis"
  echo "  ls_ lines $(wc -l < "$1.ls.dis"); lui 0xf0004: $(grep -c 'lui.*0xf0004' "$1.ls.dis"); lui 0x20000: $(grep -c 'lui.*0x20000' "$1.ls.dis")"; }
link() { python3 -B sw/firmware/ctrl/test/ctrl_plat_image.py --config configs/endstation_ax7101_1x1_tdm8.yaml \
    --csr-csv sw/firmware/ctrl/test/ctrl_plat_csr.csv --flash-map "$2" --output "$O/$1" \
    --libc "$RT/libc.a" --compiler-runtime "$RT/libcompiler_rt.a" > "$O/$1.log" 2>&1
  rc=$?; printf '%s: rc=%s elf=%s\n' "$1" "$rc" "$([ -e "$O/$1/ctrl_app.elf" ] && echo yes || echo no)"
  if [ -e "$O/$1/ctrl_app.elf" ]; then scan "$O/$1/ctrl_app.elf"; else grep -m1 -E 'REFUSED|error:' "$O/$1.log" | cut -c1-170 | sed 's/^/  /'; fi; }
mk() { d="$O/maps/$1"; mkdir -p "$d/generated"; cp "$F/flash_port.json" "$d/"; }
mk real; cp "$F/generated-csr.h" "$d/generated/csr.h"; cp "$F/generated-mem.h" "$d/generated/mem.h"; link real "$d"
mk link-standin; ln -s "$RV/csr.h" "$d/generated/csr.h"; ln -s "$RV/mem.h" "$d/generated/mem.h"; link link-standin "$d"
mk copy-standin; cp "$RV/csr.h" "$RV/mem.h" "$d/generated/"; link copy-standin "$d"
mk lacks-mem; cp "$F/generated-csr.h" "$d/generated/csr.h"; link lacks-mem "$d"
