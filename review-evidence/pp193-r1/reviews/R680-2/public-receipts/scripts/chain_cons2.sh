#!/usr/bin/env bash
# The scratch parent's consumer and out-of-context gates at the final head
# 57fb7dd2 (the gitlink committed on top of the earlier scratch commits, never
# pushed), after the head's processor gate run is done.
S=<scratch>/r2
P=$S/parent
PP=$P/protocol-processor
LANE=<lane>
H=57fb7dd21d316ce49c305c22812de5c16d6770f6
until [ -f $S/rec/head-gates/ALL.done ]; do sleep 30; done
[ "$(git -C $P rev-parse --show-toplevel)" = "$P" ] || exit 3
[ "$(git -C $PP rev-parse --show-toplevel)" = "$PP" ] || exit 3
git -C $PP fetch -q $LANE '+refs/heads/*:refs/remotes/lane/*' || exit 4
git -C $PP clean -fdxq || exit 4
git -C $PP checkout -q "$H" || exit 5
[ "$(git -C $PP rev-parse HEAD)" = "$H" ] || exit 6
[ -z "$(git -C $PP status --porcelain --ignored)" ] || exit 6
git -C $P add protocol-processor || exit 7
git -C $P commit -q -m "scratch: protocol-processor gitlink at head ${H:0:8}" || exit 7
bash $S/scripts/run_consumers.sh $S/rec/head-cons
bash $S/scripts/run_ooc.sh $S/rec/head-ooc
echo done > $S/rec/CONS2.done
