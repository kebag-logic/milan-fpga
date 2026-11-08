#!/usr/bin/env bash
# paths_round1.sh: round 1's saved routed checkpoints, one paths.sh run each, one after another: the recipe's
# three directives at a566d4f9 (the record's route set) and the shipping (build-dev, ExtraPostPlacementOpt) routes at
# a566d4f9 and 2d939d2d. Records each checkpoint's sha256 first.
set -u
here=$(cd "$(dirname "$0")" && pwd); S=$VALIDATION_STORAGE/scratch/851-a744b/paths-r1
R1=$VALIDATION_STORAGE/scratch/851-a744/w; B=$HOME/litex-milan/work
while read -r name dcp; do
  mkdir -p "$S/$name"; sha256sum "$dcp" | awk '{print $1}' > "$S/$name/dcp.sha256"; stat -c %s "$dcp" > "$S/$name/dcp.bytes"
  echo "== $name $(date -u +%FT%TZ)"; bash "$here/paths.sh" "$dcp" "$S/$name" > "$S/$name.log" 2>&1; echo "== $name rc=$? $(date -u +%FT%TZ)"
done <<LIST
recipe-eto-a566d4f9 $R1/ax7101-ExtraTimingOpt/alinx_ax7101_route.dcp
recipe-eppo-a566d4f9 $R1/ax7101/gateware/alinx_ax7101_route.dcp
recipe-aslh-a566d4f9 $R1/ax7101-AltSpreadLogic_high/alinx_ax7101_route.dcp
ship-eppo-2d939d2d $B/build_ax7101_eppo_meas851a744h2d939d/gateware/alinx_ax7101_route.dcp
ship-eppo-a566d4f9 $B/build_ax7101_eppo_meas851a744ha566d4/gateware/alinx_ax7101_route.dcp
LIST
echo DONE
