#!/usr/bin/env bash
# resume of route_chain.sh after the 08:55 stop: the scratch parent already carries #760
# (status-760 in route-chain.txt); route h760, revert #760, then the routed cone reports
# and the head OOC cut-half reports. Every Vivado run takes the exclusive lock.
S=<data>/tmp/pp181-a635
P=$S/parent
log=$S/route-chain.txt
step() { echo "$(date -u +%FT%TZ) $*" >> $log; }
step "resume after 08:55 stop"
test "$(git -C $P rev-parse --show-toplevel)" = "$P" || { step "parent toplevel wrong"; exit 9; }
test "$(git -C $P/protocol-processor rev-parse --show-toplevel)" = "$P/protocol-processor" || { step "submodule toplevel wrong"; exit 9; }
step "gitlink $(git -C $P ls-files -s protocol-processor)"
step "status-resume $(git -C $P status --short | tr '\n' ';')"
rm -rf $S/route-h760; $S/route.sh h760; step "route h760 rc=$?"
git -C $P apply -R $S/760.patch; step "revert 760 rc=$?"
step "status-after $(git -C $P status --short | tr '\n' ';')"
. <home>/Xilinx/2026.1/Vivado/settings64.sh >/dev/null 2>&1 || true
for l in h0 h760; do
  rm -rf $S/cone/$l; mkdir -p $S/cone/$l; cd $S/cone/$l
  flock -x $VIVADO_LOCK <home>/Xilinx/2026.1/Vivado/bin/vivado -mode batch -nojournal -log cone.log \
    -source $S/route_cone.tcl -tclargs $S/route-$l/work/ax7101/gateware/alinx_ax7101_route.dcp > vivado.out 2>&1
  echo "rc=$?" > rc.txt; step "cone $l $(cat rc.txt)"
done
rm -rf $S/ooc/cut-1x1 $S/ooc/cut-8x8
$S/ooc_run2.sh <data>/lanes/pp181-cut $S/ooc/cut-1x1 1 1; step "ooc cut-1x1 $(cat $S/ooc/cut-1x1/rc.txt)"
$S/ooc_run2.sh <data>/lanes/pp181-cut $S/ooc/cut-8x8 8 8; step "ooc cut-8x8 $(cat $S/ooc/cut-8x8/rc.txt)"
step CHAIN-DONE
