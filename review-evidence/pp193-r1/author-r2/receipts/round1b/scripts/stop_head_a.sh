#!/usr/bin/env bash
# runner A (process group 1247013) keeps srp_top, acmp and notify; once notify's
# rc is written, stop the group (it has just started d3, which runner B owns)
S=<scratch>
until [ -f $S/rec/head-camps/notify.rc ]; do sleep 10; done
kill -TERM -- -1247013; sleep 5; kill -KILL -- -1247013 2>/dev/null
rm -rf $S/rec/head-camps/work/d3 $S/rec/head-camps/d3.log
echo "runner A stopped after notify at $(date -Is)" > $S/rec/head-camps/SPLIT.txt
