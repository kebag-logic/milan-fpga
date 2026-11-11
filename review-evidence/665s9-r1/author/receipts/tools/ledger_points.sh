#!/usr/bin/env bash
# ledger_points.sh: the platform image at the four ledger points, each linked against its shape's split export.
set -euo pipefail
L=<lane>; S=<scratch>; W=$S/ledger
PY=<home>/litex-milan/venv/bin/python3
export PATH=<home>/br-milan-rv32/host/bin:/usr/local/bin:/usr/bin:/bin COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true PYTHONHASHSEED=0
FLOW=(--synth-directive AreaOptimized_high --opt-directive ExploreArea --place-directive ExtraPostPlacementOpt --vivado-max-threads 32)
cd "$L"; echo "head $(git rev-parse HEAD)"
mkdir -p "$W"
export_shape() {  # stem standin-elf -> $W/<stem>-soc, $W/<stem>-flash-map
  local stem=$1 elf=$2
  /usr/bin/python3 sw/builder/endstation_builder.py configs/$stem.yaml --placement split > "$W/$stem-recipe.log"
  mapfile -t ARGV < <(/usr/bin/python3 -c "import json,sys; print('\n'.join(json.load(open(sys.argv[1]))['argv']))" sw/builder/out/$stem/soc_params.json)
  local i; for i in "${!ARGV[@]}"; do [ "${ARGV[$i]}" = "sw/builder/out/$stem/ctrl_app.elf" ] && ARGV[$i]=$elf; done
  rm -rf "$W/$stem-soc" "$W/$stem-flash-map"
  (cd sw/litex && "$PY" milan_soc.py "${ARGV[@]}" --entity-gen-dir "$L/configs/generated/$stem" "${FLOW[@]}" --no-compile-software --output-dir "$W/$stem-soc" > "$W/$stem-soc.log" 2>&1)
  "$PY" -B sw/firmware/ctrl_nvm/plat/gen_flash_port.py --csr-csv "$W/$stem-soc/csr.csv" --csr-h "$W/$stem-soc/software/include/generated/csr.h" --out "$W/$stem-flash-map" > /dev/null
}
link() {  # stem interfaces label [ledgered point]
  local stem=$1 n=$2 label=$3; shift 3
  rm -rf "$W/$label"
  "$PY" -B sw/firmware/ctrl/test/ctrl_plat_image.py --config configs/$stem.yaml --interfaces "$n" "$@" --csr-csv "$W/$stem-soc/csr.csv" --flash-map "$W/$stem-flash-map" --output "$W/$label" --libc "$S/boot-1x1/runtime/libc.a" --compiler-runtime "$S/boot-1x1/runtime/libcompiler_rt.a" > "$W/$label.log" 2>&1
  echo "$label linked"
}
export_shape endstation_ax7101_1x1_tdm8 "$S/boot-1x1/image-provisional/ctrl_app.elf"
export_shape endstation_ax7101_8x8 "$S/boot-8x8/image-provisional/ctrl_app.elf"
link endstation_ax7101_1x1_tdm8 1 1x1-1if
link endstation_ax7101_1x1_tdm8 2 1x1-2if
link endstation_ax7101_8x8 1 8x8-1if
link endstation_ax7101_8x8 2 8x8-2if --ledgered-point platform-8x8-two-interfaces
cmp "$W/1x1-1if/ctrl_app.elf" "$S/route/image/ctrl_app.elf" && echo "1x1-1if is the route's image"
echo done
