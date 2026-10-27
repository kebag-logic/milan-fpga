#!/bin/sh
# Link the four split images for one ctrl source; usage: image_points.sh <clone> <ctrl-source> <outdir>
set -u
clone=$1; src=$2; out=$3
libc=$(riscv64-elf-gcc -march=rv32i -mabi=ilp32 -print-file-name=libc_nano.a)
rt=$(riscv64-elf-gcc -march=rv32i -mabi=ilp32 -print-libgcc-file-name)
mkdir -p "$out"
for pt in "1x1_tdm8 1" "1x1_tdm8 2" "8x8 1" "8x8 2"; do
  set -- $pt; cfg=$1; n=$2; extra=""
  [ "$cfg" = 8x8 ] && [ "$n" = 2 ] && extra="--ledgered-point 8x8-two-interfaces"
  ( cd "$clone" && python3 -B -s sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_ax7101_$cfg.yaml \
      --output "$out/$cfg-if$n" --ctrl-source "$src" --with-aecp --interfaces $n --layout split $extra \
      --libc "$libc" --compiler-runtime "$rt" > "$out/$cfg-if$n.log" 2>&1; echo $? > "$out/$cfg-if$n.rc" ) &
done
wait
