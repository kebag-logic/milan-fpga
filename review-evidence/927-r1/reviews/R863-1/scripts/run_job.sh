#!/bin/sh
# Run one suite or campaign in a probe tree with the pinned Verilator first on
# PATH and bounded build jobs; write <receipts>/<name>.log and <name>.rc.
# usage: run_job.sh <packet-dir> <tree-dir> <name> <command...>
set -u
P=$1; T=$2; N=$3; shift 3
R=$P/receipts
mkdir -p "$R"
PATH=$P/scratch/bin:$PATH
VERILATOR_JOBS=${VERILATOR_JOBS:-4}
VBUILD_JOBS=${VBUILD_JOBS:-4}
export PATH VERILATOR_JOBS VBUILD_JOBS
{
  echo "# job $N in $T at $(git -C "$T" rev-parse HEAD)"
  echo "# verilator: $(verilator --version)"
  echo "# command: $*"
  echo "# start: $(date -u +%FT%TZ)"
} > "$R/$N.log"
( cd "$T" && "$@" ) >> "$R/$N.log" 2>&1
rc=$?
echo "# end: $(date -u +%FT%TZ) rc=$rc" >> "$R/$N.log"
echo $rc > "$R/$N.rc"
