#!/usr/bin/env bash
# lay out the records as they appear in the output directory
S=<scratch>
R=$S/rec; T=$S/stage
bash $S/scripts/merge_camps.sh
rm -rf $T; mkdir -p $T/gates $T/consumers $T/ooc $T/campaigns $T/scripts
cp -r $R/base-gates $T/gates/base; cp -r $R/head-gates $T/gates/head; cp -r $R/head2-gates $T/gates/head-final
cp -r $R/base-cons $T/consumers/base; cp -r $R/head-cons $T/consumers/head; cp -r $R/head2-cons $T/consumers/head-final
cp $R/compare-cons-large.txt $T/consumers/
cp -r $R/base-ooc $T/ooc/base; cp -r $R/head-ooc $T/ooc/head
cp -r $R/camps/base $R/camps/head $R/camps/head-final $R/camps/SOURCES.txt $T/campaigns/
mkdir -p $T/campaigns/base/work $T/campaigns/head/work $T/campaigns/head-final/work
cp -r $R/base-camps/work/srp_top $T/campaigns/base/work/; cp -r $R/head-camps/work/srp_top $T/campaigns/head/work/
cp -r $R/base-camps-d/work/gsi $T/campaigns/base/work/; cp -r $R/head-camps/work/gsi $T/campaigns/head/work/; cp -r $R/head2-camps/work/gsi $T/campaigns/head-final/work/
cp -r $R/newchecks-at-base $R/head-extra $T/
mkdir -p $T/dev; cp -r $R/dev-camp3 $T/dev/listener-arms-campaign; cp $R/dev-camp3.log $T/dev/listener-arms-campaign.log
cp $R/wip-pptop.log $R/wip-pptop.rc $T/dev/ 2>/dev/null
cp -r $R/compare $T/compare; cp $R/compare-cons-*-checklines.diff $T/compare/ 2>/dev/null
cp $R/memwatch.log $T/
cp $S/scripts/*.sh $S/scripts/*.py $T/scripts/
cp $S/head.sha $T/head-67b90c17.sha; cp $S/head2.sha $T/head-final.sha
mkdir -p $T/merge-check; cp $S/merge-check/rec/MERGE.txt $S/merge-check/rec/gsi.{log,rc,sec} $S/merge-check/rec/pp_top.{log,rc,sec} $T/merge-check/
