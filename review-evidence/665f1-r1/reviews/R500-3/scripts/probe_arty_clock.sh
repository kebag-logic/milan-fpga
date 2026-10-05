#!/bin/sh
# Compile the LiteSPI flash port as the RV32 arm does, but with the system
# clock the three Arty shapes ship (configs/endstation_arty_*.yaml sys_clk_hz),
# instead of the stand-in's 100 MHz. Usage: probe_arty_clock.sh <repo> <workdir> <cc>
set -u
REPO=$1; WORK=$2; CC=$3
mkdir -p "$WORK/generated"
cp "$REPO/sw/firmware/ctrl_nvm/test/rv32/generated/csr.h" "$REPO/sw/firmware/ctrl_nvm/test/rv32/generated/mem.h" "$WORK/generated/"
for hz in 100000000 83333000; do
  printf '#ifndef GENERATED_SOC_H\n#define GENERATED_SOC_H\n#define CONFIG_CLOCK_FREQUENCY %s\n#endif\n' "$hz" > "$WORK/generated/soc.h"
  for cfg in "$REPO"/configs/endstation_*.yaml; do grep -q "sys_clk_hz: $hz" "$cfg" && echo "shape $(basename "$cfg" .yaml) ships sys_clk_hz $hz"; done
  # nvm_shape_gen.h is generated per shape by the suite; any shape's serves the port
  "$CC" -march=rv32i -mabi=ilp32 -Os -std=c11 -ffreestanding -Wall -Wextra -Werror \
     -I"$WORK" -I"$WORK/gen" -c "$REPO/sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c" -o "$WORK/ls_$hz.o"
  echo "CONFIG_CLOCK_FREQUENCY=$hz rc=$?"
done
