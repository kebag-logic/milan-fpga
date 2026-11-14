#!/bin/bash
# Launch the map rows plus reviewer plants in 8 detached shards; each writes its log and rc.
P=$PACKET
T=$CLONE
NAMES=$(python3 -I -c "import sys;sys.path[:0]=['$T/sw/firmware/ctrl/test'];import aecp_map_mutants as m;print(' '.join(r[0] for r in m.ROWS))")
rm -rf $P/scratch/maprows $P/receipts/maprows; mkdir -p $P/scratch/maprows $P/receipts/maprows
for i in 0 1 2 3 4 5 6 7; do
  setsid nohup bash -c "python3 -I $P/scripts/run_rows.py $T $P/scratch/maprows/s$i $i 8 --extra $NAMES > $P/receipts/maprows/s$i.log 2>&1; echo \$? > $P/receipts/maprows/s$i.rc" >/dev/null 2>&1 < /dev/null &
done
