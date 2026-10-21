#!/usr/bin/env bash
S=<scratch>
. $S/scripts/env.sh
cd $S/wip/tb/pp_top || exit 2
t0=$(date +%s)
make > $S/rec/wip-pptop.log 2>&1
echo $? > $S/rec/wip-pptop.rc
echo $(( $(date +%s) - t0 )) > $S/rec/wip-pptop.sec
