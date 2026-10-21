#!/usr/bin/env bash
# head runner A keeps srp_top, acmp and notify; once notify's rc is written,
# stop its group (it has just started d3), then a helper takes runner B's
# remaining campaigns from the other end, with a watcher on runner B
S=<scratch>
until [ -f $S/rec/head-camps/notify.rc ]; do sleep 10; done
kill -TERM -- -1247013; sleep 5; kill -KILL -- -1247013 2>/dev/null
rm -rf $S/rec/head-camps/work/d3 $S/rec/head-camps/d3.log
echo "runner A stopped after notify at $(date -Is)" > $S/rec/head-camps/SPLIT.txt
setsid bash $S/scripts/watch_primary.sh 1731358 $S/rec/head-camps $S/rec/head-camps-d > /dev/null 2>&1 < /dev/null &
bash $S/scripts/helper_camps.sh $S/head-pp-c $S/rec/head-camps $S/rec/head-camps-d 2 d3 elab_mutants name_state name_wr gsi ctr dispatch
