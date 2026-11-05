#!/usr/bin/env bash
# ooc.sh <sha> <tag>: OOC synthesis of milan_datapath (syn/ooc/milan_datapath_ooc.tcl) on a fresh clean clone at <sha>.
set -u
sha=$1; tag=$2; A=$VALIDATION_STORAGE/839-a731/area; C=$A/clone-$tag; R=$A/run-$tag
[ -d "$C" ] || $MANAGEMENT/2026-09-23/839-a731/receipts/gates/tools/clone_at.sh "$sha" "$C" || exit 3
test "$(git -C "$C" rev-parse HEAD)" = "$sha" || exit 4
mkdir -p "$R"; cd "$R" || exit 5
source $VALIDATION_STORAGE/839-a731/env.sh
source $WORKSPACE_HOME/Xilinx/2026.1/Vivado/settings64.sh
export TAG=$tag
{ echo "# head $sha tag $tag"; $MANAGEMENT/2026-09-23/vivado-slot.sh vivado -mode batch -nojournal -log vivado-$tag.log -source "$C/syn/ooc/milan_datapath_ooc.tcl"; } > run-$tag.out 2>&1
echo $? > rc
git -C "$C" status --porcelain > tree-after.txt
