#!/usr/bin/env bash
# gchain13.sh <1x1|8x8> <head>: one GATING bench bitstream of the train at <head>, by the S12b gating lane's own recipe
# (its gchain.sh, gprep.sh and gbuild.sh, copied with only their scratch path changed): a clean clone of <head>, the
# split boot simulation (its provisional image and runtime are the stand-in inputs), gprep.sh (the builder's split
# placement, the stand-in export, the flash port's map, ctrl_plat_image.py --interfaces 1), then gbuild.sh through
# vivado-slot.sh: the recipe argv, --eth-port e2, ExtraPostPlacementOpt, threads min(the inherited CPUs, 16), --build.
# Then the image identity gate, the artifacts' sha256 and the signoff floors (r5fit12's signoff.py).
set -u
P=$1; H=$2; T=<scratch>; G=$T/gate13; X=$G/tools
V=<management>/2026-09-23/vivado-slot.sh
if [ "$P" = 1x1 ]; then STEM=endstation_ax7101_1x1_tdm8; else STEM=endstation_ax7101_8x8; fi
C=$G/clones/g$P; B=$G/tmp/gboot-$P; W=$G/work/g$P; D=ExtraPostPlacementOpt; O=$W/build_$D
export MAKEFLAGS="-j8 --no-print-directory"
step() { echo "=== $* $(date -Iseconds)"; "$@"; local rc=$?; echo "=== rc=$rc $1 $(date -Iseconds)"; [ $rc -eq 0 ] || exit $rc; }
[ -d "$C" ] || step bash $T/bin/clone.sh "$H" "$C"
step bash $X/boot.sh "$C" "$B" "$STEM"
step bash $X/gprep.sh "$C" "$STEM" "$B" "$W"
step "$V" bash $X/gbuild.sh "$C" "$STEM" "$D" "$W"
<home>/litex-milan/venv/bin/python3 "$C/sw/litex/check_image_identity.py" "$O" > "$W/identity.log" 2>&1
echo "identity: $(tail -1 "$W/identity.log")"
( cd "$O" && sha256sum gateware/alinx_ax7101.bit gateware/alinx_ax7101.bin aem_desc.bin csr.csv flashboot_layout.json image_manifest.json 2>/dev/null ) > "$W/artifacts.sha256"
sha256sum "$C/sw/builder/out/$STEM/ctrl_app.elf" >> "$W/artifacts.sha256"
cat "$W/artifacts.sha256"
python3 -I $T/r5fit12/tools/signoff.py "$O/gateware" > "$W/signoff.txt" 2>&1; echo "signoff rc=$?"; cat "$W/signoff.txt"
echo GATE_DONE > "$W/GATE_DONE"
