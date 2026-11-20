#!/usr/bin/env bash
# obj_spot.sh <treeA> <treeB> <out>: compile the translation units that include the two changed
# firmware headers (aecp_mbx.c, ctrl_loop.c) with the firmware cross compiler at -O2 -g in each
# tree, with the source path mapped to one name, and compare the whole object files.
# rc 0 when every object is byte-identical.  Then a planted control: a copy of tree B's
# ctrl_loop.h with one added line before its first define must give a different object (line
# numbers move in debug info), proving the comparison sees header edits.
set -u
A=$1 B=$2 O=$3; mkdir -p "$O"
CC=${HOME}/br-milan-rv32/host/bin/riscv32-buildroot-linux-gnu-gcc
inc() { local r=$1; echo -I"$r/sw/firmware/ctrl" $(find "$r/sw/firmware/ctrl" "$r/sw/firmware" -maxdepth 2 -type d -printf '-I%p ' 2>/dev/null) -I"$r/sw/mailbox" -I"$r/sw/firmware/ctrl_nvm" -I"$r/third_party/tsn-c-stack/include"; }
cc1() { local r=$1 src=$2 obj=$3; ( cd "$r" && $CC -march=rv32im -mabi=ilp32 -O2 -g -ffreestanding -ffile-prefix-map="$r"=/T $(inc "$r") -c "$src" -o "$obj" ) ; }
rc=0
for src in sw/firmware/ctrl/aecp/aecp_mbx.c sw/firmware/ctrl/loop/ctrl_loop.c; do
  n=$(basename "$src" .c)
  cc1 "$A" "$src" "$O/$n.A.o" 2> "$O/$n.A.err" || { echo "COMPILE-FAIL A $src"; cat "$O/$n.A.err" | head -5; rc=2; continue; }
  cc1 "$B" "$src" "$O/$n.B.o" 2> "$O/$n.B.err" || { echo "COMPILE-FAIL B $src"; rc=2; continue; }
  a=$(sha256sum < "$O/$n.A.o" | cut -c1-64) b=$(sha256sum < "$O/$n.B.o" | cut -c1-64)
  [ "$a" = "$b" ] && v=IDENTICAL || { v=DIFFERS; rc=1; }
  echo "OBJ $src A $a B $b $v"
done
T=$O/plant; rm -rf "$T"; mkdir -p "$T"; cp -a "$B/sw" "$T/sw"; mkdir -p "$T/third_party"; cp -a "$B/third_party/tsn-c-stack" "$T/third_party/"
sed -i '0,/^#define/s//\n#define/' "$T/sw/firmware/ctrl/loop/ctrl_loop.h"
cc1 "$T" sw/firmware/ctrl/loop/ctrl_loop.c "$O/ctrl_loop.P.o" 2>/dev/null
p=$(sha256sum < "$O/ctrl_loop.P.o" | cut -c1-64) b=$(sha256sum < "$O/ctrl_loop.B.o" | cut -c1-64)
[ "$p" != "$b" ] && echo "PLANT one blank line in ctrl_loop.h: object $p differs: refused" || { echo "PLANT ESCAPED"; rc=1; }
rm -rf "$T"
echo "END rc=$rc"
exit $rc
