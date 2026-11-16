#!/usr/bin/env bash
# export_only.sh <clone> <stem> <out> <standin-elf> <runtime-dir> [--ledgered-point NAME]: S9's split recipe up to the
# gateware export (the builder, the stand-in export, the flash port's map, the platform image, then milan_soc.py with
# the recipe's argv and flow and no --build), no Vivado: the export's Verilog for a base-to-head comparison.
set -u
L=$1; STEM=$2; W=$3; STANDIN=$4; RT=$5; shift 5; LP=("$@")
T=/data-2/milan/tmp/923-a789
mkdir -p "$W"; rm -rf "$W/standin" "$W/flash-map" "$W/image" "$W/export"
. $T/env.sh
export HOME=$T/home TMPDIR=$T/tmp LITEX_ENV_CC_TRIPLE=riscv32-linux
CFG=configs/$STEM.yaml
cd "$L" || exit 3
echo "head $(git rev-parse --short HEAD) status: $(git status --porcelain | wc -l)"
/usr/bin/python3 sw/builder/endstation_builder.py "$CFG" --placement split > "$W/builder.log" 2>&1 || exit 4
mapfile -t ARGV < <(/usr/bin/python3 -c "import json,sys; print('\n'.join(json.load(open(sys.argv[1]))['argv']))" sw/builder/out/$STEM/soc_params.json)
FW=$(printf '%s\n' "${ARGV[@]}" | grep -A1 -x -- --ctrl-firmware | tail -1)
STAND_ARGV=("${ARGV[@]}"); for i in "${!STAND_ARGV[@]}"; do [ "${STAND_ARGV[$i]}" = "$FW" ] && STAND_ARGV[$i]=$STANDIN; done
FLOW=(--synth-directive AreaOptimized_high --opt-directive ExploreArea --place-directive ExtraPostPlacementOpt)
(cd sw/litex && python3 milan_soc.py "${STAND_ARGV[@]}" --entity-gen-dir "$L/configs/generated/$STEM" "${FLOW[@]}" --no-compile-software --output-dir "$W/standin" > "$W/standin.log" 2>&1) || { echo "standin export failed"; exit 5; }
python3 -B sw/firmware/ctrl_nvm/plat/gen_flash_port.py --csr-csv "$W/standin/csr.csv" --csr-h "$W/standin/software/include/generated/csr.h" --out "$W/flash-map" > /dev/null || exit 6
python3 -B sw/firmware/ctrl/test/ctrl_plat_image.py --config "$CFG" --interfaces 1 "${LP[@]}" --csr-csv "$W/standin/csr.csv" --flash-map "$W/flash-map" --output "$W/image" --libc "$RT/libc.a" --compiler-runtime "$RT/libcompiler_rt.a" > "$W/image.log" 2>&1 || { echo "image failed"; exit 7; }
cp "$W/image/ctrl_app.elf" "$FW"
(cd sw/litex && python3 milan_soc.py "${ARGV[@]}" --entity-gen-dir "$L/configs/generated/$STEM" "${FLOW[@]}" --no-compile-software --output-dir "$W/export" > "$W/export.log" 2>&1) || { echo "export failed"; exit 8; }
git checkout -q -- configs sw/builder 2>/dev/null; git clean -q -fd configs/generated sw/builder/out 2>/dev/null
echo "export rc=0 status after: $(git status --porcelain --untracked-files=no | wc -l)"
