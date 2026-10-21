#!/usr/bin/env bash
# after the base consumer chain: commit the scratch parent's gitlink at the
# head (fetched from the lane, never pushed), then the consumer and OOC gates
S=<scratch>
P=$S/parent
PP=$P/protocol-processor
H=$(cat $S/head.sha)
until [ -f $S/rec/BASE-CONS.done ]; do sleep 30; done
[ "$(git -C $P rev-parse --show-toplevel)" = "$P" ] || exit 3
[ "$(git -C $PP rev-parse --show-toplevel)" = "$PP" ] || exit 3
git -C $PP clean -fdXq || exit 4
git -C $PP fetch -q <lane> "$H" || exit 4
git -C $PP checkout -q "$H" || exit 5
[ "$(git -C $PP rev-parse HEAD)" = "$H" ] || exit 6
[ -z "$(git -C $PP status --porcelain --ignored)" ] || exit 6
git -C $P add protocol-processor || exit 7
git -C $P commit -q -m "scratch: protocol-processor gitlink at head ${H:0:8}" || exit 7
bash $S/scripts/run_consumers.sh $S/rec/head-cons
bash $S/scripts/run_ooc.sh $S/rec/head-ooc
echo done > $S/rec/HEAD-CONS.done
