#!/usr/bin/env bash
# rbuild.sh <clone> <work> <directive>: the gating recipe's Vivado build (the train's gbuild) at 8x8/1if: the argv
# rprep.sh wrote in <work>/argv.txt, its flow flags with <directive> as the placement directive, --eth-port e2,
# through milan_soc.py --build into <work>/build_<directive>. Run inside vivado-slot.sh.
set -u
L=$1; W=$2; D=$3; STEM=endstation_ax7101_8x8; O=$W/build_$D
mkdir -p "$O"; date -Iseconds > "$O.start"
TH=${VIV_THREADS:-8}
source <scratch>/bin/env.sh
export HOME=<home> XILINXD_LICENSE_FILE=<home>/.Xilinx/Xilinx.lic
source <home>/Xilinx2/2026.1/Vivado/settings64.sh
cd "$L/sw/litex" || { echo 3 > "$O.rc"; exit 3; }
mapfile -t ARGV < "$W/argv.txt"
echo "head $(git -C "$L" rev-parse HEAD); status $(git -C "$L" status --porcelain | tr '\n' ' ')"
sha256sum "$L/configs/$STEM.yaml" "$L/sw/builder/out/$STEM/ctrl_app.elf" "$L/sw/builder/out/$STEM/soc_params.json"
FLOW=(--synth-directive AreaOptimized_high --opt-directive ExploreArea --place-directive "$D")
echo "python3 milan_soc.py ${ARGV[*]} --eth-port e2 ... ${FLOW[*]} --build --output-dir $O"
python3 milan_soc.py "${ARGV[@]}" --eth-port e2 --entity-gen-dir "$L/configs/generated/$STEM" "${FLOW[@]}" \
  --no-compile-software --vivado-max-threads "$TH" --build --output-dir "$O"
rc=$?
echo "$rc" > "$O.rc"; date -Iseconds > "$O.end"
echo "== END-OF-BUILD rc=$rc $(date -Iseconds)"
exit $rc
