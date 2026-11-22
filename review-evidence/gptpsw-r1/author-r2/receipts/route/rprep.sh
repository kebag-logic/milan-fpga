#!/usr/bin/env bash
# rprep.sh <clone> <work> <sw|plane>: the gating recipe's split prep at 8x8/1if (the train's gprep): the builder's
# split argv, the runtime archives, a stand-in image and export, the flash port's map, then the platform image linked
# against them, copied to the argv's --ctrl-firmware path. sw: the argv takes --sw-gptp in --fabric-gptp's place and
# the image is built --with-gptp (#884); plane: the recipe as it is, the image without gPTP.
set -euo pipefail
L=$1; W=$2; M=$3; STEM=endstation_ax7101_8x8
case $M in sw) GF=--sw-gptp; IG=--with-gptp;; plane) GF=--fabric-gptp; IG=;; *) echo "mode sw|plane" >&2; exit 2;; esac
source <scratch>/bin/env.sh
export HOME=<scratch>/home
CFG=configs/$STEM.yaml
PD=<home>/litex-milan
mkdir -p "$W"; cd "$L"
echo "head $(git rev-parse HEAD) status: $(git status --porcelain | tr '\n' ' ')"; date -Iseconds
python3 -B sw/builder/endstation_builder.py "$CFG" --placement split > "$W/builder.log" 2>&1
mapfile -t ARGV < <(python3 -c "import json,sys; print('\n'.join(json.load(open(sys.argv[1]))['argv']))" sw/builder/out/$STEM/soc_params.json)
for i in "${!ARGV[@]}"; do [ "${ARGV[$i]}" = "--fabric-gptp" ] && ARGV[$i]=$GF; done
printf '%s\n' "${ARGV[@]}" > "$W/argv.txt"
FW=$(printf '%s\n' "${ARGV[@]}" | grep -A1 -x -- --ctrl-firmware | tail -1)
rm -rf "$W/runtime" "$W/standin-image" "$W/standin" "$W/flash-map" "$W/image"
python3 -B tb/verilator/ctrl_service_budget/runtime_ssp.py --picolibc $PD/pythondata-software-picolibc/pythondata_software_picolibc/data \
  --compiler-rt $PD/pythondata-software-compiler_rt/pythondata_software_compiler_rt/data \
  --litex-software $PD/litex/litex/soc/software --output "$W/runtime" > "$W/runtime.log" 2>&1
python3 -B sw/firmware/ctrl/test/ctrl_srp_image.py --config "$CFG" --interfaces 1 --with-aecp --layout split \
  --output "$W/standin-image" --libc "$W/runtime/libc.a" --compiler-runtime "$W/runtime/libcompiler_rt.a" > "$W/standin-image.log" 2>&1
STAND=("${ARGV[@]}"); for i in "${!STAND[@]}"; do [ "${STAND[$i]}" = "$FW" ] && STAND[$i]=$W/standin-image/ctrl_app.elf; done
FLOW=(--synth-directive AreaOptimized_high --opt-directive ExploreArea --place-directive ExtraPostPlacementOpt)
(cd sw/litex && python3 milan_soc.py "${STAND[@]}" --entity-gen-dir "$L/configs/generated/$STEM" "${FLOW[@]}" \
   --no-compile-software --output-dir "$W/standin" > "$W/standin.log" 2>&1)
echo "standin export rc=0"
python3 -B sw/firmware/ctrl_nvm/plat/gen_flash_port.py --csr-csv "$W/standin/csr.csv" \
  --csr-h "$W/standin/software/include/generated/csr.h" --out "$W/flash-map" > "$W/flash-map.log" 2>&1
python3 -B sw/firmware/ctrl/test/ctrl_plat_image.py --config "$CFG" --interfaces 1 $IG --csr-csv "$W/standin/csr.csv" \
  --flash-map "$W/flash-map" --output "$W/image" --libc "$W/runtime/libc.a" \
  --compiler-runtime "$W/runtime/libcompiler_rt.a" > "$W/image.log" 2>&1 || { tail -5 "$W/image.log"; exit 5; }
python3 -c "import json;d=json.load(open('$W/image/size.json'));print('image plan', json.dumps(d['split']))"
cp "$W/image/ctrl_app.elf" "$FW"
sha256sum "$W/image/ctrl_app.elf" "$FW" "$CFG" sw/builder/out/$STEM/soc_params.json
date -Iseconds; echo PREP_DONE
