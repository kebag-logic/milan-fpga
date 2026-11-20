#!/usr/bin/env bash
# fitexport.sh <1x1|8x8> <head>: fitpoint.sh's steps before Vivado, at <head>: a clean clone, the split boot for the
# stand-in image, route_image (the split recipe's export, its identity gate and the integrated script). Whether the
# routes are owed is then read from the export against step 12's (gateware13.py); fitpoint.sh resumes from here.
set -u
P=$1; H=$2; T=<scratch>; S=$T/r5fit15; X=$S/tools
if [ "$P" = 1x1 ]; then b=boot.sh; stem=endstation_ax7101_1x1_tdm8; ri=route_image.sh; W=$S/route; else
  b=boot8.sh; stem=endstation_ax7101_8x8; ri=route_image8.sh; W=$S/route8; fi
say() { echo "[export $P $(date +%T)] $*"; }
mkdir -p "$W"
[ -d $S/repo$P ] || bash $T/bin/clone.sh "$H" $S/repo$P > $S/clone-$P.log 2>&1 || { say "clone failed"; exit 2; }
say "head $(git -C $S/repo$P rev-parse HEAD)"
bash $X/$b $stem $S/tmp/boot-$P > $W.boot.log 2>&1; say "boot rc=$(cat $S/tmp/boot-$P.rc 2>/dev/null)"
[ "$(cat $S/tmp/boot-$P.rc 2>/dev/null)" = 0 ] || exit 3
bash $X/$ri $S/repo$P > $W.image.log 2>&1 || { say "route_image rc=$?"; exit 4; }
say "route_image done: $(tail -3 $W.image.log | tr '\n' ' ')"
echo done > $W/EXPORT_DONE
