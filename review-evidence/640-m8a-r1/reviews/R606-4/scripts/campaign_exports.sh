#!/bin/bash
# Gateware exports (no Vivado, no software) of both AX7101 shipping configs: default at the
# reviewed head and at dev c6bd08c6, then split exports at the head with the head's own linked
# images. Within one tree the exports run one at a time: the end-station build regenerates
# shared tracked files and must not overlap another build in the same tree.
# usage: campaign_exports.sh <dev-tree>  (PACKET and CLONE exported)
set -u
. "$PACKET/scripts/env.sh"
export PATH=$S/litex-venv/bin:$PATH
dev=$1
R=$PACKET/receipts/exports
E=$S/exports
mkdir -p "$R" "$E"
exp() { tag=$1; tree=$2; shift 2
  python3 "$PACKET/scripts/soc_export.py" "$tree" "$@" > "$R/$tag.log" 2>&1; echo $? > "$R/$tag.rc"; }
(
  exp dev-default-1x1 "$dev" endstation_ax7101_1x1_tdm8 "$E/dev-default-1x1"
  exp dev-default-8x8 "$dev" endstation_ax7101_8x8 "$E/dev-default-8x8"
) &
(
  exp head-default-1x1 "$CLONE" endstation_ax7101_1x1_tdm8 "$E/head-default-1x1"
  exp head-default-8x8 "$CLONE" endstation_ax7101_8x8 "$E/head-default-8x8"
  exp head-split-1x1 "$CLONE" endstation_ax7101_1x1_tdm8 "$E/head-split-1x1" \
      --ctrl-mailbox --ctrl-firmware "$S/links_head/1x1_tdm8_i1_split/ctrl_app.elf"
  exp head-split-8x8 "$CLONE" endstation_ax7101_8x8 "$E/head-split-8x8" \
      --ctrl-mailbox --ctrl-firmware "$S/links_head/8x8_i2_split/ctrl_app.elf"
) &
wait
for shape in 1x1 8x8; do
  python3 "$PACKET/scripts/export_digest.py" "$E/dev-default-$shape" "$E/head-default-$shape" \
    > "$R/digest-default-$shape.txt" 2>&1
  echo $? > "$R/digest-default-$shape.rc"
done
echo done > "$R/DONE"
