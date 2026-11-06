#!/bin/bash
# nomap_elf.sh CHECKOUT BOOTDIR OUT: both refusals removed in a disposable copy, then the image linked with no map, a
# JSON-only map and maps lacking both headers or one, to compare with the images the boot probes planted.
C=$1; B=$2; O=$3; rm -rf "$O"; mkdir -p "$O/maps"; cd "$C" || exit 2
sed -i -e 's/^        if missing:$/        if False:/' -e 's/^    if flash_map is None and any(path.exists() for path in archives):$/    if False:/' sw/firmware/ctrl/test/ctrl_plat_image.py
link() { n=$1; shift; python3 -B sw/firmware/ctrl/test/ctrl_plat_image.py --config configs/endstation_ax7101_1x1_tdm8.yaml --csr-csv "$B/soc-provisional/csr.csv" \
    "$@" --output "$O/$n" --libc "$B/runtime/libc.a" --compiler-runtime "$B/runtime/libcompiler_rt.a" > "$O/$n.log" 2>&1
  echo "$n: rc=$? sha256 $(sha256sum "$O/$n/ctrl_app.elf" | cut -d' ' -f1)"; }
link no-map
cp -r "$B/split-soc/flash-map" "$O/maps/lacks-both"; rm "$O/maps/lacks-both/generated/csr.h" "$O/maps/lacks-both/generated/mem.h"
link lacks-both --flash-map "$O/maps/lacks-both"
mkdir -p "$O/maps/json-only"; cp "$B/split-soc/flash-map/flash_port.json" "$O/maps/json-only/"
link json-only --flash-map "$O/maps/json-only"
for h in csr mem; do cp -r "$B/split-soc/flash-map" "$O/maps/lacks-$h"; rm "$O/maps/lacks-$h/generated/$h.h"; link lacks-$h --flash-map "$O/maps/lacks-$h"; done
link control --flash-map "$B/split-soc/flash-map"
