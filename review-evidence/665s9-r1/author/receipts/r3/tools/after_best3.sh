#!/usr/bin/env bash
# after_best3.sh: once the best-of-three chain has ended, the all-fabric endpoint route through the slot wrapper.
S=<scratch>
while [ ! -f $S/route/BEST3_DONE ]; do sleep 30; done
<home>/milan-fpga-management/2026-09-23/vivado-slot.sh $S/tools/route_one.sh fabric > $S/route/slot-fabric.log 2>&1
