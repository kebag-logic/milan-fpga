#!/bin/bash
# The firmware-boundary job's steps (firmware_boundary.sh) from a checkout, with LiteX and migen on
# PYTHONPATH and temporary files on disk, into a log with the head, elapsed and rc last.
# usage: boundary_unit.sh CHECKOUT LOG SDK_DEST
set -u
C=$1 LOG=$2 DEST=$3
export PYTHONPATH=$WORKSPACE_HOME/litex-milan/litex:$WORKSPACE_HOME/litex-milan/migen
export TMPDIR=$VALIDATION_STORAGE/scratch/665s1-a680k-work/tmp
cd "$C" || exit 2
start=$(date +%s)
echo "HEAD $(git rev-parse HEAD) DIRTY $(git status --porcelain --untracked-files=no | wc -l)" > "$LOG"
bash $MANAGEMENT/2026-09-23/665s1-a680k/probes/firmware_boundary.sh \
  $VALIDATION_TOOLS/bootlin-504-probe/riscv32-ilp32d--glibc--stable-2025.08-1.tar.xz "$DEST" >> "$LOG" 2>&1
rc=$?
echo "elapsed=$(( $(date +%s) - start ))s tree: $(git status --porcelain --untracked-files=all --ignore-submodules=none | wc -l) changed path(s) after" >> "$LOG"
echo "rc=$rc" >> "$LOG"
