#!/bin/sh
# Compile every firmware C file outside test/ at two revisions with the split image's RV32 flags and one compiler, and
# compare each object's code and data (sections dumped, the compiler's .comment dropped).
# usage: objects_identical.sh <repo> <rev-a> <rev-b> <workdir> <gcc-bin-dir>
set -eu
repo=$1; a=$2; b=$3; work=$4; bin=$5
CC=$bin/riscv32-linux-gcc; OD=$bin/riscv32-linux-objdump; OC=$bin/riscv32-linux-objcopy
FLAGS="-march=rv32im -mabi=ilp32 -ffreestanding -fno-stack-protector -Os -DNDEBUG -std=c11 -Wall -Wextra -pedantic -DCTRL_MBX_BASE=0x80000000u -DCTRL_MBX_DMA_BASE=0x8000f400u -ffunction-sections -fdata-sections"
for r in $a $b; do
  d=$work/$r; rm -rf "$d"; mkdir -p "$d/src" "$d/obj"
  git -C "$repo" archive "$r" sw/firmware/ctrl sw/firmware/ctrl_nvm sw/firmware/gtest configs | tar -x -C "$d/src"
  cp "$work/../srp_entity_gen.h" "$d/srp_entity_gen.h"   # srp_entity.py at the repo, configs/endstation_ax7101_8x8.yaml (unchanged across the two revisions)
  cp -r "$repo/third_party/tsn-c-stack" "$repo/third_party/lwSRP" "$d/src/" 2>/dev/null || true
  inc=$(find "$d/src/sw/firmware/ctrl" "$d/src/tsn-c-stack" "$d/src/lwSRP" "$d/src/sw/firmware/ctrl_nvm" -type d -not -path '*/test*' -not -path '*/.git*' -not -path "*/examples/*" | sed 's/^/-I/' | tr '\n' ' ') ; inc="$inc -nostdinc -isystem $($CC -print-file-name=include) -isystem $d/src/tsn-c-stack/examples/rv32/include -Wno-error=implicit-function-declaration -Wno-implicit-function-declaration -Wno-builtin-declaration-mismatch"
  ( cd "$d/src/sw/firmware/ctrl" && find . -name '*.c' -not -path './test/*' | sort ) > "$d/list"
  while read -r f; do
    o=$d/obj/$(echo "$f" | sed 's|^\./||; s|/|__|g').o
    if ( cd "$d/src/sw/firmware/ctrl" && $CC $FLAGS $inc -include "$d/srp_entity_gen.h" -c "$f" -o "$o" ) 2>"$o.err"; then
      $OD -d -z "$o" | tail -n +3 > "$o.dis"; $OC -R .comment -R .note.GNU-stack "$o" "$o.nc"; $OD -s -r "$o.nc" | tail -n +3 > "$o.sec"; $OD -t "$o.nc" | tail -n +3 | sort > "$o.sym"; echo "ok $f"
    else echo "nocompile $f"; fi
  done < "$d/list" > "$d/status"
done
echo "compiler: $($CC --version | head -1)"
same=0; diff=0; skipped=0
while read -r st f; do
  o=$(echo "$f" | sed 's|^\./||; s|/|__|g').o
  if [ "$st" != ok ] || ! grep -q "^ok $f\$" "$work/$b/status"; then skipped=$((skipped+1)); echo "SKIP $f ($st at $a)"; continue; fi
  if cmp -s "$work/$a/obj/$o.dis" "$work/$b/obj/$o.dis" && cmp -s "$work/$a/obj/$o.sec" "$work/$b/obj/$o.sec" && cmp -s "$work/$a/obj/$o.sym" "$work/$b/obj/$o.sym"; then
    same=$((same+1)); echo "SAME $f"; else diff=$((diff+1)); echo "DIFF $f"; fi
done < "$work/$a/status"
echo "identical $same, different $diff, not compiled $skipped"
[ "$diff" -eq 0 ]
