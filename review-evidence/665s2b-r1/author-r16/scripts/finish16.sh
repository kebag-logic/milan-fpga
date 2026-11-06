#!/bin/bash
# The harness gate legs at the final head, after the 13:10 host reset: once every group of a leg is finished by the
# leg or its helpers (combine.py), stop the helper units still running duplicates, then merge and regrade the whole
# leg from the clone it was built from (finish_leg.sh). usage: finish16.sh LEG HELPERS POINT
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683u/scripts/env.sh
S=$MANAGEMENT/2026-09-23/665s2b-a683u/scripts
T=$VALIDATION_STORAGE/665s2b-a683u
LEG=$1 HELPERS=$2 POINT=$3
until python3 -B $S/combine.py $T/G2 $T/builds/$LEG "$HELPERS" all | grep -q " 0 by neither"; do sleep 30; done
echo "$(date +%T) $LEG: every group finished ($HELPERS)" >> $T/logs/dispatch.txt
for h in ${HELPERS//,/ }; do
    systemctl --user is-active --quiet "milan-665s2b-a683u-$h.service" && \
        systemctl --user stop "milan-665s2b-a683u-$h.service" && echo "$(date +%T) stopped $h's unit (its remaining runs duplicate finished groups)" >> $T/logs/dispatch.txt
done
sleep 10
if pgrep -f "$T/builds/$LEG/native/Vsim" > /dev/null; then echo "$(date +%T) $LEG: simulations still running" >> $T/logs/dispatch.txt; exit 3; fi
bash $S/finish_leg.sh "$LEG" G2 "$HELPERS" all "$POINT"
echo "$(date +%T) $LEG regraded: $(tail -1 $T/logs/$LEG-regrade.log)" >> $T/logs/dispatch.txt
