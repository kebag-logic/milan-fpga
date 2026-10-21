#!/usr/bin/env bash
# The scratch parent's consumer gates, after both processor gate runs are done
# (so no more than the campaigns build beside it): the protocol-processor
# gitlink committed at each pin (fetched from the lane, never pushed), then the
# consumer gates and the out-of-context gates at the base and the head, and the
# out-of-context gates alone at processor main (the PR's base).
S=<scratch>/r2
P=$S/parent
PP=$P/protocol-processor
LANE=<lane>
until [ -f $S/rec/base-gates/ALL.done ] && [ -f $S/rec/head-gates/ALL.done ]; do sleep 30; done
[ "$(git -C $P rev-parse --show-toplevel)" = "$P" ] || exit 3
[ "$(git -C $PP rev-parse --show-toplevel)" = "$PP" ] || exit 3
git -C $PP fetch -q $LANE '+refs/heads/*:refs/remotes/lane/*' \
  '+refs/remotes/origin/main:refs/remotes/lane/origin-main' || exit 4
pin() {
  local sha=$1 label=$2
  [ "$(git -C $P rev-parse --show-toplevel)" = "$P" ] || exit 3
  [ "$(git -C $PP rev-parse --show-toplevel)" = "$PP" ] || exit 3
  git -C $PP clean -fdxq || exit 4
  git -C $PP checkout -q "$sha" || exit 5
  [ "$(git -C $PP rev-parse HEAD)" = "$sha" ] || exit 6
  [ -z "$(git -C $PP status --porcelain --ignored)" ] || exit 6
  git -C $P add protocol-processor || exit 7
  git -C $P commit -q -m "scratch: protocol-processor gitlink at $label ${sha:0:8}" || exit 7
}
pin 08023123ae2df5d802d20a9bb22cd063942845cd main
bash $S/scripts/run_ooc.sh $S/rec/main-ooc
pin 6ddfcda4c3170b8f463c8623833f7541ca8c1faf base
bash $S/scripts/run_consumers.sh $S/rec/base-cons
bash $S/scripts/run_ooc.sh $S/rec/base-ooc
pin c7c8825fd18237dd6cab2776f6e84cde5e550040 head
bash $S/scripts/run_consumers.sh $S/rec/head-cons
bash $S/scripts/run_ooc.sh $S/rec/head-ooc
echo done > $S/rec/CONS.done
