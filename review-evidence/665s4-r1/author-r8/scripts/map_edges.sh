#!/bin/bash
# map_edges.sh CHECKOUT BOOTDIR OUT: real archives and the real generated map, with the map's shape broken in the ways
# an existence check might miss. Each line: rc, ELF, and either the stand-in constants in ls_* or the refusal's words.
# The ruling's outcome is a named refusal or no ELF; the control and the relative map must link with 0 and 0.
C=$1; B=$2; O=$3; rm -rf "$O"; mkdir -p "$O"
cd "$C" || exit 2
M=$B/split-soc/flash-map
scan() { # elf
  riscv32-linux-objdump -d "$1" | awk '/^[0-9a-f]+ <ls_/{f=1} /^$/{f=0} f' > "$1.ls.dis"
  echo "  ls_ lines $(wc -l < "$1.ls.dis"); lui 0xf0004: $(grep -c 'lui.*0xf0004' "$1.ls.dis"); lui 0x20000: $(grep -c 'lui.*0x20000' "$1.ls.dis")"
}
link() { # name mapdir
  python3 -B sw/firmware/ctrl/test/ctrl_plat_image.py --config configs/endstation_ax7101_1x1_tdm8.yaml \
    --csr-csv "$B/split-soc/mapped/soc/csr.csv" --flash-map "$2" --output "$O/$1" \
    --libc "$B/runtime/libc.a" --compiler-runtime "$B/runtime/libcompiler_rt.a" > "$O/$1.log" 2>&1
  rc=$?; printf '%s: rc=%s elf=%s\n' "$1" "$rc" "$([ -e "$O/$1/ctrl_app.elf" ] && echo yes || echo no)"
  if [ -e "$O/$1/ctrl_app.elf" ]; then scan "$O/$1/ctrl_app.elf"; else grep -m1 -E 'REFUSED|error:' "$O/$1.log" | cut -c1-200 | sed 's/^/  /'; fi
}
fresh() { d="$O/maps/$1"; mkdir -p "$O/maps"; cp -r "$M" "$d"; }
link control "$M"
fresh empty-csr; : > "$d/generated/csr.h"; link empty-csr "$d"
fresh empty-mem; : > "$d/generated/mem.h"; link empty-mem "$d"
fresh dir-csr; rm "$d/generated/csr.h"; mkdir "$d/generated/csr.h"; link dir-csr "$d"
fresh dangling-mem; rm "$d/generated/mem.h"; ln -s /nonexistent/mem.h "$d/generated/mem.h"; link dangling-mem "$d"
mkdir -p "$O/maps/flattened"; cp "$M/flash_port.json" "$O/maps/flattened/"
cp "$M/generated/csr.h" "$O/maps/flattened/generated-csr.h"; cp "$M/generated/mem.h" "$O/maps/flattened/generated-mem.h"
link flattened "$O/maps/flattened"
link absent "$O/maps/not-there"
fresh a-file; link a-file "$d/flash_port.json"
fresh no-json; rm "$d/flash_port.json"; link no-json "$d"
rel=$(python3 -c 'import os,sys; print(os.path.relpath(sys.argv[1]))' "$M"); link relative "$rel"
