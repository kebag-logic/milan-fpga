#!/usr/bin/env bash
# fitpoint.sh <1x1|8x8>: the AX7101 split route of one point at the candidate head (one interface), by the #810 route
# lane's recipe (S9 round 3's tools): the split boot for the stand-in image, route_image (the split recipe's export and
# its identity gate), the integrated route (synthesis, ExtraPostPlacementOpt) through vivado-slot.sh, then
# ExtraTimingOpt and AltSpreadLogic_high from its synthesis checkpoint, each through a slot, then each set's signoff.
set -u
P=$1; S=<scratch>/r5fitP11; X=$S/tools; V=<management>/2026-09-23/vivado-slot.sh
if [ "$P" = 1x1 ]; then b=boot.sh; stem=endstation_ax7101_1x1_tdm8; ri=route_image.sh; ro=route_one.sh; rd=route_directive.sh; W=$S/route; else
  b=boot8.sh; stem=endstation_ax7101_8x8; ri=route_image8.sh; ro=route_one8.sh; rd=route_directive8.sh; W=$S/route8; fi
say() { echo "[fit $P $(date +%T)] $*"; }
mkdir -p "$W"
say "head $(git -C $S/repo$P rev-parse HEAD)"
[ "$(cat $S/tmp/boot-$P.rc 2>/dev/null)" = 0 ] || bash $X/$b $stem $S/tmp/boot-$P > $W.boot.log 2>&1; say "boot rc=$(cat $S/tmp/boot-$P.rc 2>/dev/null)"
[ "$(cat $S/tmp/boot-$P.rc 2>/dev/null)" = 0 ] || exit 3
[ -f $W/split/gateware/baseline_integrated.tcl ] || bash $X/$ri $S/repo$P > $W.image.log 2>&1 || { say "route_image rc=$?"; exit 4; }
# Vivado reads its license from the account's ~/.Xilinx (the units run with a scratch HOME)
export HOME=<home> XILINXD_LICENSE_FILE=<home>/.Xilinx/Xilinx.lic
say "route_image done: $(tail -3 $W.image.log | tr '\n' ' ')"
$V bash $X/$ro split > $W/slot-split.log 2>&1
say "integrated rc=$(cat $W/split/gateware/route.rc 2>/dev/null)"
[ -f $W/split/gateware/alinx_ax7101_synth.dcp ] || { say "no synthesis checkpoint"; exit 5; }
python3 -I $X/prep_directives3.py $W
for d in ExtraTimingOpt AltSpreadLogic_high; do
  ( $V bash $X/$rd $d > $W/slot-$d.log 2>&1; say "$d rc=$(cat $W/split-$d/route.rc 2>/dev/null)" ) &
  sleep 90
done
wait
for d in split/gateware split-ExtraTimingOpt split-AltSpreadLogic_high; do
  say "signoff $d"; python3 -I $X/signoff.py $W/$d; echo "rc=$?"
done
echo done > $W/FIT_DONE
