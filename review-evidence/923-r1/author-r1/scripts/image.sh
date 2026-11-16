#!/usr/bin/env bash
# image.sh <clone> <stem> <directive> <standin-elf> <runtime-dir>: S9's split recipe for one AX7101 config at one
# interface (the #920 lane's route_image steps): the builder's split placement, a stand-in export for the CSR map, the
# flash port's map, the platform image linked against them and copied to the path the recipe argv names, then the
# Vivado build with the recipe's flow and <directive> as the placement directive, the timing sign-off and the identity
# gate. Run inside vivado-slot.sh, one build at a time.
set -u
L=$1; STEM=$2; D=$3; STANDIN=$4; RT=$5
T=/data-2/milan/tmp/923-a789
W=$T/image/$STEM; O=$W/build_$D
mkdir -p "$W"; rm -rf "$W/standin" "$W/flash-map" "$W/image" "$O"
. $T/env.sh
export HOME=$T/home TMPDIR=$T/tmp LITEX_ENV_CC_TRIPLE=riscv32-linux
mkdir -p "$HOME" "$TMPDIR"
CFG=configs/$STEM.yaml
cd "$L" || exit 3
echo "head $(git rev-parse HEAD) status: $(git status --porcelain | tr '\n' ' ') $(date -Iseconds)"
/usr/bin/python3 sw/builder/endstation_builder.py "$CFG" --placement split || exit 4
mapfile -t ARGV < <(/usr/bin/python3 -c "import json,sys; print('\n'.join(json.load(open(sys.argv[1]))['argv']))" sw/builder/out/$STEM/soc_params.json)
FW=$(printf '%s\n' "${ARGV[@]}" | grep -A1 -x -- --ctrl-firmware | tail -1)
echo "recipe argv: ${ARGV[*]}"
STAND_ARGV=("${ARGV[@]}"); for i in "${!STAND_ARGV[@]}"; do [ "${STAND_ARGV[$i]}" = "$FW" ] && STAND_ARGV[$i]=$STANDIN; done
FLOW=(--synth-directive AreaOptimized_high --opt-directive ExploreArea --place-directive "$D")
(cd sw/litex && python3 milan_soc.py "${STAND_ARGV[@]}" --entity-gen-dir "$L/configs/generated/$STEM" "${FLOW[@]}" --no-compile-software --output-dir "$W/standin" > "$W/standin.log" 2>&1) || { echo "standin export failed"; exit 5; }
python3 -B sw/firmware/ctrl_nvm/plat/gen_flash_port.py --csr-csv "$W/standin/csr.csv" --csr-h "$W/standin/software/include/generated/csr.h" --out "$W/flash-map" || exit 6
case $STEM in *8x8*) LP=(--ledgered-point platform-8x8-one-interface);; *) LP=();; esac
python3 -B sw/firmware/ctrl/test/ctrl_plat_image.py --config "$CFG" --interfaces 1 "${LP[@]}" --csr-csv "$W/standin/csr.csv" --flash-map "$W/flash-map" --output "$W/image" --libc "$RT/libc.a" --compiler-runtime "$RT/libcompiler_rt.a" > "$W/image.log" 2>&1 || { echo "image failed"; tail -5 "$W/image.log"; exit 7; }
cp "$W/image/ctrl_app.elf" "$FW"
sha256sum "$W/image/ctrl_app.elf" "$FW" "$CFG" sw/builder/out/$STEM/soc_params.json
grep -E '"tiles"|"bytes"' "$W/image.log" | head -6
source $WORKSPACE_HOME/Xilinx2/2026.1/Vivado/settings64.sh
command -v vivado || { echo 'no vivado on PATH'; exit 8; }
echo "python3 milan_soc.py ${ARGV[*]} --entity-gen-dir $L/configs/generated/$STEM ${FLOW[*]} --no-compile-software --vivado-max-threads 8 --build --output-dir $O"
(cd sw/litex && HOME=$WORKSPACE_HOME python3 milan_soc.py "${ARGV[@]}" --entity-gen-dir "$L/configs/generated/$STEM" "${FLOW[@]}" \
  --no-compile-software --vivado-max-threads 8 --build --output-dir "$O")
rc=$?; echo "$rc" > "$O.rc"; echo "== BUILD rc=$rc $(date -Iseconds)"
[ $rc = 0 ] || exit $rc
python3 $MANAGEMENT/2026-09-23/923-a789/round1/scripts/signoff.py "$O/gateware"; echo "signoff rc=$?"
python3 sw/litex/check_image_identity.py "$O"; echo "identity rc=$?"
echo "status after: $(git status --porcelain | tr '\n' ' ')"
