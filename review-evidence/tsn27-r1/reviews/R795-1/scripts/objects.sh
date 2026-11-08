#!/bin/bash
# Core objects (adp, acmp, maap) built for RV32 with the base and head wire.h: text bytes and
# compiler-runtime helper references per option set.
set -u; . "$(dirname "$0")/env.sh"
O=$RCP/objects; W=$SCR/objects; mkdir -p "$O"; : > "$O/summary.txt"
tree 70936b77dc41981e192438388cd0aced69954f18 "$W/base"; tree HEAD "$W/head"
RV=riscv64-elf-gcc; INC=$($RV -print-file-name=include)
for side in base head; do
 for set in "stack-Debug:-march=rv32i -O0" "stack-Release:-march=rv32i -O3 -DNDEBUG" \
            "Os-rv32im:-march=rv32im -Os -DNDEBUG -ffunction-sections" "Os-rv32i:-march=rv32i -Os -DNDEBUG -ffunction-sections" \
            "O2-rv32im:-march=rv32im -O2 -DNDEBUG -ffunction-sections"; do
  tag=${set%%:*}; flags=${set#*:}; text=0; refs=""
  for m in adp acmp maap; do
    o=$W/$side-$tag-$m.o
    $RV $flags -mabi=ilp32 -std=c11 -ffreestanding -fno-builtin -nostdinc -isystem "$INC" -I"$W/$side/examples/rv32/include" -DCTRL_REENTRY_ASSERT -I"$W/$side/include" -c "$W/$side/src/$m.c" -o "$o" || echo "BUILD FAIL $side $tag $m" >> "$O/summary.txt"
    t=$(riscv64-elf-size -A "$o" | awk '$1 ~ /^\.text/ {s += $2} END {print s + 0}'); text=$((text + t))
    refs="$refs $(riscv64-elf-nm -u "$o" | awk '$2 ~ /^__/ {print $2}' | tr '\n' ',')"
  done
  n=$(for m in adp acmp maap; do riscv64-elf-objdump -dr "$W/$side-$tag-$m.o"; done | grep -c "R_RISCV_CALL.*__lshrdi3")
  echo "$side $tag text=$text lshrdi3_call_relocs=$n undefined_helpers=[$refs ]" >> "$O/summary.txt"
 done
done
cat "$O/summary.txt"
