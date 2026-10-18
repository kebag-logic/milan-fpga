#!/usr/bin/env bash
# after the 10:57 crash: the head OOC 8x8 cut-half reports (cut mid-run), then the base+#760 route.
S=<data>/tmp/pp181-a635
log=$S/route-chain.txt
step() { echo "$(date -u +%FT%TZ) $*" >> $log; }
step "resume after 10:57 crash"
rm -rf $S/ooc/cut-8x8
$S/ooc_run2.sh <data>/lanes/pp181-cut $S/ooc/cut-8x8 8 8; step "ooc cut-8x8 $(cat $S/ooc/cut-8x8/rc.txt)"
$S/route_base760.sh
step CHAIN3-DONE
