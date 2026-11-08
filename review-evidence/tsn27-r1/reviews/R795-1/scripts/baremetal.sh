#!/bin/bash
# The repository's own RV32 gate on the base and on the exact head, with text sizes.
set -u; . "$(dirname "$0")/env.sh"
O=$RCP/baremetal; mkdir -p "$O"
for side in base:70936b77dc41981e192438388cd0aced69954f18 head:HEAD; do
  n=${side%%:*} c=${side#*:}; D=$SCR/baremetal/$n
  tree "$c" "$D/src"
  python3 "$D/src/scripts/baremetal.py" --work "$D/work" --jobs 2 > "$O/$n.log" 2>&1; echo "$n rc $?" >> "$O/rc.txt"
  cp "$D/work/results.json" "$O/$n-results.json" 2>/dev/null
  for k in debug release; do
    e=$D/work/$k/rv32_smoke.elf
    [ -f "$e" ] && echo "$n $k $(riscv64-elf-size "$e" | tail -1 | awk '{print "text="$1" data="$2" bss="$3}') lshrdi3_in_nm=$(riscv64-elf-nm "$e" | grep -c __lshrdi3)" >> "$O/sizes.txt"
  done
done
cat "$O/rc.txt" "$O/sizes.txt"
