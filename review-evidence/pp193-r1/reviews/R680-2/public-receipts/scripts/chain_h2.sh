#!/usr/bin/env bash
# head 57fb7dd2, runner 2: once the base chain is done, the second half of the
# campaigns in head-pp-c2 at --jobs 2
S=<scratch>/r2
until [ -f $S/rec/base-CHAIN.done ]; do sleep 30; done
bash $S/scripts/run_camps.sh $S/head-pp-c2 $S/rec/head-camps2 2 dispatch ctr gsi name_wr name_state elab_mutants
echo done > $S/rec/head-H2.done
