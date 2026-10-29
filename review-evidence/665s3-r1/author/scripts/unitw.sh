#!/bin/bash
# One heavy gate as its own transient unit, MemoryMax 10G, pinned to a CPU range, waited for (a chain's step).
# usage: unitw.sh NAME CPUS CHECKOUT LOG CWD_REL CMD...
set -u
S=$MANAGEMENT/2026-09-23/665s3-a697c/scripts
N=$1 CPUS=$2; shift 2
systemd-run --user --wait --quiet --unit="milan-665s3-a697c-$N" --collect --property=MemoryMax=10G \
    --setenv=HOME=$WORKSPACE_HOME --setenv=TMPDIR=$VALIDATION_STORAGE/665s3-a697c/tmp --setenv=PATH=$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin \
    /usr/bin/taskset -c "$CPUS" /bin/bash "$S/gate.sh" "$@"
