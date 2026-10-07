#!/usr/bin/env bash
# Link the composed RV32I image at the clone's head and at round 6 (13e71513),
# then compare the ELFs byte for byte. Usage: image_compare.sh <clone> <out> <riscv32-linux-gcc>
set -u
C=$1; O=$2; export MILAN_RV32_CC=$3
( cd "$C" && python3 sw/firmware/ctrl/test/ctrl_image.py --base 13e715136b0b7c8d9763e0b730d9709f2c9f5932 --out "$O" ) || exit $?
cd "$O" && sha256sum head/*/ctrl_app.elf base/*/ctrl_app.elf
for s in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do cmp head/$s/ctrl_app.elf base/$s/ctrl_app.elf && echo "$s byte-identical"; done
