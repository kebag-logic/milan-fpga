#!/usr/bin/env bash
# Rebuild both RV32 image fixtures at every shape in two trees and hash the ELFs.
# usage: images.sh <head-tree> <dev-tree> <work> <litex-root>
# MILAN_RV32_CC must name the pinned SDK compiler.
set -u
HEAD_T=$1; DEV_T=$2; W=$3; LX=$4
SHAPES="endstation_arty_4x4 endstation_arty_8ch endstation_arty_current endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8"
mkdir -p "$W/rt" "$W/logs"
# One runtime, used by both sides (built with the head tree's unchanged builder).
( cd "$HEAD_T/sw/firmware/ctrl/test" && python3 -B ctrl_image_runtime.py \
    --picolibc "$LX/pythondata-software-picolibc/pythondata_software_picolibc/data" \
    --compiler-rt "$LX/pythondata-software-compiler_rt/pythondata_software_compiler_rt/data" \
    --litex-software "$LX/litex/litex/soc/software" --output "$W/rt" ) > "$W/logs/runtime.log" 2>&1
echo "runtime rc=$?"
sha256sum "$W/rt/libc.a" "$W/rt/libcompiler_rt.a"
pids=()
for side in head dev; do
  T=$HEAD_T; [ $side = dev ] && T=$DEV_T
  for s in $SHAPES; do
    ( python3 -B "$T/sw/firmware/ctrl/test/ctrl_image.py" --shape $s --out "$W/$side/img/$s" > "$W/logs/$side-img-$s.log" 2>&1; echo $? > "$W/logs/$side-img-$s.rc" ) &
    pids+=($!)
    for i in 1 2; do for v in srp nosrp; do
      extra=""; [ $v = nosrp ] && extra="--without-srp"
      ( cd "$T/sw/firmware/ctrl/test" && python3 -B ctrl_srp_image.py --config "$T/configs/$s.yaml" --output "$W/$side/srp/$s-if$i-$v" \
          --interfaces $i $extra --libc "$W/rt/libc.a" --compiler-runtime "$W/rt/libcompiler_rt.a" > "$W/logs/$side-srp-$s-if$i-$v.log" 2>&1; echo $? > "$W/logs/$side-srp-$s-if$i-$v.rc" ) &
      pids+=($!)
      while [ "$(jobs -rp | wc -l)" -ge 16 ]; do sleep 1; done
    done; done
  done
done
wait
for side in head dev; do
  for s in $SHAPES; do
    f="$W/$side/img/$s/head/$s/ctrl_app.elf"
    echo "$side ctrl_image $s rc=$(cat $W/logs/$side-img-$s.rc) $(sha256sum "$f" 2>/dev/null | cut -d' ' -f1)"
    for i in 1 2; do for v in nosrp srp; do
      f="$W/$side/srp/$s-if$i-$v/ctrl_app.elf"
      echo "$side ctrl_srp_image $s-if$i-$v rc=$(cat $W/logs/$side-srp-$s-if$i-$v.rc) $(sha256sum "$f" 2>/dev/null | cut -d' ' -f1)"
    done; done
  done
done
