#!/usr/bin/env bash
# third.sh: #818's third placement directive once one of the two running implementations has ended (at most two at a time)
S=<scratch>
until [ -f $S/route/split/gateware/route.rc ] || [ -f $S/route/split-ExtraTimingOpt/route.rc ]; do sleep 30; done
echo "$(date -Iseconds) one ended: split $(cat $S/route/split/gateware/route.rc 2>/dev/null) ExtraTimingOpt $(cat $S/route/split-ExtraTimingOpt/route.rc 2>/dev/null)"
<home>/milan-fpga-management/2026-09-23/vivado-slot.sh $S/tools/route_directive.sh AltSpreadLogic_high > $S/route/slot-AltSpreadLogic_high.log 2>&1
echo "$(date -Iseconds) AltSpreadLogic_high rc=$(cat $S/route/split-AltSpreadLogic_high/route.rc)"
