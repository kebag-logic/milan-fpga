#!/usr/bin/env bash
# like-for-like comparison: route-1x1 at processor base 22c139a4 with #760 applied,
# then back to the head gitlink. Run after route_chain2.sh (CHAIN-DONE). Exclusive lock.
S=<data>/tmp/pp181-a635
P=$S/parent; M=$P/protocol-processor
BASE=22c139a4323bc96c779d13e3f6774480c5fb9b75
HEAD=07447acb5244d6d230ee61e1ad172cd4da4a007c
log=$S/route-chain.txt
step() { echo "$(date -u +%FT%TZ) $*" >> $log; }
test "$(git -C $P rev-parse --show-toplevel)" = "$P" || { step "parent toplevel wrong"; exit 9; }
test "$(git -C $M rev-parse --show-toplevel)" = "$M" || { step "submodule toplevel wrong"; exit 9; }
git -C $M checkout -q --detach $BASE && git -C $P add protocol-processor; step "gitlink base $(git -C $P ls-files -s protocol-processor)"
git -C $P apply $S/760.patch; step "apply 760 rc=$?"
rm -rf $S/route-base760; $S/route.sh base760; step "route base760 rc=$?"
git -C $P apply -R $S/760.patch; step "revert 760 rc=$?"
git -C $M checkout -q --detach $HEAD && git -C $P add protocol-processor; step "gitlink restored $(git -C $P ls-files -s protocol-processor)"
step "status-after $(git -C $P status --short | tr '\n' ';')"
. <home>/Xilinx/2026.1/Vivado/settings64.sh >/dev/null 2>&1 || true
rm -rf $S/cone/base760; mkdir -p $S/cone/base760; cd $S/cone/base760
flock -x $VIVADO_LOCK <home>/Xilinx/2026.1/Vivado/bin/vivado -mode batch -nojournal -log cone.log \
  -source $S/route_cone.tcl -tclargs $S/route-base760/work/ax7101/gateware/alinx_ax7101_route.dcp > vivado.out 2>&1
echo "rc=$?" > rc.txt; step "cone base760 $(cat rc.txt)"
step BASE760-DONE
