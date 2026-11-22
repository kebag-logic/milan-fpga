#!/bin/sh
# run_plants.sh <checkout> <packet>: named author plants and the reviewer's own, each group its own process.
R=$1; P=$2; O=$P/scratch/plants
run() { tag=$1; shift; ( python3 -B $P/scripts/plants.py $R $O/$tag "$@" > $P/receipts/plants/$tag.log 2>&1; echo $? > $P/receipts/plants/$tag.rc ) & }
run srp2-talker srp 2 - talker-resume-drops-what-came-due,talker-resume-drops-what-came-due-at-a-phase,talker-registration-kept-across-a-reset
run srp2-unchanged srp 2 - talker-unchanged-held,talker-hold-off-adds-its-terms-at-the-latest,talker-hold-off-a-centisecond-short
run srp2-build-a srp 2 - build-resumed-drops-what-came-due,build-paused-keeps-its-due,build-paused-not-aged
run srp2-build-b srp 2 - build-paused-unreported,build-refused-second-slice-not-due,transmit-due-cleared-with-a-frame-owed
run srp1-talker srp 1 - talker-resume-drops-what-came-due,talker-resume-drops-what-came-due-at-a-phase,talker-registration-kept-across-a-reset
run srp1-8x8-talker srp 1 endstation_ax7101_8x8 talker-resume-drops-what-came-due,talker-resume-drops-what-came-due-at-a-phase,talker-registration-kept-across-a-reset
run aecp-reset aecp registration-notice-kept-across-a-reset
run own2 own 2 - r875-whole-build-keeps-its-due,r875-reset-records-ready,r875-reset-clears-source-0-only
run own1 own 1 - r875-reset-records-ready,r875-reset-clears-source-0-only
wait
for f in $P/receipts/plants/*.rc; do echo "$(basename $f .rc) rc=$(cat $f)"; done
grep -h "^\[ok\]\|^\[ESCAPED\]\|^CAMPAIGN" $P/receipts/plants/*.log
