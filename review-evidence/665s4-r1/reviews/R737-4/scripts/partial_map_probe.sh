#!/bin/bash
# partial_map_probe.sh CHECKOUT BOOTDIR OUT: link the platform image with a flash map directory missing its headers.
# A true map gives a control image; each partial map removes generated files. Reports rc, ELF and the stand-in constants in ls_*.
C=$1; B=$2; O=$3; rm -rf "$O"; mkdir -p "$O"
cd "$C"
scan() { # elf
  riscv32-linux-objdump -d "$1" | awk '/^[0-9a-f]+ <ls_/{f=1} /^$/{f=0} f' > "$1.ls.dis"
  echo "ls_ lines $(wc -l < "$1.ls.dis"); lui 0xf0004: $(grep -c 'lui.*0xf0004' "$1.ls.dis"); lui 0x20000: $(grep -c 'lui.*0x20000' "$1.ls.dis")"
}
link() { # name mapdir
  python3 -B sw/firmware/ctrl/test/ctrl_plat_image.py --config configs/endstation_ax7101_1x1_tdm8.yaml \
    --csr-csv "$B/split-soc/mapped/soc/csr.csv" --flash-map "$2" --output "$O/$1" \
    --libc "$B/runtime/libc.a" --compiler-runtime "$B/runtime/libcompiler_rt.a" > "$O/$1.log" 2>&1
  rc=$?; printf '%s: rc=%s elf=%s\n' "$1" "$rc" "$([ -e "$O/$1/ctrl_app.elf" ] && echo yes || echo no)"
  [ -e "$O/$1/ctrl_app.elf" ] && scan "$O/$1/ctrl_app.elf" || tail -1 "$O/$1.log" | cut -c1-200
}
M=$B/split-soc/flash-map
link control-true-map "$M"
mkdir "$O/json-only"; cp "$M/flash_port.json" "$O/json-only/"; link json-only-map "$O/json-only"
for f in $(cd "$M"; find . -type f ! -name flash_port.json | sed 's#^\./##'); do
  d="$O/without-$(echo "$f" | tr '/.' '__')"; cp -r "$M" "$d"; rm "$d/$f"; link "partial-$(basename "$d")" "$d"
done
