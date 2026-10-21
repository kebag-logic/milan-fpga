#!/usr/bin/env bash
# information only: the head merged with processor main 08023123 in scratch
S=<scratch>
. $S/scripts/env.sh
M=$S/merge-check; mkdir -p $M/rec
cd $M/tree || exit 2
( t0=$(date +%s); python3 -B tb/pp_top/gsi_mutants.py --output $M/rec/gsi-work --verilator $VERILATOR --jobs 4 > $M/rec/gsi.log 2>&1; echo $? > $M/rec/gsi.rc; echo $(( $(date +%s) - t0 )) > $M/rec/gsi.sec ) &
( rsync -a --exclude=.git $M/tree/ $M/tree2/; cd $M/tree2/tb/pp_top; t0=$(date +%s); make > $M/rec/pp_top.log 2>&1; echo $? > $M/rec/pp_top.rc; echo $(( $(date +%s) - t0 )) > $M/rec/pp_top.sec ) &
wait
echo done > $M/rec/ALL.done
