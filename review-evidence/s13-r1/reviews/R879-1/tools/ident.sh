#!/usr/bin/env bash
# ident.sh CLONE STEM WORK: the bench recipe's image INPUTS of one shape at one clone's head, without Vivado:
#   1. the builder's split placement recipe (endstation_builder.py CFG --placement split), its argv;
#   2. a provisional platform image (ident_prov.py) and a stand-in export of the recipe's SoC with it (csr.csv);
#   3. the flash port map from that export (gen_flash_port.py) and the platform image linked against both;
#   4. the recipe's milan_soc.py export with that image, without --build (the bench recipe's --eth-port e2 and
#      ExtraPostPlacementOpt flow), into WORK/export.
set -euo pipefail
C=$(realpath "$1"); STEM=$2; W=$(realpath -m "$3"); T=$(dirname "$(realpath "$0")")
source "$T/env.sh"
CFG=configs/$STEM.yaml
mkdir -p "$W"; cd "$C"
echo "head $(git rev-parse HEAD) porcelain $(git status --porcelain | wc -l)"; date -Iseconds
/usr/bin/python3 sw/builder/endstation_builder.py "$CFG" --placement split > "$W/builder.log"
mapfile -t ARGV < <(/usr/bin/python3 -c "import json,sys; print('\n'.join(json.load(open(sys.argv[1]))['argv']))" sw/builder/out/$STEM/soc_params.json)
printf '%s\n' "${ARGV[@]}" > "$W/argv.txt"
FW=$(printf '%s\n' "${ARGV[@]}" | grep -A1 -x -- --ctrl-firmware | tail -1)
mapfile -t PROV < <(python3 -B "$T/ident_prov.py" "$C" "$STEM" "$W/boot" | tail -3)
STAND=("${ARGV[@]}"); for i in "${!STAND[@]}"; do [ "${STAND[$i]}" = "$FW" ] && STAND[$i]=${PROV[0]}; done
FLOW=(--synth-directive AreaOptimized_high --opt-directive ExploreArea --place-directive ExtraPostPlacementOpt)
rm -rf "$W/standin" "$W/flash-map" "$W/image" "$W/export"
(cd sw/litex && python3 milan_soc.py "${STAND[@]}" --eth-port e2 --entity-gen-dir "$C/configs/generated/$STEM" "${FLOW[@]}" \
   --no-compile-software --output-dir "$W/standin" > "$W/standin.log" 2>&1)
python3 -B sw/firmware/ctrl_nvm/plat/gen_flash_port.py --csr-csv "$W/standin/csr.csv" \
   --csr-h "$W/standin/software/include/generated/csr.h" --out "$W/flash-map" > "$W/flash-map.log" 2>&1
python3 -B sw/firmware/ctrl/test/ctrl_plat_image.py --config "$CFG" --interfaces 1 --csr-csv "$W/standin/csr.csv" \
   --flash-map "$W/flash-map" --output "$W/image" --libc "${PROV[1]}" --compiler-runtime "${PROV[2]}" > "$W/image.log" 2>&1
cp "$W/image/ctrl_app.elf" "$FW"
(cd sw/litex && python3 milan_soc.py "${ARGV[@]}" --eth-port e2 --entity-gen-dir "$C/configs/generated/$STEM" "${FLOW[@]}" \
   --no-compile-software --vivado-max-threads 16 --output-dir "$W/export" > "$W/export.log" 2>&1)
sha256sum "$W/image/ctrl_app.elf" "$CFG" sw/builder/out/$STEM/soc_params.json "${PROV[1]}" "${PROV[2]}"
echo "porcelain after: $(git status --porcelain | tr '\n' ' ')"; date -Iseconds; echo IDENT_DONE
