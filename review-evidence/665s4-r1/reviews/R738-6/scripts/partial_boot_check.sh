#!/bin/bash
# partial_boot_check.sh CLONE WORK: prove what each booted image carried, then link a truly partial map (the refusal
# removed in a copy, the header deleted, not replaced) and compare its loadable bytes to the image that was booted.
C=$1; W=$2; RV=$C/sw/firmware/ctrl_nvm/test/rv32/generated
scan() { riscv32-linux-objdump -d "$1" | awk '/^[0-9a-f]+ <ls_/{f=1} /^$/{f=0} f' > /tmp/r738-ls.$$
  printf 'lui 0xf0004: %s; lui 0xf0003: %s; lui 0x20000: %s' "$(grep -c 'lui.*0xf0004' /tmp/r738-ls.$$)" "$(grep -c 'lui.*0xf0003' /tmp/r738-ls.$$)" "$(grep -c 'lui.*0x20000' /tmp/r738-ls.$$)"; rm -f /tmp/r738-ls.$$; }
bin() { riscv32-linux-objcopy -O binary "$1" "$1.bin" && sha256sum "$1.bin" | cut -c1-16; }
for n in control stand-in-mem stand-in-csr; do
  b=$W/$n-build; e=$b/image/ctrl_app.elf
  printf '%s: elf %s; ' "$n" "$([ -e "$e" ] && echo yes || echo no)"
  cmp -s "$b/split-soc/flash-map/generated/csr.h" "$RV/csr.h" && printf 'map csr.h=STAND-IN; ' || printf 'map csr.h=generated; '
  cmp -s "$b/split-soc/flash-map/generated/mem.h" "$RV/mem.h" && printf 'map mem.h=STAND-IN; ' || printf 'map mem.h=generated; '
  [ -e "$e" ] && { scan "$e"; printf '; loadable %s' "$(bin "$e")"; }
  echo
done
d=$W/no-refusal; cp -a --reflink=auto "$C" "$d"
python3 -I - "$d/sw/firmware/ctrl/test/ctrl_plat_image.py" <<'EOF'
import sys,pathlib
p=pathlib.Path(sys.argv[1]); s=p.read_text()
a="        if missing:\n            raise Refusal(PARTIAL_MAP.format(\" and \".join(missing)))\n"
assert s.count(a)==1; p.write_text(s.replace(a,""))
EOF
b=$W/control-build; m=$W/true-partial-map; rm -rf "$m"; cp -r "$b/split-soc/flash-map" "$m"; rm "$m/generated/csr.h"
( cd "$d" && python3 -B sw/firmware/ctrl/test/ctrl_plat_image.py --config configs/endstation_ax7101_1x1_tdm8.yaml \
   --csr-csv "$W/stand-in-csr-build/soc/csr.csv" --flash-map "$m" --output "$W/true-partial" \
   --libc "$b/runtime/libc.a" --compiler-runtime "$b/runtime/libcompiler_rt.a" --interfaces 1 $EXTRA ) > "$W/true-partial.log" 2>&1
echo "true partial map (csr.h deleted, refusal removed in a copy): rc=$?"
e=$W/true-partial/ctrl_app.elf; [ -e "$e" ] && { printf '  '; scan "$e"; printf '; loadable %s\n' "$(bin "$e")"; } || tail -2 "$W/true-partial.log" | cut -c1-200
