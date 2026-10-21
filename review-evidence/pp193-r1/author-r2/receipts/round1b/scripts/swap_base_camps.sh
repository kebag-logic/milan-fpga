#!/usr/bin/env bash
# once the base srp_top campaign has its rc, stop the runner (which started
# the next campaign under the tmpfs TMPDIR) and run the rest under env.sh's
# disk TMPDIR, into the same record directory
S=<scratch>
until [ -f $S/rec/base-camps/srp_top.rc ]; do sleep 15; done
pkill -f "run_camps.sh $S/base-pp-c" ; sleep 2
pkill -f "rec/base-camps/work/acmp" ; sleep 5
pkill -f "rec/base-camps/work/acmp" ; sleep 2
rm -rf $S/rec/base-camps/work/acmp $S/rec/base-camps/acmp.log
echo "swapped at $(date -Is)" > $S/rec/base-camps/SWAP.txt
bash $S/scripts/run_camps.sh $S/base-pp-c $S/rec/base-camps 3 acmp notify d3 aecp dispatch ctr gsi name_wr name_state elab_mutants
