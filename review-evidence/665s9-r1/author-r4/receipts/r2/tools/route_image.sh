#!/usr/bin/env bash
# route_image.sh <src>: the shipping 1x1 split image for the integrated route, built through the split recipe in <src>,
# a clean clone of the head (the exported script reads the RTL from it, so it stays until the routes end).
set -euo pipefail
L=$1; S=<scratch>; W=$S/route; B=$S/tmp/boot-1x1
CFG=configs/endstation_ax7101_1x1_tdm8.yaml; STEM=endstation_ax7101_1x1_tdm8
PY=<home>/litex-milan/venv/bin/python3
export PATH=<round1-scratch><home-path>/host/bin:/usr/local/bin:/usr/bin:/bin COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true PYTHONHASHSEED=0
FLOW=(--synth-directive AreaOptimized_high --opt-directive ExploreArea --place-directive ExtraPostPlacementOpt --vivado-max-threads 32)
cd "$L"
echo "head $(git rev-parse HEAD)"
# 1. the split recipe: the config's own shape, control.placement: split
/usr/bin/python3 sw/builder/endstation_builder.py "$CFG" --placement split
mapfile -t ARGV < <(/usr/bin/python3 -c "import json,sys; print('\n'.join(json.load(open(sys.argv[1]))['argv']))" sw/builder/out/$STEM/soc_params.json)
FW=$(printf '%s\n' "${ARGV[@]}" | grep -A1 -x -- --ctrl-firmware | tail -1)
echo "recipe argv names --ctrl-firmware $FW"
# 2. a stand-in export for the CSR map, which does not depend on the image (the boot run's provisional image)
STANDIN=$B/image-provisional/ctrl_app.elf
STAND_ARGV=("${ARGV[@]}"); for i in "${!STAND_ARGV[@]}"; do [ "${STAND_ARGV[$i]}" = "$FW" ] && STAND_ARGV[$i]=$STANDIN; done
rm -rf "$W/standin" "$W/flash-map" "$W/image" "$W/split"
(cd sw/litex && "$PY" milan_soc.py "${STAND_ARGV[@]}" --entity-gen-dir "$L/configs/generated/$STEM" "${FLOW[@]}" --no-compile-software --output-dir "$W/standin" > "$W/standin.log" 2>&1)
# 3. the flash port's map from that export, 4. the platform image linked against its csr.csv and that map
"$PY" -B sw/firmware/ctrl_nvm/plat/gen_flash_port.py --csr-csv "$W/standin/csr.csv" --csr-h "$W/standin/software/include/generated/csr.h" --out "$W/flash-map"
"$PY" -B sw/firmware/ctrl/test/ctrl_plat_image.py --config "$CFG" --interfaces 1 --csr-csv "$W/standin/csr.csv" --flash-map "$W/flash-map" --output "$W/image" --libc "$B/runtime/libc.a" --compiler-runtime "$B/runtime/libcompiler_rt.a"
cp "$W/image/ctrl_app.elf" "$FW"
# 5. the split image the recipe names, exported for the route; its build runs the identity gate
(cd sw/litex && "$PY" milan_soc.py "${ARGV[@]}" --entity-gen-dir "$L/configs/generated/$STEM" "${FLOW[@]}" --no-compile-software --output-dir "$W/split" > "$W/split.log" 2>&1)
tail -2 "$W/split.log"
# the CSR map is the stand-in's
diff <(grep -E '^(csr_base|csr_register|constant|memory_region),' "$W/standin/csr.csv" | grep -v -E '^memory_region,(rom|sram),') \
     <(grep -E '^(csr_base|csr_register|constant|memory_region),' "$W/split/csr.csv" | grep -v -E '^memory_region,(rom|sram),') && echo "csr map: the image's equals the stand-in's"
"$PY" sw/litex/check_image_identity.py "$W/split"
# 6. the M0s recipe's integrated script, full-split census
/usr/bin/python3 syn/ooc/pp_baseline.py "$W/split/gateware" --placement full-split --single-thread-synthesis
echo done
