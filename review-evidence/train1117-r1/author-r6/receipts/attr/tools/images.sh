#!/bin/bash
# images.sh: the attribution experiment's images compared (images.txt): each built ctrl_app.elf's sha256 and section
# sizes, the symbols that move between images, the bytes that differ in the loaded image, and the hold-off's
# assignment (srp_mbx.c declare_sources, m->held_cs[n] = SRP_REDECLARE_CS) disassembled in each.
set -u
T=<scratch>; A=$T/r7attr; X=<home>/br-milan-rv32/host/bin/riscv32-linux
W=$T/tmp/r7img; mkdir -p $W
e() { echo $A/$1/build/image/ctrl_app.elf; }
echo "# The attribution images (8x8/1if, valid-destinations arm, legs.py build: CPU regions cover, split L1, no XIP)"
echo "# A c05d5acb (step 13); B c1e95dc1 (the head); C B with SRP_REDECLARE_CS at step 12's expression (2,027 cs);"
echo "# D 01765bb0 (step 13's first parent, before #953); E B with SRP_REDECLARE_CS 2048u"
for x in A B C D E; do
  echo "$x sha256 $(sha256sum $(e $x) | cut -c1-64) $($X-readelf -SW $(e $x) | awk '{for(i=1;i<=NF;i++) if($i==".text"||$i==".rodata"||$i==".data"||$i==".bss") printf "%s 0x%s ", $i, $(i+4)}')"
  $X-objcopy -O binary $(e $x) $W/$x.bin
  $X-nm -n $(e $x) | awk '{print $1, $3}' > $W/$x.nm
done
for p in "A C" "D A" "A B" "B E" "A E"; do
  set -- $p
  moved=$(paste $W/$1.nm $W/$2.nm | awk '$1!=$3 || $2!=$4 {n++} END {print n+0 " of " NR}')
  echo "$1 vs $2: $(cmp -l $W/$1.bin $W/$2.bin | wc -l) loaded bytes differ; symbols at another address: $moved"
done
for x in A B C D E; do
  echo "## $x: the hold-off's assignment"
  $X-objdump -d $(e $x) | grep -B3 -A2 -E "sh\s+a3,0\(s11\)" | grep -A5 -B1 -E "li\s+a3,2027|lui\s+a3,0x1" | head -6
done
