#!/usr/bin/env bash
# After the base consumer pass: base xvlog and ooc, then stage the head as the
# gitlink and run every consumer gate, xvlog and ooc at head.
set -u
S=<scratch>
P=$S/parent
PP=$P/protocol-processor
HEAD_SHA=$(cat $S/head.sha)
until [ -f $S/rec/cons-base/ALL.done ]; do sleep 30; done
mv $S/rec/cons-base/ALL.done $S/rec/cons-base/ALL.first.done
cp $S/rec/cons-base/STATE.txt $S/rec/cons-base/STATE.first.txt
bash $S/scripts/run_consumers.sh $S/rec/cons-base xvlog
bash $S/scripts/run_ooc.sh $S/rec/ooc-base
# stage the head
[ "$(git -C $P rev-parse --show-toplevel)" = "$P" ] || exit 3
[ "$(git -C $PP rev-parse --show-toplevel)" = "$PP" ] || exit 3
git -C $PP fetch -q <lane> 188-189-listener || exit 4
git -C $PP checkout -q "$HEAD_SHA" || exit 5
[ "$(git -C $PP rev-parse HEAD)" = "$HEAD_SHA" ] || exit 6
git -C $P add protocol-processor || exit 7
bash $S/scripts/run_consumers.sh $S/rec/cons-head
bash $S/scripts/run_ooc.sh $S/rec/ooc-head
echo done > $S/rec/CHAIN.done
