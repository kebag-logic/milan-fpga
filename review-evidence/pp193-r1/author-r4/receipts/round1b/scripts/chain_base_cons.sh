#!/usr/bin/env bash
S=<scratch>
bash $S/scripts/run_consumers.sh $S/rec/base-cons
bash $S/scripts/run_ooc.sh $S/rec/base-ooc
echo done > $S/rec/BASE-CONS.done
