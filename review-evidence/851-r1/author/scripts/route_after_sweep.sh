#!/usr/bin/env bash
# route_after_sweep.sh <head>: hold until every shard of the head's sweep has written its results.json and no shard unit
# is active (never a route beside a sweep), then run route.sh <head>.
set -u
H=$1; S=$VALIDATION_STORAGE/scratch/851-a744/sweep-${H:0:8}; here=$(cd "$(dirname "$0")" && pwd)
until [ "$(ls $S/shard-*/spec/results.json 2>/dev/null | wc -l)" -ge 4 ] && \
      ! systemctl --user list-units --plain --no-legend --state=active "milan-851-a744-${H:0:8}-shard*" | grep -q shard; do
  sleep 30
done
echo "sweep done $(date -Iseconds)" > $VALIDATION_STORAGE/scratch/851-a744/route-after-${H:0:8}.log
exec bash "$here/route.sh" "$H"
