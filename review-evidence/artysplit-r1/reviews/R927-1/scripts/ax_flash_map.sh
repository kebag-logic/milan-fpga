#!/usr/bin/env bash
# Produce an AX7101 1x1 split SoC flash map at the head tree (stand-in ELF,
# SoC export without software, gen_flash_port), then run the AX firmware
# identity comparison with it. usage: ax_flash_map.sh <packet-dir>
set -u
P=$1 S=$1/scratch H=$1/scratch/work-head B=$1/scratch/work-base
LITEX=$(ls -d "$HOME"/litex-milan/litex "$HOME"/litex-milan/migen "$HOME"/litex-milan/lite* "$HOME"/litex-milan/pythondata-* 2>/dev/null | sort -u | paste -sd:)
export PYTHONPATH="$LITEX" PYTHONHASHSEED=0
W=$S/axmap; rm -rf "$W"; mkdir -p "$W"
rt=$S/boot-arty/runtime
cd "$H" || exit 2
python3 -B sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_ax7101_1x1_tdm8.yaml --interfaces 1 \
    --with-aecp --layout split --output "$W/standin" --libc "$rt/libc.a" --compiler-runtime "$rt/libcompiler_rt.a" \
    > "$W/standin.log" 2>&1 || { echo "standin rc=$?"; exit 1; }
argv=$(python3 -I -c 'import json,sys; a=json.load(open(sys.argv[1]))["argv"]; i=a.index("--ctrl-firmware"); a[i+1]=sys.argv[2]; print(" ".join(a))' \
    "$(ls "$S"/identity/head/endstation_ax7101_1x1_tdm8-split/*/soc_params.json)" "$W/standin/ctrl_app.elf")
python3 -B sw/litex/milan_soc.py $argv --entity-gen-dir "$H/configs/generated/endstation_ax7101_1x1_tdm8" \
    --no-compile-software --output-dir "$W/soc" > "$W/soc.log" 2>&1 || { echo "soc rc=$?"; exit 1; }
python3 -B sw/firmware/ctrl_nvm/plat/gen_flash_port.py --csr-csv "$W/soc/csr.csv" \
    --csr-h "$W/soc/software/include/generated/csr.h" --out "$W/flash-map" > "$W/fmap.log" 2>&1 || { echo "fmap rc=$?"; exit 1; }
bash "$P/scripts/ax_firmware_identity.sh" "$B" "$H" "$W/flash-map" "$rt" "$S/axfw"
