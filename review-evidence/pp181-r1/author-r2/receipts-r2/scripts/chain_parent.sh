#!/usr/bin/env bash
# Round 2, the scratch parent (milan-fpga dev 7d79ffb2, never committed or pushed):
# base 08ae0013 = parent consumer gates, then the processor gates in its submodule;
# head = parent consumer gates; then route-1x1 with #760 (recipe unchanged, exclusive
# Vivado lock) and the routed cone reports. One step per line in chain.txt.
S=<data>/tmp/pp181-a635; R=$S/r2; P=$S/parent; M=$P/protocol-processor
BASE=08ae00130f096f241463172c4781885934400ee4
HEAD=$(cat $R/head-sha.txt)
log=$R/chain.txt
step() { echo "$(date -u +%FT%TZ) $*" >> $log; }
top() { test "$(git -C $P rev-parse --show-toplevel)" = "$P" && test "$(git -C $M rev-parse --show-toplevel)" = "$M"; }
top || { step "toplevel wrong"; exit 9; }
step "parent $(git -C $P rev-parse HEAD) status-before $(git -C $P status --short | tr '\n' ';')"
git -C $M checkout -q --detach $BASE && git -C $P add protocol-processor; step "gitlink base $(git -C $P ls-files -s protocol-processor)"
$S/parent_gates.sh $R/pgates/base; step "parent gates base done"
top || { step "toplevel wrong"; exit 9; }
$R/gates.sh $M base; step "processor gates base done"
top || { step "toplevel wrong"; exit 9; }
git -C $M checkout -q --detach $HEAD && git -C $P add protocol-processor; step "gitlink head $(git -C $P ls-files -s protocol-processor)"
$S/parent_gates.sh $R/pgates/head; step "parent gates head done"
top || { step "toplevel wrong"; exit 9; }
step "760.patch sha256 $(sha256sum < $S/760.patch | cut -c1-64)"
git -C $P apply $S/760.patch; step "apply 760 rc=$?"
step "status-760 $(git -C $P status --short | tr '\n' ';')"
rm -rf $S/route-r2-head760; $R/route.sh r2-head760; step "route r2-head760 rc=$?"
git -C $P apply -R $S/760.patch; step "revert 760 rc=$?"
step "status-after $(git -C $P status --short | tr '\n' ';')"
. <home>/Xilinx/2026.1/Vivado/settings64.sh >/dev/null 2>&1 || true
rm -rf $R/cone/head760; mkdir -p $R/cone/head760; cd $R/cone/head760
flock -x $VIVADO_LOCK <home>/Xilinx/2026.1/Vivado/bin/vivado -mode batch -nojournal -log cone.log \
  -source $S/route_cone.tcl -tclargs $S/route-r2-head760/work/ax7101/gateware/alinx_ax7101_route.dcp > vivado.out 2>&1
echo "rc=$?" > rc.txt; step "cone head760 $(cat rc.txt)"
step CHAIN-DONE
