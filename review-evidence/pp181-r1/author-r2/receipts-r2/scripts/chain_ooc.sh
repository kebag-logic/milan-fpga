#!/usr/bin/env bash
# Round 2 OOC: the unchanged complete-processor recipe at 10 ns plus the #181 cone
# queries (ooc_cone2.tcl), at head (the lane) and base 08ae0013 (a clean export),
# 1x1 and 8x8; every Vivado run under the exclusive lock (ooc_run2.sh).
S=<data>/tmp/pp181-a635; R=$S/r2
log=$R/chain-ooc.txt
step() { echo "$(date -u +%FT%TZ) $*" >> $log; }
step "head $(git -C <data>/lanes/pp181-cut rev-parse HEAD)"
for t in "head <data>/lanes/pp181-cut" "base $R/base-tree"; do
  set -- $t
  for s in "1 1" "8 8"; do
    o=$R/ooc/$1-${s% *}x${s#* }; rm -rf $o
    $S/ooc_run2.sh $2 $o $s; step "ooc $1 ${s% *}x${s#* } $(cat $o/rc.txt)"
  done
done
step OOC-DONE
