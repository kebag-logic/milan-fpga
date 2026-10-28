#!/bin/bash
# One gate from the lane checkout in this unit: system python, LiteX and migen on PYTHONPATH, TMPDIR on disk.
#   $1 the log   $2... the command; the log ends "rc=N elapsed=Ns" (run_gate.sh), the head first.
set -u
export PYTHONPATH=$WORKSPACE_HOME/litex-milan/litex:$WORKSPACE_HOME/litex-milan/migen
export TMPDIR=$VALIDATION_STORAGE/scratch/665s1-a680k-work/tmp
cd $LANES/665-s1-faces || exit 2
LOG=$1; shift
echo "HEAD $(git rev-parse HEAD) DIRTY $(git status --porcelain --untracked-files=no | wc -l)" > "$LOG.head"
$MANAGEMENT/2026-09-23/665s1-a680k/probes/run_gate.sh "$LOG" "$@"
