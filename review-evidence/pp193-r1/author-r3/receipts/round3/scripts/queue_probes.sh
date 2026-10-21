#!/usr/bin/env bash
# after R679-2's probes: the head's new checks against the base RTL, and the
# role-shift probe at the base and at the head, one build at a time
S=<scratch>/r3
H=$(cat $S/head.sha)
B=7b424cdfe111a426f00517ff471246b4b9650726
until [ -f $S/rec/r679-2-probes-base/DONE ]; do sleep 10; done
rm -rf $S/rec/q; mkdir -p $S/rec/q/head-tree $S/rec/q/base-tree
git -C <lane> archive $H | tar -x -C $S/rec/q/head-tree
git -C <lane> archive $B | tar -x -C $S/rec/q/base-tree
for t in head-tree base-tree; do (cd $S/rec/q/$t && git init -q && git add -A && git -c user.name=x -c user.email=x@y commit -q -m x); done
bash $S/scripts/tests_on_rtl.sh $S/rec/newchecks-at-base $S/rec/q/head-tree $S/rec/q/base-tree > $S/rec/newchecks-at-base.out 2>&1
bash $S/scripts/probe_tree.sh $S/rec/role-shift-base $S/rec/q/base-tree $S/probes/role_shift_probe.py > $S/rec/role-shift-base.out 2>&1
bash $S/scripts/probe_tree.sh $S/rec/role-shift-head $S/rec/q/head-tree $S/probes/role_shift_probe.py > $S/rec/role-shift-head.out 2>&1
echo done > $S/rec/q/DONE
