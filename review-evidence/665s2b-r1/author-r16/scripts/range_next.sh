#!/bin/bash
# When a leg's unit ends, book its range again: start the next unit on that range once cpu_ranges.py lists it free.
# usage: range_next.sh UNIT RANGE NEXT_UNIT CMD...
set -u
S=$MANAGEMENT/2026-09-23/665s2b-a683u/scripts
T=$VALIDATION_STORAGE/665s2b-a683u
UNIT=$1 RANGE=$2 NEXT=$3; shift 3
until ! systemctl --user is-active -q "milan-665s2b-a683u-$UNIT"; do sleep 60; done
until python3 $MANAGEMENT/2026-09-23/cpu_ranges.py show 2>&1 | tail -1 | grep -q "'$RANGE'"; do sleep 60; done
echo "$(date +%T) $UNIT ended; $RANGE free; start $NEXT" >> $T/logs/range_next.txt
python3 $MANAGEMENT/2026-09-23/cpu_ranges.py show 2>&1 | tail -1 >> $T/logs/range_next.txt
bash $S/unit.sh "$NEXT" "$RANGE" 16G -- "$@" >> $T/logs/range_next.txt 2>&1
