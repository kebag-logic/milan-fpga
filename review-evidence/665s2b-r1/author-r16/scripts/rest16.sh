#!/bin/bash
# After the 13:10 host reset: docs.yml's last two jobs and its verifier, then the lane gates from nvm_selftest, in
# this lane's unit, one after the other. usage: rest16.sh HEAD
set -u
H=$1
S=$MANAGEMENT/2026-09-23/665s2b-a683u/scripts
T=$VALIDATION_STORAGE/665s2b-a683u
bash $S/docsrest.sh "$H" "$T/docs-$H" docs-gates-2
tr -d '\000' < $T/lane-logs-final2/summary.txt | grep -v '^[[:space:]]*$' > $T/lane-logs-final2/summary.tmp
mv $T/lane-logs-final2/summary.tmp $T/lane-logs-final2/summary.txt
echo "# resumed at nvm_selftest after the 13:10 host reset" >> $T/lane-logs-final2/summary.txt
FROM=nvm_selftest bash $S/lane_gates.sh "$H" final2
