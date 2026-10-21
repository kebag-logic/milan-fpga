#!/usr/bin/env bash
S=<scratch>
setsid bash $S/scripts/watch_primary.sh 638809 $S/rec/base-camps $S/rec/base-camps-d > /dev/null 2>&1 < /dev/null &
bash $S/scripts/helper_camps.sh $S/base-pp-c2 $S/rec/base-camps $S/rec/base-camps-d 2 elab_mutants name_state name_wr gsi ctr dispatch aecp
