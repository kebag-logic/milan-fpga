#!/usr/bin/env bash
# gchain.sh <1x1|8x8> <head> <directive> <label>: one split image of <head> by the S12b gating lane's recipe (the train's
# gchain15.sh, boot.sh, gprep.sh and gbuild.sh, copied with only the scratch path changed; the directive a parameter):
# a clean clone of <head>, the split boot simulation (its provisional image and runtime are the stand-in inputs),
# gprep.sh (the builder's split placement, the stand-in export, the flash port's map, ctrl_plat_image.py --interfaces 1),
# then gbuild.sh through vivado-slot.sh: the recipe argv, --eth-port e2, <directive>, threads min(the inherited CPUs, 16),
# --build. Then the image identity gate, the artifacts' sha256 and #818's floor. Clone and boot dir are per <label>.
set -u
P=$1; H=$2; D=$3; LBL=$4; T=<scratch>; G=$T/gate; X=$G/tools
V=<home>/milan-fpga-management/2026-09-23/vivado-slot.sh
if [ "$P" = 1x1 ]; then STEM=endstation_ax7101_1x1_tdm8; else STEM=endstation_ax7101_8x8; fi
C=$G/clones/$LBL-$P; B=$G/tmp/gboot-$LBL-$P; W=$G/work/$LBL-$P; O=$W/build_$D
export MAKEFLAGS="-j8 --no-print-directory"
step() { echo "=== $* $(date -Iseconds)"; "$@"; local rc=$?; echo "=== rc=$rc $1 $(date -Iseconds)"; [ $rc -eq 0 ] || exit $rc; }
mkdir -p $G/clones $G/tmp $G/work
[ -d "$C" ] || step bash $T/bin/clone.sh "$H" "$C"
[ -f "$B/BOOT_DONE" ] || { step bash $X/boot.sh "$C" "$B" "$STEM"; touch "$B/BOOT_DONE"; }
[ -f "$W/PREP_DONE" ] || { step bash $X/gprep.sh "$C" "$STEM" "$B" "$W"; touch "$W/PREP_DONE"; }
step flock $T/route.lock "$V" bash $X/gbuild.sh "$C" "$STEM" "$D" "$W"   # one route of this lane at a time
<home>/litex-milan/venv/bin/python3 "$C/sw/litex/check_image_identity.py" "$O" > "$O.identity.log" 2>&1
echo "identity rc=$?: $(tail -1 "$O.identity.log")"
( cd "$O" && sha256sum gateware/alinx_ax7101.bit gateware/alinx_ax7101.bin aem_desc.bin csr.csv flashboot_layout.json image_manifest.json 2>/dev/null ) > "$O.artifacts.sha256"
sha256sum "$C/sw/builder/out/$STEM/ctrl_app.elf" >> "$O.artifacts.sha256"
cat "$O.artifacts.sha256"
python3 -I $T/bin/signoff.py "$O/gateware" > "$O.signoff.txt" 2>&1; echo "signoff rc=$?"; cat "$O.signoff.txt"
echo GATE_DONE > "$O.GATE_DONE"
