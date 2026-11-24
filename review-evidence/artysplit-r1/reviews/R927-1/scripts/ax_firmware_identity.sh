#!/usr/bin/env bash
# Link the AX7101 split product firmware (1x1/1if and 8x8/1if) at the base
# tree and at the head tree from identical inputs (the fixture csr.csv, one
# flash map, one runtime) and compare the ELF bytes.
# usage: ax_firmware_identity.sh <base-tree> <head-tree> <flash-map> <runtime-dir> <out>
set -u
base=$1 head=$2 fmap=$3 rt=$4 out=$5
LITEX=$(ls -d "$HOME"/litex-milan/litex "$HOME"/litex-milan/migen "$HOME"/litex-milan/lite* "$HOME"/litex-milan/pythondata-* 2>/dev/null | sort -u | paste -sd:)
rm -rf "$out"; mkdir -p "$out"
for side in base head; do
    tree=${!side}
    for cfg in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
        d="$out/$side-$cfg"
        ( cd "$tree" && env PYTHONPATH="$LITEX" PYTHONHASHSEED=0 python3 -B sw/firmware/ctrl/test/ctrl_plat_image.py \
            --config "configs/$cfg.yaml" --interfaces 1 --csr-csv sw/firmware/ctrl/test/ctrl_plat_csr.csv \
            --flash-map "$fmap" --output "$d" --libc "$rt/libc.a" --compiler-runtime "$rt/libcompiler_rt.a" ) \
            > "$d.log" 2>&1
        echo "$side $cfg rc=$? $(sha256sum "$d/ctrl_app.elf" 2>/dev/null | cut -c1-64)"
    done
done
for cfg in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
    if cmp -s "$out/base-$cfg/ctrl_app.elf" "$out/head-$cfg/ctrl_app.elf"; then echo "IDENTICAL ELF $cfg"; else echo "DIFFERENT ELF $cfg"; fi
done
