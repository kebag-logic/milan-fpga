#!/usr/bin/env bash
# route-1x1 at the final head: without #760, then with it (patch dev..22840662,
# applied to the scratch parent's working tree only), then the routed cone reports.
# Every Vivado run takes the exclusive lock (route.sh, route_cone.tcl below).
S=<data>/tmp/pp181-a635
P=$S/parent
log=$S/route-chain.txt
: > $log
step() { echo "$(date -u +%FT%TZ) $*" >> $log; }
test "$(git -C $P rev-parse --show-toplevel)" = "$P" || { step "parent toplevel wrong"; exit 9; }
test "$(git -C $P/protocol-processor rev-parse --show-toplevel)" = "$P/protocol-processor" || { step "submodule toplevel wrong"; exit 9; }
step "gitlink $(git -C $P ls-files -s protocol-processor)"
step "status-before $(git -C $P status --short | tr '\n' ';')"
rm -rf $S/route-h0; $S/route.sh h0; step "route h0 rc=$?"
git -C $P apply $S/760.patch; step "apply 760 rc=$?"
step "status-760 $(git -C $P status --short | tr '\n' ';')"
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
step CHAIN-DONE
