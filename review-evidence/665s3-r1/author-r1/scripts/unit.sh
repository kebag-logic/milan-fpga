#!/bin/bash
# One heavy gate as its own transient unit, MemoryMax 10G, pinned to a CPU range; never inside the agent's unit.
# usage: unit.sh NAME CPUS CHECKOUT LOG CWD_REL CMD...
set -eu
S=$MANAGEMENT/2026-09-23/665s3-a697b/scripts
N=$1 CPUS=$2; shift 2
systemd-run --user --unit="milan-665s3-a697b-$N" --collect --property=MemoryMax=10G \
    --setenv=HOME=$WORKSPACE_HOME --setenv=TMPDIR=$VALIDATION_STORAGE/665s3-a697b/tmp --setenv=PATH=$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin \
    /usr/bin/taskset -c "$CPUS" /bin/bash "$S/gate.sh" "$@"
