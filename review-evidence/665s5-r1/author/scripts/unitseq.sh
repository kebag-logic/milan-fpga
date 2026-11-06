#!/bin/bash
# Start a sequence of heavy steps (seq.sh) as its own transient unit (MemoryMax 10G, pinned to a CPU range), not waited for.
# usage: unit.sh NAME CPUS CHECKOUT LOG CWD_REL CMD...
set -u
S=$MANAGEMENT/2026-09-23/665s5-a702/scripts
N=$1 CPUS=$2; shift 2
systemd-run --user --quiet --unit="milan-665s5-a702-$N" --collect --property=MemoryMax=10G \
    --setenv=HOME=$WORKSPACE_HOME --setenv=TMPDIR=$VALIDATION_STORAGE/665s5-a702/tmp \
    --setenv=PATH=$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin \
    /usr/bin/taskset -c "$CPUS" /bin/bash "$S/seq.sh" "$@"
echo "started milan-665s5-a702-$N on $CPUS"
