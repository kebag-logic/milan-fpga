#!/usr/bin/env bash
# collect3.sh: round 3's route receipts (the export at a2690e68, the three directives from its one synthesis
# checkpoint), with route_dir from collect.sh: host paths replaced (receipt.py), large reports reduced to their
# summary lines with the full file's size and sha256
set -uo pipefail
S=<scratch>; O=<home>/milan-fpga-management/2026-09-23/665s9-a760/receipts/r3
R="python3 $S/tools/receipt.py"; H=a2690e682d929e6d3811006f961a24361827c596
eval "$(sed -n '/^big() {/,/^}/p; /^route_dir() {/,/^}/p' $S/tools/collect.sh)"
mkdir -p "$S/tmp" "$O/route"
for d in ExtraPostPlacementOpt ExtraTimingOpt AltSpreadLogic_high; do
  route_dir $S/route/split-$d "$O/route/split-$d" $H "the split route's one synthesis checkpoint, placed at $d (#818; ExtraPostPlacementOpt is the recipe's)"
  $R $S/route/split-$d/baseline_implementation.tcl "$O/route/split-$d/baseline_implementation.tcl" $H "tools/prep_directives3.py" > /dev/null
  $R $S/route/slot-$d.log "$O/route/slot-$d.log" $H "vivado-slot.sh tools/route_directive.sh $d" > /dev/null
done
$R $S/route/route_image.log "$O/route/route_image.log" $H "tools/route_image.sh <clean clone of the head>" > /dev/null
$R $S/route/slot-split.log "$O/route/slot-split.log" $H "vivado-slot.sh tools/route_one.sh split (cut by the 08:23 host reset during placement)" > /dev/null
$R $S/route/third.log "$O/route/third.log" $H "tools/third3.sh" > /dev/null
$R $S/route/gate-check-shipping-view.log "$O/route/gate-check-shipping-view.log" $H "syn/ooc/pp_resource_gate.py check <the export's gateware, the recipe directive's reports> --endpoint route-1x1 --placement full-split --shipping-selection" > /dev/null
$R $S/route/split/image_manifest.json "$O/route/split-image_manifest.json" $H "the split image's manifest" > /dev/null
(cd $S/route/split/gateware && sha256sum alinx_ax7101.v baseline_integrated.tcl alinx_ax7101_rom_bank*.init alinx_ax7101.xdc) > $S/tmp/inputs.txt
$R $S/tmp/inputs.txt "$O/route/split-inputs.sha256" $H "sha256 of the exported netlist, integrated script, rom bank images and constraints" > /dev/null
big $S/route/split/gateware/alinx_ax7101_synth.dcp "$O/route/alinx_ax7101_synth.dcp.sha256"
grep -n "write_checkpoint\|Writing placer database\|synth_design completed\|Finished Writing" $S/route/split/gateware/baseline.log | head -20 > $S/tmp/synthlog.txt
$R $S/tmp/synthlog.txt "$O/route/split-synthesis-checkpoint-lines.txt" $H "the recipe session's checkpoint lines from baseline.log (the session the reset cut)" > /dev/null
for d in ExtraPostPlacementOpt ExtraTimingOpt AltSpreadLogic_high; do echo "== $d"; python3 $S/tools/signoff.py $S/route/split-$d; done > $S/tmp/signoff-all.txt 2>&1
$R $S/tmp/signoff-all.txt "$O/route/signoff-all.txt" $H "tools/signoff.py <route dir>, each directive" > /dev/null
echo collected
