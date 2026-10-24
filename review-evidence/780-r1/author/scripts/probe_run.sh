#!/usr/bin/env bash
# #780 probe (not committed): pp_shadow base leg with probe_get_avb_info_on_another_type() added, at one revision,
# in its own clean clone; prints the status the parent wrapper delivers for GET_AVB_INFO(CLOCK_DOMAIN 0).
# usage: probe_run.sh <rev>
set -u
rev=$1; h=${rev:0:8}; X=$VALIDATION_STORAGE/scratch/780-a670; D=$(cd "$(dirname "$0")" && pwd); C=$X/probe-$h
[ -d "$C" ] || bash $D/make_clone.sh "$C" "$rev" > $X/r/probe-$h.clone.log 2>&1 || exit 2
source $D/env.sh
cd $C && patch -p1 --forward < $D/../probe/pp_shadow-p780-probe.patch > $X/r/probe-$h.patch.log 2>&1 || exit 3
cd $C/tb/verilator/pp_shadow && make -j8 run-base > $X/r/probe-$h.log 2>&1; echo $? > $X/r/probe-$h.rc
