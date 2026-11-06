#!/bin/bash
# fallback_elf.sh CHECKOUT BOOTDIR OUT: the header refusal removed in a disposable copy, a true partial map linked, to
# compare with the boot probes' planted images: a map that lacks a header compiles on the stand-in the plant holds.
C=$1; B=$2; O=$3; rm -rf "$O"; mkdir -p "$O/maps"; cd "$C" || exit 2
sed -i 's/^        if missing:$/        if False:/' sw/firmware/ctrl/test/ctrl_plat_image.py
for h in csr mem; do cp -r "$B/split-soc/flash-map" "$O/maps/lacks-$h"; rm "$O/maps/lacks-$h/generated/$h.h"
  python3 -B sw/firmware/ctrl/test/ctrl_plat_image.py --config configs/endstation_ax7101_1x1_tdm8.yaml --csr-csv "$B/soc-provisional/csr.csv" \
    --flash-map "$O/maps/lacks-$h" --output "$O/lacks-$h" --libc "$B/runtime/libc.a" --compiler-runtime "$B/runtime/libcompiler_rt.a" > "$O/lacks-$h.log" 2>&1
  echo "lacks-$h: rc=$? sha256 $(sha256sum "$O/lacks-$h/ctrl_app.elf" | cut -d' ' -f1)"; done
