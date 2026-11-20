#!/usr/bin/env bash
# gprep.sh <clone> <stem> <boot-dir> <work-dir>: S9's split recipe steps 1-4 (prep.sh, the shape a parameter) for the
# gating images: the builder's split placement, a stand-in export for the CSR map, the flash port's map, the platform
# image linked against them (one interface, as the train's route_image.sh / route_image8.sh), copied to the path the
# recipe argv names; the argv is written to <work-dir>/argv.txt for the build.
set -euo pipefail
L=$1; STEM=$2; B=$3; W=$4; S=<scratch>/gate13
source $S/tools/env.sh
CFG=configs/$STEM.yaml
mkdir -p "$W"; cd "$L"
echo "head $(git rev-parse HEAD) status: $(git status --porcelain | tr '\n' ' ')"; date -Iseconds
/usr/bin/python3 sw/builder/endstation_builder.py "$CFG" --placement split
mapfile -t ARGV < <(/usr/bin/python3 -c "import json,sys; print('\n'.join(json.load(open(sys.argv[1]))['argv']))" sw/builder/out/$STEM/soc_params.json)
printf '%s\n' "${ARGV[@]}" > "$W/argv.txt"
FW=$(printf '%s\n' "${ARGV[@]}" | grep -A1 -x -- --ctrl-firmware | tail -1)
echo "recipe argv: ${ARGV[*]}"
echo "recipe argv names --ctrl-firmware $FW"
STANDIN=$B/image-provisional/ctrl_app.elf
STAND_ARGV=("${ARGV[@]}"); for i in "${!STAND_ARGV[@]}"; do [ "${STAND_ARGV[$i]}" = "$FW" ] && STAND_ARGV[$i]=$STANDIN; done
rm -rf "$W/standin" "$W/flash-map" "$W/image"
FLOW=(--synth-directive AreaOptimized_high --opt-directive ExploreArea --place-directive ExtraPostPlacementOpt)
(cd sw/litex && python3 milan_soc.py "${STAND_ARGV[@]}" --entity-gen-dir "$L/configs/generated/$STEM" "${FLOW[@]}" --no-compile-software --output-dir "$W/standin" > "$W/standin.log" 2>&1)
echo "standin export rc=0"
python3 -B sw/firmware/ctrl_nvm/plat/gen_flash_port.py --csr-csv "$W/standin/csr.csv" --csr-h "$W/standin/software/include/generated/csr.h" --out "$W/flash-map"
python3 -B sw/firmware/ctrl/test/ctrl_plat_image.py --config "$CFG" --interfaces 1 --csr-csv "$W/standin/csr.csv" --flash-map "$W/flash-map" --output "$W/image" --libc "$B/runtime/libc.a" --compiler-runtime "$B/runtime/libcompiler_rt.a"
cp "$W/image/ctrl_app.elf" "$FW"
sha256sum "$W/image/ctrl_app.elf" "$FW" "$CFG" sw/builder/out/$STEM/soc_params.json "$B/runtime/libc.a" "$B/runtime/libcompiler_rt.a"
echo "status after prep: $(git status --porcelain | tr '\n' ' ')"
date -Iseconds; echo PREP_DONE
