#!/bin/bash
# link_probes.sh CHECKOUT BOOTDIR OUT: real archives and the real map at this head. A logging compiler shows whether
# each refusal calls the compiler at all; the real compiler links the control and a map named by a relative path.
C=$1; B=$2; O=$3; rm -rf "$O"; mkdir -p "$O/fake" "$O/maps"; cd "$C" || exit 2
M=$B/split-soc/flash-map; CFG=configs/endstation_ax7101_1x1_tdm8.yaml; CSV=$B/soc-provisional/csr.csv
LOG=$O/compiler-calls.log; : > "$LOG"
printf '#!/bin/bash\necho "$*" >> %s\nexit 1\n' "$LOG" > "$O/fake/fake-gcc"; chmod +x "$O/fake/fake-gcc"
base() { python3 -B sw/firmware/ctrl/test/ctrl_plat_image.py --config $CFG --csr-csv "$CSV" --output "$O/$1" \
  --libc "$B/runtime/libc.a" --compiler-runtime "$B/runtime/libcompiler_rt.a" "${@:2}"; }
fake() { n=$1; shift; before=$(wc -l < "$LOG"); MILAN_RV32_CC=$O/fake/fake-gcc base "$n" "$@" > "$O/$n.log" 2>&1; rc=$?
  printf '%s: rc=%s compiler calls=%s files left=%s\n  %s\n' "$n" "$rc" "$(( $(wc -l < "$LOG") - before ))" "$(ls -A "$O/$n" | wc -l)" "$(tail -1 "$O/$n.log" | cut -c1-120)"; }
scan() { riscv32-linux-objdump -d "$1" | awk '/^[0-9a-f]+ <ls_/{f=1} /^$/{f=0} f' > "$1.ls"; echo "  ls_ lines $(wc -l < "$1.ls"); lui 0xf0004: $(grep -c 'lui.*0xf0004' "$1.ls"); lui 0x20000: $(grep -c 'lui.*0x20000' "$1.ls"); sha256 $(sha256sum "$1" | cut -c1-16)"; }
real() { n=$1; shift; base "$n" "$@" > "$O/$n.log" 2>&1; rc=$?; printf '%s: rc=%s elf=%s\n' "$n" "$rc" "$([ -e "$O/$n/ctrl_app.elf" ] && echo yes || echo no)"; [ -e "$O/$n/ctrl_app.elf" ] && scan "$O/$n/ctrl_app.elf"; }
cp -r "$M" "$O/maps/json-only"; rm -r "$O/maps/json-only/generated"
cp -r "$M" "$O/maps/lacks-csr"; rm "$O/maps/lacks-csr/generated/csr.h"
cp -r "$M" "$O/maps/lacks-mem"; rm "$O/maps/lacks-mem/generated/mem.h"
echo "== a logging compiler: the refusals call it never, the complete map's control calls it"
fake no-map; fake json-only --flash-map "$O/maps/json-only"; fake lacks-csr --flash-map "$O/maps/lacks-csr"; fake lacks-mem --flash-map "$O/maps/lacks-mem"
fake control-complete --flash-map "$M"
echo "== the real compiler"
real complete --flash-map "$M"
real relative --flash-map "$(python3 -c 'import os,sys; print(os.path.relpath(sys.argv[1]))' "$M")"
