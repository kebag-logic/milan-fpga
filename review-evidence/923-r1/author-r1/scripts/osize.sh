#!/bin/bash
# osize.sh TREE: .text bytes of the changed AECP objects, compiled as the split image compiles them (rv32im -Os), at
# the 8x8 shape's generated header.
L=$1; T=/data-2/milan/tmp/923-a789; G=$T/img/head/platform-8x8-1if/image
CC=$WORKSPACE_HOME/br-milan-rv32/host/bin/riscv32-buildroot-linux-gnu-gcc
SZ=$WORKSPACE_HOME/br-milan-rv32/host/bin/riscv32-buildroot-linux-gnu-size
F="-march=rv32im -mabi=ilp32 -ffreestanding -fno-stack-protector -Os -DNDEBUG -std=c11 -Wall -Wextra -Werror -pedantic -ffunction-sections -fdata-sections -DCTRL_MBX_BASE=0x80000000u"
I="-I$L/sw/firmware/ctrl/aecp -I$L/sw/firmware/ctrl/mbx -I$L/sw/firmware/ctrl/port -I$L/sw/firmware/ctrl/loop -I$L/sw/firmware/ctrl/app -I$L/sw/firmware/ctrl/adp -I$L/sw/firmware/ctrl/acmp -I$L/sw/firmware/ctrl/maap -I$L/sw/firmware/ctrl/srp -I$L/third_party/tsn-c-stack/include -I$L/sw/firmware/ctrl_nvm -I$G -I$G/gen -I$G/nvm-shape"
mkdir -p $T/tmp/osize; tot=0
for f in aecp/aecp_maps.c aecp/aecp_face.c aecp/aecp_mbx.c app/ctrl_app_aecp.c mbx/mbx.c aecp/aecp_commands.c; do
  o=$T/tmp/osize/$(basename $f .c).o
  $CC $F $I -c $L/sw/firmware/ctrl/$f -o $o 2>$o.err || { echo "$f: compile failed"; head -3 $o.err; continue; }
  t=$($SZ $o | awk 'NR==2{print $1}'); tot=$((tot+t)); echo "$f $t"
done; echo "total $tot"
