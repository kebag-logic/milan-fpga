#!/usr/bin/env bash
# carry.sh <1x1|8x8> <head>: the gating recipe's inputs of one image at <head>, without Vivado: a clean clone, gprep.sh
# (the builder's split placement, the stand-in export, the flash map, the platform image link) reusing the 822e3af0
# chain's split boot runtime, then the recipe's milan_soc.py command without --build (gbuild.sh's argv, --eth-port e2,
# the ExtraPostPlacementOpt flow, no Vivado) into <work>/export. compare_inputs.py then holds every input to the
# 822e3af0 build's.
set -u
P=$1; H=$2; T=<scratch>; G=$T/gate; X=$G/tools
if [ "$P" = 1x1 ]; then STEM=endstation_ax7101_1x1_tdm8; else STEM=endstation_ax7101_8x8; fi
C=$G/clones/carry-$H-$P; B=$G/tmp/gboot-flip-$P; W=$G/work/carry-$H-$P
[ -d "$C" ] || bash $T/bin/clone.sh "$H" "$C" > /dev/null
bash $X/gprep.sh "$C" "$STEM" "$B" "$W" || exit 3
source $T/bin/env.sh
cd "$C/sw/litex" || exit 3
mapfile -t ARGV < "$W/argv.txt"
FLOW=(--synth-directive AreaOptimized_high --opt-directive ExploreArea --place-directive ExtraPostPlacementOpt)
python3 milan_soc.py "${ARGV[@]}" --eth-port e2 --entity-gen-dir "$C/configs/generated/$STEM" "${FLOW[@]}" \
  --no-compile-software --vivado-max-threads 16 --output-dir "$W/export" > "$W/export.log" 2>&1; echo "export rc=$?"
