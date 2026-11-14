#!/bin/bash
# Start one heavy job of lane 895 (round 5) as its own transient unit on a CPU range booked by cpu_ranges.py pick.
# usage: unit.sh NAME CPU_RANGE MEMORY_MAX CWD -- CMD...   (output in units/NAME.log, rc in units/NAME.rc)
set -u
NAME=$1 RANGE=$2 MEM=$3 CWD=$4; shift 4
[ "$1" = "--" ] && shift
U=/data-2/milan/tmp/895-a775/r5/units
mkdir -p "$U" "/data-2/milan/tmp/895-a775/r5/tmp/$NAME"
rm -f "$U/$NAME.rc"
exec systemd-run --user --unit="milan-895-a775-r5-$NAME" --collect --property=MemoryMax="$MEM" \
  --setenv=HOME=$WORKSPACE_HOME --setenv=PATH=$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin \
  /usr/bin/taskset -c "$RANGE" /bin/bash -c ". $MANAGEMENT/2026-09-23/895-a775/scripts/env.sh
export TMPDIR=/data-2/milan/tmp/895-a775/r5/tmp/$NAME
cd $CWD || exit 3
{ echo \"# \$(date -Iseconds) head \$(git rev-parse HEAD 2>/dev/null) dirty \$(git status --porcelain 2>/dev/null | wc -l) range $RANGE\"
  $*
  r=\$?
  echo \"# \$(date -Iseconds) rc \$r\"; } > $U/$NAME.log 2>&1
echo \$r > $U/$NAME.rc"
