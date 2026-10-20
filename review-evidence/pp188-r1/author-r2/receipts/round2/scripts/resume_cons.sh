#!/usr/bin/env bash
# Resume after the host reset: the head consumer gate milan_dp (cut mid-run)
# and the OOC head gates, at the staged round-2 head.
set -u
S=<scratch>
P=$S/parent
PP=$P/protocol-processor
[ "$(git -C $P rev-parse --show-toplevel)" = "$P" ] || exit 3
[ "$(git -C $PP rev-parse --show-toplevel)" = "$PP" ] || exit 3
[ "$(git -C $PP rev-parse HEAD)" = "$(cat $S/head2.sha)" ] || exit 6
rm -f $S/rec2/cons-head/ALL.done
bash $S/scripts/run_consumers.sh $S/rec2/cons-head.resume milan_dp
mv $S/rec2/cons-head.resume/milan_dp.* $S/rec2/cons-head/ && cp $S/rec2/cons-head.resume/STATE.txt $S/rec2/cons-head/STATE-resume.txt
echo done > $S/rec2/cons-head/ALL.done
bash $S/scripts/run_ooc.sh $S/rec2/ooc-head
echo done > $S/rec2/CHAIN.done
